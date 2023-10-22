from .datfile import DatFile
from ...text import decode_text
from ...csvhelper import write_csv_data, read_csv_file, read_csv_data
import struct
import io
from .sections import encode_section_text

def _extract_chara_styles(f):
    dat = DatFile(f)
    section = dat.read_section(1)
    count, = struct.unpack_from('<L', section, 0)
    styles = [decode_text(section, 4 + 0x8A * i) for i in range(count)]
    return styles

def extract_chara_styles(l7cdir, outputdir):
    with open(l7cdir / '_Data/System/CharaStyleDataPack.dat', 'rb') as f:
        styles = _extract_chara_styles(f)
    with open(outputdir / 'CharaStyleDataPack.csv', 'w', encoding='utf-8', newline='') as f:
        write_csv_data(f, 'is', ['#', 'Japanese'], styles)

#Lt insertion
# def recompile_chara_styles(l7cdir, csvdir, outputdir):
    # with open(l7cdir / '_Data/System/CharaStyleDataPack.dat', 'rb') as f:
        # styles = read_csv_file(csvdir / 'CharaStyleDataPack.csv', 'is', ['#', 'English'])
        
        # dat = DatFile(f)
        # section = bytearray(dat.section[1])
        # for i, style in styles.items():
            # encode_section_text(section, style, 4 + 0x8A * i, max_length=0x8A,
                                # id=f'CharaStyleDataPack.csv:{i}')
    # dat.save_to_file(outputdir / '_Data/System/CharaStyleDataPack.dat')
    
    
def recompile_chara_styles(l7cdir, csvdir, outputdir):
#open the csv
    with open(csvdir / 'CharaStyleDataPack.csv', 'r', encoding='utf-8', newline='') as f:
        styles = read_csv_data(f, 'is', ['#', 'English'])

#open the dat        
    with open(l7cdir / '_Data/System/CharaStyleDataPack.dat', 'rb') as f:
        binary = f.read()
    dat = DatFile(io.BytesIO(binary))
        
#read the csv and insert in dat        
    section = bytearray(dat.read_section(1))
    for i, style in styles.items():
        encode_section_text(section, style, 4 + 0x8A * i, max_length=0x8A, id=f'CharaStyleDataPack.csv:{i}')
    dat.sections[1].blob = section    
 
 #save the dat                               
    dat.save_to_file(outputdir / '_Data/System/CharaStyleDataPack.dat')