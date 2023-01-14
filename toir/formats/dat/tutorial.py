from .datfile import DatFile
from ...text import decode_text, remove_redundant_cc
from ...csvhelper import write_csv_data
import struct

def _extract_tutorial_text(f):
    dat = DatFile(f)
    tutorial = {}
    for i in range(dat.count):
        section = dat.read_section(i)
        count, = struct.unpack_from('<L', section, 0)
        tutorial[i] = [remove_redundant_cc(decode_text(section, 4 + 0x106 * j))
                        for j in range(count)]
    return tutorial

def extract_tutorial(l7cdir, outputdir):
    with open(l7cdir / '_Data/Battle/TutorialData.dat', 'rb') as f:
        items = _extract_tutorial_text(f)
    with open(outputdir / 'TutorialData.csv', 'w', encoding='utf-8', newline='') as f:
        write_csv_data(f, 'iis', ['section', 'index', 'japanese'], items)
