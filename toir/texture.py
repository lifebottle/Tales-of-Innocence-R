import struct
import png
from .formats.dat import DatFile
from pathlib import Path

def export_texture(binary, path):
    width, height = struct.unpack_from('<HH', binary, 12)
    bpp = binary[0x10]
    offset = 0x12

    if bpp == 32:
        rows = []
        stride = width * 4
        for _ in range(height):
            rows.append(binary[offset:offset+stride])
            offset += stride    

        with open(path, 'wb') as f:
            writer = png.Writer(width, height, bitdepth=8, alpha=True, greyscale=False)
            writer.write_packed(f, reversed(rows))
    else:
        palette = []
        for _ in range(1 << bpp):
            color = struct.unpack_from('<BBBB', binary, offset)
            palette.append((color[2], color[1], color[0], color[3]))
            offset += 4    
        rows = []
        stride = (width * 8) // bpp
        for _ in range(height):
            rows.append(binary[offset:offset+stride])
            offset += stride    

        with open(path, 'wb') as f:
            writer = png.Writer(width, height, bitdepth=bpp, palette=palette)
            writer.write_packed(f, reversed(rows))

if __name__ == '__main__':
    import sys
    with open(sys.argv[1], 'rb') as f:
        binary = f.read()
    export_texture(binary, 'test_1.png')

_TEX_FILES = [
    ('_Data/System', 'SystemTex.dat'),
    ('_Data/System', 'SystemFaceTex_00.dat'),
    ('_Data/System', 'SystemFaceTex_01.dat'),
    ('_Data/System', 'SystemFaceTex_02.dat'),
    ('_Data/System', 'SystemFaceTex_03.dat'),
    ('_Data/System', 'SystemFaceTex_04.dat'),
    ('_Data/System', 'SystemFaceTex_05.dat'),
    ('_Data/System', 'SystemFaceTex_06.dat'),
    ('_Data/System', 'SystemFaceTex_07.dat'),
    ('_Data/Menu/BattleBook', 'BattleBookTex.dat'),
    ('_Data/GameOver', 'GameOverTex.dat'),
]

def extract_textures(l7cdir, outputdir):
    for tex_path, tex_file in _TEX_FILES:
        texoutdir = outputdir / tex_file[:-4]
        texoutdir.mkdir(parents=True, exist_ok=True)
        with open(l7cdir / f'{tex_path}/{tex_file}', 'rb') as f:
            dat = DatFile(f)
            for i, section in enumerate(dat.sections):
                export_texture(section, texoutdir / f'{i:04}.png')

def recompile_texture(texture):
    reader = png.Reader(bytes=texture)
    width, height, rows, info = reader.read()
    #print(info)

    if info['planes'] == 4 and info['bitdepth'] == 8:
        header = b'\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        header += struct.pack('<HH', width, height)
        header += b'\x20\x08'
        for row in reversed(list(rows)):
            for i in range(0, len(row), 4):
                header += struct.pack('BBBB', row[i + 2], row[i + 1],
                                      row[i + 0], row[i + 3])
        return header
    elif info['planes'] == 1 and info['bitdepth'] == 8 and info['greyscale'] == False:
        header = b'\x00\x01\x01\x00\x00\x00\x01\x20\x00\x00\x00\x00'
        header += struct.pack('<HH', width, height)
        header += b'\x08\x00'
        for entry in reader.palette():
            header += bytes([entry[2], entry[1], entry[0], entry[3]])
        for row in reversed(list(rows)):
            header += row        
        return header
        
def recompile_textures(l7cdir, texdir, outputdir):
    for tex_path, tex_file in _TEX_FILES:
        dir = texdir / Path(tex_path).name / tex_file[:-4]
        if dir.exists() and dir.is_dir():
            with open(l7cdir / f'{tex_path}/{tex_file}', 'rb') as f:
                dat = DatFile(f)
                for file in dir.glob('*.png'):
                    index = int(file.stem)
                    texture = open(file, 'rb').read()
                    dat.sections[index] = recompile_texture(texture)
                    (outputdir / Path(tex_path)).mkdir(parents=True, exist_ok=True)
                    print(outputdir / Path(tex_path) / tex_file)
                    with open(outputdir / Path(tex_path) / tex_file, 'wb') as f2:
                        dat.save(f2)