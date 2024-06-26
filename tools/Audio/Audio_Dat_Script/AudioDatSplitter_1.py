import struct
import sys
from dataclasses import dataclass
from pathlib import Path
from io import BytesIO
from subprocess import run
import shutil


def main() -> None:
    print("Audio script helper")
    if len(sys.argv) <= 4:
        print("Not enough arguments!")

    in_folder = Path(sys.argv[2]).resolve()
    out_folder = Path(sys.argv[3]).resolve()
    if sys.argv[1] == "--extract":
        converter_path = Path(sys.argv[4]).resolve()
        extract_audio(in_folder, out_folder, converter_path)
    elif sys.argv[1] == "--insert":
        if len(sys.argv) <= 5:
            print("Not enough arguments!")
        audio_folder = Path(sys.argv[4]).resolve()
        converter_path = Path(sys.argv[5]).resolve()
        insert_audio(in_folder, audio_folder, out_folder, converter_path)
    else:
        print(f"Invalid mode! {sys.argv[1]}")


def extract_audio(in_folder: Path, out_folder: Path, converter_path: Path) -> None:
    print(str(in_folder))
    for file in in_folder.glob("*.pck"):
        with open(file, "rb") as f:
            # Read the header
            header = f.read(0x30)

            # Sanity checks
            parts = struct.unpack_from("<I", header, 0x00)[0]
            pad = struct.unpack_from("<3I", header, 0x04)

            # ignore the non-3-part files
            if parts != 3:
                print(f"Parts amount different expected 3, got {parts} in file {file.as_posix()}. Skipping...")
                continue
            assert all([x == 0 for x in pad]), f"Pading_1 is not 0!"

            # Read the parts (assumed 3)
            offsets = struct.unpack_from("<I4xI4xI4x", header, 0x10)
            sizes = struct.unpack_from("<4xI4xI4xI", header, 0x10)
            
            # check for Battle-like files (lazy check)
            pck = f
            f.seek(offsets[2])
            if f.read(4) == b"\x03\x00\x00\x00":
                f.seek(offsets[2])
                pck = BytesIO(f.read(sizes[2]))
                header = pck.read(0x30)
                # Read the parts (assumed 3)
                offsets = struct.unpack_from("<I4xI4xI4x", header, 0x10)
                sizes = struct.unpack_from("<4xI4xI4xI", header, 0x10)


            blobs = []
            for off, size in zip(offsets, sizes):
                pck.seek(off)
                blobs.append(pck.read(size))

            # Only PPVA is of interest, so let's yoink that
            ppva_pos = struct.unpack_from("<I", blobs[2], 0x18)[0]
            pck.seek(ppva_pos + offsets[2])
            ppva_blob = pck.read()

            ppva_magic = ppva_blob[:4]
            assert ppva_magic == b"PPVA", f"PPVA has wrong MAGIC"
            index_low, index_high = struct.unpack_from("<II", ppva_blob, 0x10)
            riff_count = index_high - index_low + 1

            # Get RIFF's
            # riff_blob = BytesIO(blobs[0])
            riff_ptrs = struct.unpack_from("<" + ("I12x" * riff_count), ppva_blob, 0x20)
            riff_sizes = struct.unpack_from(
                "<" + ("8xI4x" * riff_count), ppva_blob, 0x20
            )
            riff_srates = struct.unpack_from(
                "<" + ("4xI8x" * riff_count), ppva_blob, 0x20
            )

        vag_folder = in_folder / "temp" / file.stem
        vag_folder.mkdir(exist_ok=True, parents=True)
        for i, (off, sz, sr) in enumerate(zip(riff_ptrs, riff_sizes, riff_srates), 1):
            if 0xFFFFFFFF in {off, sz, sr}:
                continue
            with open(vag_folder / f"{file.stem}_{i}.vag", "wb+") as o:
                o.write(b"VAGp")
                o.write(struct.pack(">IIIIIIHH", 0x30000, 0, sz, sr, 0, 0, 0, 0x100))
                o.write(struct.pack(">IIII", 0, 0, 0, 0))
                o.write(struct.pack(">IIII", 0, 0, 0, 0))
                o.write(blobs[0][off : off + sz])

        audio_folder = out_folder / file.stem
        audio_folder.mkdir(exist_ok=True, parents=True)
        for vag in vag_folder.glob("*.*"):
            run([
                str(converter_path),
                "-o",
                str(audio_folder / f"{vag.stem}.wav"),
                str(vag),
            ])
    
    shutil.rmtree(in_folder / "temp", ignore_errors=True)


