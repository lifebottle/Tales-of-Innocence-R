from .sections import *
import struct
from ...text import decode_text
import csv

def read_artes(section):
    count, = struct.unpack_from('<L', section, 0)
    items = []
    for i in range(count):
        name = decode_text(section, 4 + i * 0xE0 + 0x24)
        description = decode_text(section, 4 + i * 0xE0 + 0x4D)
        items.append({
            'name': name,
            'description': description,
        })
    return items

def _extract_artes(binary):
    artes = {}
    sections = read_sections(binary)
    for i in range(0, len(sections)):
        artes[i] = read_artes(sections[i])
    return artes

def extract_artes(l7cdir, outputdir):
    with open(l7cdir / '_Data/System/ArtsDataPack.dat', 'rb') as f:
        binary = f.read()
    items = _extract_artes(binary)
    
    with open(outputdir / 'ArtsDataPack.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, ['category', 'index', 'field', 'text'])
        for category, items in items.items():
            for i, item in enumerate(items):
                writer.writerow({
                    'category': category,
                    'index': i,
                    'field': 'name',
                    'text': item['name'],
                })
                writer.writerow({
                    'category': category,
                    'index': i,
                    'field': 'description',
                    'text': item['description'],
                })

def read_artes_csv(csvdir):
    artes = {}
    with open(csvdir / 'ArtsDataPack.csv', 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f, ['category', 'index', 'field', 'japanese', 'translation'])
        for row in reader:
            category = row['category']
            if not category:
                continue
            category = int(category)
            index = int(row['index'])
            field = row['field']
            translation = row['translation']
            if not (0 <= category < 8):
                raise ValueError('unknown category in ArtsDataPack.csv')
            if category not in artes:
                artes[category] = {}
            if index not in artes[category]:
                artes[category][index] = {}
            if field == 'name':
                artes[category][index]['name'] = translation
            elif field == 'description':
                artes[category][index]['description'] = translation
            else:
                raise ValueError('unknown field in ArtsDataPack.csv')
    return artes

def write_artes(category, section, artes):
    count, = struct.unpack_from('<L', section, 0)
    if count != len(artes):
        raise ValueError('ArtsDataPack.csv: number of Artes does not match original')
    for i in range(count):
        start = 4 + i * 0xE0
        encode_section_text(section, artes[i]['name'], start + 0x24, max_length=0x28,
                            id=f'ArtsDataPack.csv:{category},{i},name')
        encode_section_text(section, artes[i]['description'], start + 0x4D, max_length=0x90,
                            id=f'ArtsDataPack.csv:{category},{i},description')

def insert_artes(binary, artes):
    newbinary = read_dat_header(binary)
    sections = [bytearray(section) for section in read_sections(binary)]
    for i in range(0, len(sections)):
        write_artes(i, sections[i], artes[i])
        newbinary = append_section(newbinary, sections[i])
    assert(len(binary) == len(newbinary))
    return newbinary

def recompile_artes(l7cdir, csvdir, outputdir):
    items = read_artes_csv(csvdir)
    with open(l7cdir / '_Data/System/ArtsDataPack.dat', 'rb') as f:
        binary = f.read()
    binary = insert_artes(binary, items)
    outputdir = outputdir / '_Data/System'
    outputdir.mkdir(parents=True, exist_ok=True)
    with open(outputdir / 'ArtsDataPack.dat', 'wb') as f:
        f.write(binary)
