from .datfile import DatFile
from ...text import decode_text, remove_redundant_cc
from ...csvhelper import write_csv_data
import struct

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
