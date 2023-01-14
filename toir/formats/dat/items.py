from .sections import read_sections, read_dat_header, append_section
import struct
from collections import namedtuple
from ...text import decode_text, encode_text
import csv

ItemCategory = namedtuple('ItemCategory', ['name', 'recordSize'])

_ITEM_CATEGORIES = [
    ItemCategory('Use', 0x4C),
    ItemCategory('Weapon', 0x54),
    ItemCategory('Armor', 0x54),
    ItemCategory('Helm', 0x54),
    ItemCategory('Acc', 0x5C),
    ItemCategory('Material', 0x3C),
    ItemCategory('Event', 0x3C),
    ItemCategory('DLC', 0x54),
    ItemCategory('CodeName', 0x50),
    ItemCategory('Recipe', 0x80),
    ItemCategory('RaveAbility', 0x48),
    ItemCategory('OperationCond', 0x3c),
]

def read_items(category, names, descriptions):
    count, = struct.unpack_from('<L', names, 0)
    items = []
    for i in range(count):
        name = decode_text(names, 4 + i * category.recordSize + 0xf)
        description = decode_text(descriptions, 4 + i * 0x92)
        items.append({
            'name': name,
            'description': description,
        })
    return items

def _extract_items(binary):
    items = {}
    sections = read_sections(binary)
    for i in range(0, len(_ITEM_CATEGORIES)):
        items[_ITEM_CATEGORIES[i].name] = read_items(_ITEM_CATEGORIES[i],
                                                     sections[2*i],
                                                     sections[2*i+1])
    return items

def extract_items(l7cdir, outputdir):
    with open(l7cdir / '_Data/System/ItemDataPack.dat', 'rb') as f:
        binary = f.read()
    items = _extract_items(binary)
    with open(outputdir / 'ItemDataPack.csv', 'w', encoding='utf-8', newline='') as f:
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

def read_item_csv(csvdir):
    items = {}
    with open(csvdir / 'ItemDataPack.csv', 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f, ['category', 'index', 'field', 'japanese', 'translation'])
        for row in reader:
            category = row['category']
            if not category:
                continue
            index = int(row['index'])
            field = row['field']
            translation = row['translation']
            if category not in items:
                items[category] = {}
            if index not in items[category]:
                items[category][index] = {}
            if field == 'name':
                items[category][index]['name'] = translation
            elif field == 'description':
                items[category][index]['description'] = translation
            else:
                raise ValueError('unknown field in ItemDataPack.csv')
    return items

def write_items(category, names, descriptions, items):
    count, = struct.unpack_from('<L', names, 0)
    if count != len(items):
        raise ValueError('number of items does not match original')
    for i in range(count):
        name = encode_text(items[i]['name'])
        if len(name) > 0x2C:
            print(f'"{category.name},{i},name" is too long (44 bytes allowed), truncating...')
            name = name[:0x2B] # one less for trailing zero
        name += bytes(0x2C - len(name))
        name_start = 4 + i * category.recordSize + 0xf
        names[name_start:name_start+0x2C] = name
        
        description = encode_text(items[i]['description'])
        if len(description) > 0x92:
            print(f'"{category.name},{i},description" is too long (144 bytes allowed), truncating...')
            description = description[:0x91] # one less for trailing zero
        description += bytes(0x92 - len(description))
        desc_start = 4 + i * 0x92
        descriptions[desc_start:desc_start+0x92] = description

def insert_items(binary, items):
    newbinary = read_dat_header(binary)
    sections = [bytearray(section) for section in read_sections(binary)]
    for i in range(0, len(_ITEM_CATEGORIES)):
        write_items(_ITEM_CATEGORIES[i], sections[2*i], sections[2*i+1],
                    items[_ITEM_CATEGORIES[i].name])
        newbinary = append_section(newbinary, sections[2*i])
        newbinary = append_section(newbinary, sections[2*i+1])
    newbinary = append_section(newbinary, sections[-1])
    assert(len(binary) == len(newbinary))
    return newbinary

def recompile_items(l7cdir, csvdir, outputdir):
    items = read_item_csv(csvdir)
    with open(l7cdir / '_Data/System/ItemDataPack.dat', 'rb') as f:
        binary = f.read()
    binary = insert_items(binary, items)
    outputdir = outputdir / '_Data/System'
    outputdir.mkdir(parents=True, exist_ok=True)
    with open(outputdir / 'ItemDataPack.dat', 'wb') as f:
        f.write(binary)
