from .sections import read_sections
import struct
from ...text import decode_text
import csv

def _extract_chara_abilities(binary):
    count, = struct.unpack_from('<L', binary, 0)
    abilities = {}
    for i in range(count):
        abilities[i] = {
            'name': decode_text(binary, 0x17 + i * 0xC8),
            'description': decode_text(binary, 0x40 + i * 0xC8),
        }
    return abilities

def extract_chara_ability(l7cdir, outputdir):
    with open(l7cdir / '_Data/System/CharaAbility.dat', 'rb') as f:
        binary = f.read()
    items = _extract_chara_abilities(binary)
    with open(outputdir / 'CharaAbility.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, ['index', 'field', 'text'])
        for i, ability in items.items():
            writer.writerow({
                'index': i,
                'field': 'name',
                'text': ability['name'],
            })
            writer.writerow({
                'index': i,
                'field': 'description',
                'text': ability['description'],
            })
