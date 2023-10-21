from .sections import encode_section_text
from .datfile import DatFile
from ...text import decode_text, encode_text
from ...csvhelper import write_csv_data
import struct
import io
from ...csvhelper import read_csv_data
import csv

def _extract_mission(f):
    binary = f.read()
    mission = {}
    count, = struct.unpack_from('<L', binary, 0)
    
    for i in range(count):
        mission[i] = {
            'line_1': decode_text(binary, 4 + i * 0xA8),
            'line_2': decode_text(binary, 4 + i * 0xA8 + 0x41),
            'target': decode_text(binary, 4 + i * 0xA8 + 0x82),
        }
    return mission
        

def extract_mission(l7cdir, outputdir):
    with open(l7cdir / '_Data/Battle/MissionData.dat', 'rb') as f:
        mission = _extract_mission(f)
    with open(outputdir / 'MissionData.csv', 'w', encoding='utf-8', newline='') as f:
        write_csv_data(f, 'ifs', ['Section', '#', 'Japanese'], mission)

def recompile_mission(l7cdir, csvdir, outputdir):
#open the csv
    with open(csvdir / 'MissionData.csv', 'r', encoding='utf-8', newline='') as f:
        missions = read_csv_data(f, 'ifs', ['Section', '#', 'Japanese', 'English'])

#open the original dat        
    with open(l7cdir / '_Data/Battle/MissionData.dat', 'rb') as f:
        binary = f.read()
    dat = DatFile(io.BytesIO(binary))
    section = bytearray(dat)
    for i, mission in missions.items():
        encode_section_text(section, mission[I]['line_1'], 4 + i * 0xA8, max_length=0x24,  id=f'MissionData.csv:{i}.line_1')
        encode_section_text(section, mission[I]['line_2'], 4 + i * 0xA8+0x41, max_length=0x24,  id=f'MissionData.csv:{i}.line_2')
        encode_section_text(section, mission[I]['target'], 4 + i * 0xA8+0x82, max_length=0x24,  id=f'MissionData.csv:{i}.target')
    dat.sections[1] = section 

#save the dat in new location
    outputfile = outputdir / '_Data/Battle/test/MissionData.dat'
    outputfile.parent.mkdir(parents=True, exist_ok=True)
    with open(outputfile, 'wb') as f:
        dat.save(f)
