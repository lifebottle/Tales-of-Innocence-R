from ...text import decode_text
from ...csvhelper import write_csv_data
import struct

def _extract_succession(f):
    section = f.read()
    count, = struct.unpack_from('<L', section, 0)
    succession = {}
    for i in range(count):
        succession[i] = {
            'name': decode_text(section, 0x09 + i * 0xD0),
            'description': decode_text(section, 0x42 + i * 0xD0),
        }
    return succession

def extract_succession(l7cdir, outputdir):
    with open(l7cdir / '_Data/System/SuccessionData.dat', 'rb') as f:
        styles = _extract_succession(f)
    with open(outputdir / 'SuccessionData.csv', 'w', encoding='utf-8', newline='') as f:
        write_csv_data(f, 'ifs', ['index', 'field', 'japanese'], styles)
