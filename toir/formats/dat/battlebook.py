from .sections import read_sections
import struct
from ...text import decode_text
import csv

def read_battle_book(section):
    count, = struct.unpack_from('<L', section, 0)
    title = decode_text(section, 4);
    text = []
    for i in range(count):
        text.append(decode_text(section, 0x30 + 0x83 * i))
    return title, text

def _extract_battle_book(binary):
    battle_book = {}
    sections = read_sections(binary)
    for i in range(0, len(sections)):
        battle_book[i] = read_battle_book(sections[i])
    return battle_book

def extract_battle_book(l7cdir, outputdir):
    with open(l7cdir / '_Data/System/BattleBookDataPack.dat', 'rb') as f:
        binary = f.read()
    items = _extract_battle_book(binary)
    with open(outputdir / 'BattleBookDataPack.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, ['category', 'field', 'index', 'text'])
        for category, entry in items.items():
            writer.writerow({
                'category': category,
                'field': 'title',
                'index': '',
                'text': entry[0],
            })
            for i, text in enumerate(entry[1]):
                writer.writerow({
                    'category': category,
                    'field': 'text',
                    'index': i,
                    'text': text,
                })
