from .datfile import DatFile
from ...text import decode_text, remove_redundant_cc
from ...csvhelper import write_csv_data
import struct

def _extract_operation(f):
    dat = DatFile(f)

    section = dat.read_section(0)
    count, = struct.unpack_from('<L', section, 0)
    operation = {}
    operation[0] = [{
            'name': decode_text(section, 0x13 + 0xB2 * i),
            'description': decode_text(section, 0x24 + 0xB2 * i)
        } for i in range(count)]

    section = dat.read_section(1)
    count, = struct.unpack_from('<L', section, 0)
    operation[1] = [{
            'name': decode_text(section, 0x09 + 0xC0 * i),
            'description': decode_text(section, 0x32 + 0xC0 * i)
        } for i in range(count)]

    section = dat.read_section(3)
    count, = struct.unpack_from('<L', section, 0)
    operation[3] = [{
            'name': decode_text(section, 0x08 + 0xAF * i),
            'description': decode_text(section, 0x21 + 0xAF * i)
        } for i in range(count)]

    return operation

def extract_operation(l7cdir, outputdir):
    with open(l7cdir / '_Data/System/OperationDataPack.dat', 'rb') as f:
        operation = _extract_operation(f)
    with open(outputdir / 'OperationDataPack.csv', 'w', encoding='utf-8', newline='') as f:
        write_csv_data(f, 'iifs', ['category', 'index', 'field', 'japanese'], operation)
