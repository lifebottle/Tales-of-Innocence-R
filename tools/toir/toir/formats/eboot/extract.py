from .embeddedptr import EMBEDDED_POINTERS
from .ptrtables import POINTER_TABLES
from .load import load_eboot, address_to_offset
from ...text import decode_text
import struct
import csv

def _extract_eboot(eboot):
    texts = {}
    for target, _ in EMBEDDED_POINTERS:
        texts[target] = decode_text(eboot, address_to_offset(target))
    for _, start, end in POINTER_TABLES:
        for pointer in range(start, end, 4):
            target, = struct.unpack_from('<L', eboot, address_to_offset(pointer))
            texts[target] = decode_text(eboot, address_to_offset(target))
    return texts

def extract_eboot(ebootpath, outputdir)    :
    eboot = load_eboot(ebootpath)
    strings = _extract_eboot(eboot);
    with open(outputdir / "eboot.csv", 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, ['id', 'japanese'])
        for id, japanese in strings.items():
            writer.writerow({
                'id': f'{id:08X}',
                'japanese': japanese,
            })