def insert_audio(in_folder: Path, audio_folder: Path, out_folder: Path, converter_path: Path) -> None:
    for og_file in in_folder.glob("*.dat"):

        # Check existence
        wav_folder = audio_folder / og_file.stem

        if wav_folder.exists() == False:
            print(f"Skipping {og_file.name}, no audio folder found!")
            continue

        # Parse (Too lazy to compartmentalize this)
        with open(og_file, "rb") as f:
            # Read the header
            header = f.read(0x30)

            # Sanity checks
            parts = struct.unpack_from("<I", header, 0x00)[0]
            pad = struct.unpack_from("<3I", header, 0x04)

            assert parts == 3, f"Parts amount different expected 3, got {parts}"
            assert all([x == 0 for x in pad]), f"Pading_1 is not 0!"

            # Read the parts (assumed 3)
            offsets = struct.unpack_from("<I4xI4xI4x", header, 0x10)
            sizes = struct.unpack_from("<4xI4xI4xI", header, 0x10)
            blobs = []

            for off, size in zip(offsets, sizes):
                f.seek(off)
                blobs.append(f.read(size))

            # Only PPVA is of interest, so let's yoink that
            ppva_pos = struct.unpack_from("<I", blobs[2], 0x18)[0]
            f.seek(ppva_pos + offsets[2])
            ppva_blob = BytesIO(f.read())

            ppva_magic = ppva_blob.read(4)
            assert ppva_magic == b"PPVA", f"PPVA has wrong MAGIC"
            ppva_blob.seek(0x14)
            riff_count = struct.unpack("<I", ppva_blob.read(4))[0] + 1

        # Collect RIFF's
        riff_ptrs = []
        riff_sizes = []

        # Create new RIFF blob
        riff_blob = BytesIO()

        wav_in_folder = len(list(wav_folder.glob("*.wav")))
        assert (
            wav_in_folder == riff_count
        ), f"{og_file.name} has wrong amount of files, expected {riff_count} but got {wav_in_folder}"

        # Convert to vag
        vag_folder = audio_folder / "temp" / og_file.stem
        vag_folder.mkdir(exist_ok=True, parents=True)
        for wav in wav_folder.glob("*.wav"):
            run([
                str(converter_path),
                "-e",
                "-br",
                "72",
                str(wav),
                str(vag_folder / f"{wav.stem}.vag"),
            ])

        vag = [vag_folder / f"{og_file.stem}_{x}.vag" for x in range(1, riff_count + 1)]
        for vag_path in vag_files:
            with open(vag_path, "rb") as vag:
                riff = vag.read()
            riff_ptrs.append(riff_blob.tell())
            riff_blob.write(riff)
            riff_sizes.append(len(riff))

            # Align
            while (riff_blob.tell() % 0x10) != 0:
                riff_blob.write(b"\x00")
        riff_blob.seek(0)
        riff_blob = riff_blob.read()

        # Update PPVA
        for i, (ptr, size) in enumerate(zip(riff_ptrs, riff_sizes)):
            ppva_blob.seek(0x20 + (i * 0x10))
            ppva_blob.write(struct.pack("<I", ptr))
            ppva_blob.seek(0x28 + (i * 0x10))
            ppva_blob.write(struct.pack("<I", size))

        out_folder.mkdir(exist_ok=True, parents=True)
        new_file = out_folder / og_file.name

        # Write the darn thing
        blob_offsets = []
        with open(new_file, "wb+") as o:
            o.write(struct.pack("<IIII", 3, 0, 0, 0))
            o.write(struct.pack("<II", 0, 0))
            o.write(struct.pack("<II", 0, 0))
            o.write(struct.pack("<II", 0, 0))
            # Align
            while (o.tell() % 0x10) != 0:
                o.write(b"\x00")

            blob_offsets.append(o.tell())
            o.write(riff_blob)
            # Align
            while (o.tell() % 0x10) != 0:
                o.write(b"\x00")

            blob_offsets.append(o.tell())
            o.write(blobs[1])

            # Align
            while (o.tell() % 0x10) != 0:
                o.write(b"\x00")

            blob_offsets.append(o.tell())
            o.write(blobs[2][:ppva_pos])
            ppva_blob.seek(0)
            o.write(ppva_blob.read())

            o.seek(0x10)
            o.write(struct.pack("<II", blob_offsets[0], len(riff_blob)))
            o.write(struct.pack("<II", blob_offsets[1], len(blobs[1])))
            o.write(struct.pack("<II", blob_offsets[2], len(blobs[2])))

    shutil.rmtree(audio_folder / "temp", ignore_errors=True)


if __name__ == "__main__":
    main()
