from ...text import decode_text
from ...csvhelper import write_csv_data
import struct

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
        write_csv_data(f, 'ifs', ['index', 'field', 'japanese'], mission)
