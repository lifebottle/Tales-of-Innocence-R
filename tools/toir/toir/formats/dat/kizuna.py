from .datfile import DatFile
from ...text import decode_text, remove_redundant_cc
from ...csvhelper import write_csv_data
import struct
import io
from .sections import encode_section_text

def _extract_kizuna(f):
    dat = DatFile(f)
    kizuna = {}
    for i in range(dat.count):
        section = dat.read_section(i)
        count = 80
        kizuna[i] = [decode_text(section, 0x31 * j) for j in range(count)]
    return kizuna

def extract_kizuna(l7cdir, outputdir):
    with open(l7cdir / '_Data/System/KizunaDataPack.dat', 'rb') as f:
        kizuna = _extract_kizuna(f)
    with open(outputdir / 'KizunaDataPack.csv', 'w', encoding='utf-8', newline='') as f:
        write_csv_data(f, 'iis', ['chara', '#', 'japanese'], kizuna)
        
#logic not completed
def recompile_bond(l7cdir, csvdir, outputdir):
#open the csv
    with open(csvdir / 'Bond.csv', 'r', encoding='utf-8', newline='') as f:
        styles = read_csv_data(f, 'iis', ['chara','#', 'English'])
        
#open the dat        
    with open(l7cdir / '_Data/System/KizunaDataPack.dat', 'rb') as f:
        binary = f.read()
    dat = DatFile(io.BytesIO(binary))
    
#read the csv and insert in dat  
    kizuna = {}  
    for i in range(dat.count):
        section = bytearray(dat.sections[i])
        count = 80
        kizuna[i] = [encode_section_text(section, chara, 0x31 * j, max_length=0x30, id=f'CharaStyleDataPack.csv:{i}')for j in range(count)]
        #dat.sections[i] = section   
        
 #save the dat                               
    dat.save_to_file(outputdir / '_Data/System/test/KizunaDataPack.dat')