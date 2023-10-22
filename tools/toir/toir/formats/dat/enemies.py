from .sections import encode_section_text
from .datfile import DatFile
from ...text import decode_text, remove_redundant_cc, encode_text
from ...csvhelper import write_csv_data
import struct
import io
from ...text import decode_text
from ...csvhelper import read_csv_data
import csv

def _extract_enemies(f):
    dat = DatFile(f)
    section = dat.read_section(1)
    count, = struct.unpack_from('<L', section, 0)
    skills = [decode_text(section, 4 + 0x40 * i) for i in range(count)]
    
    section = dat.read_section(2)
    count, = struct.unpack_from('<L', section, 0)
    names = [decode_text(section, 8 + 0x138 * i) for i in range(count)]
    
    return skills, names

def extract_enemies(l7cdir, outputdir):
    with open(l7cdir / '_Data/System/EnemyParam.dat', 'rb') as f:
        skills, names = _extract_enemies(f)
        
    with open(outputdir / 'EnemyParam_Skills.csv', 'w', encoding='utf-8', newline='') as f:
        write_csv_data(f, 'is', ['index', 'japanese'], skills)
        
    with open(outputdir / 'EnemyParam_Names.csv', 'w', encoding='utf-8', newline='') as f:
        write_csv_data(f, 'is', ['index', 'japanese'], names)
        
def recompile_enemies(l7cdir, csvdir, outputdir):
#open the csv
    with open(csvdir / 'EnemyParam_Names.csv', 'r', encoding='utf-8', newline='') as f:
        enemies_names = read_csv_data(f, 'is', ['#', 'English'])
        
    with open(csvdir / 'EnemyParam_Artes.csv', 'r', encoding='utf-8', newline='') as f:
        enemies_artes = read_csv_data(f, 'is', ['#', 'English'])

#open the original dat        
    with open(l7cdir / '_Data/System/EnemyParam.dat', 'rb') as f:
        binary = f.read()
    dat = DatFile(io.BytesIO(binary))

#read the csv and insert in dat
    section = bytearray(dat.read_section(1))
    for i, arte in enemies_artes.items():
        encode_section_text(section, arte, 4 + 0x40 * i, max_length=0x24, id=f'EnemyParam_Artes.csv:{i}')
    dat.sections[1].blob = section 

    section = bytearray(dat.read_section(2))
    for i, name in enemies_names.items():
        encode_section_text(section, name, 8 + 0x138 * i, max_length=0x2A, id=f'EnemyParam_Names.csv:{i}')
    dat.sections[2].blob = section    

#save the dat in new location
    outputfile = outputdir / '_Data/System/EnemyParam.dat'
    outputfile.parent.mkdir(parents=True, exist_ok=True)
    with open(outputfile, 'wb') as f:
        dat.save(f)
