from .sections import encode_section_text
from .datfile import DatFile
import struct
import io
from ...text import decode_text
from ...csvhelper import read_csv_data
import csv

def write_csv_data(f, format, col_names, data):
    writer = csv.DictWriter(f, col_names)
    if format[0] == 'i':
        if isinstance(data, list):
            for i, value in enumerate(data):
                writer.writerow({
                    col_names[0]: i,
                    col_names[-1]: value,
                })
        elif isinstance(data, dict):
            for i, value in data.items():
                writer.writerow({
                    col_names[0]: i,
                    col_names[-1]: value,
                })

def read_chara_names(l7cdir):
    with open(l7cdir / '_Data/Field/PackFieldData.dat', 'rb') as f:
        binary = f.read()
    dat = DatFile(io.BytesIO(binary))
    
    namesdat = dat.read_section(30)
    count, = struct.unpack_from('<H', namesdat, 0)
    names = []
    for i in range(count):
        names.append(decode_text(namesdat, 2 + i * 0x24))

    section = dat.read_section(32)
    count, = struct.unpack_from('<H', section, 0)
    locations = []
    for i in range(count):
        locations.append(decode_text(section, 2 + i * 0x30))

    section = dat.read_section(37)
    count, = struct.unpack_from('<H', section, 0)
    skits = []
    for i in range(count):
        file_index = struct.unpack_from('<H', section, i * 0x74 + 0x12)
        skits.append((file_index, decode_text(section, i * 0x74 + 0x14)))
    return names, locations, skits

def extract_chara_names(l7cdir, outputdir):
    names, locations, skits = read_chara_names(l7cdir)
    with open(outputdir / 'CharaNames.csv', 'w', encoding='utf-8', newline='') as f:
        write_csv_data(f, 'i', ['index', 'japanese'], names)
    with open(outputdir / 'Locations.csv', 'w', encoding='utf-8', newline='') as f:
        write_csv_data(f, 'i', ['index', 'japanese'], locations)
    with open(outputdir / 'SkitNames.csv', 'w', encoding='utf-8', newline='') as f:
        write_csv_data(f, 'i', ['index', 'japanese'], skits)

def recompile_pack_field(l7cdir, csvdir, outputdir):
    with open(csvdir / 'CharaNames.csv', 'r', encoding='utf-8', newline='') as f:
        chara_names = read_csv_data(f, 'is', ['#', 'English'])

    with open(l7cdir / '_Data/Field/PackFieldData.dat', 'rb') as f:
        binary = f.read()
    dat = DatFile(io.BytesIO(binary))

    namesdat = bytearray(dat.sections[30])
    for i, name in chara_names.items():
        encode_section_text(namesdat, name, 2 + i * 0x24, max_length=0x20,
                            id=f'CharaNames.csv:{i}')
    dat.sections[30] = namesdat

    outputfile = outputdir / '_Data/Field/PackFieldData.dat'
    outputfile.parent.mkdir(parents=True, exist_ok=True)
    with open(outputfile, 'wb') as f:
        dat.save(f)
