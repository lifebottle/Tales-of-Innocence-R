from .sections import *
from .datfile import DatFile
from ...text import decode_text, remove_redundant_cc
from ...csvhelper import *
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

#new script taken from arte for reinsertion
def read_artes_csv(csvdir):
    artes = {}
    with open(csvdir / 'Operation.csv', 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f, ['category', 'index', 'field', 'japanese', 'english'])
        for row in reader:
            category = row['category']
            if not category:
                continue
            category = int(category)
            index = int(row['index'])
            field = row['field']
            translation = row['english']
            if not (0 <= category < 4): #updated to 3 instead of 8 
                raise ValueError('unknown category in Operation.csv')
            if category not in artes:
                artes[category] = {}
            if index not in artes[category]:
                artes[category][index] = {}
            if field == 'name':
                artes[category][index]['name'] = translation
            elif field == 'description':
                artes[category][index]['description'] = translation
            else:
                raise ValueError('unknown field in Operation.csv')
    return artes

def write_artes(category, section, artes):
    count, = struct.unpack_from('<L', section, 0)
    if count != len(artes):
        raise ValueError('Operation.csv: number of Artes does not match original')
    for i in range(count):
        start = 4 + i * 0xE0
        encode_section_text(section, artes[i]['name'], start + 0x24, max_length=0x28,
                            id=f'Operation.csv:{category},{i},name')
        encode_section_text(section, artes[i]['description'], start + 0x4D, max_length=0x90,
                            id=f'Operation.csv:{category},{i},description')

def insert_artes(binary, artes):
    newbinary = read_dat_header(binary)
    sections = [bytearray(section) for section in read_sections(binary)]
    for i in range(0, len(sections)):
        if i in artes:
            write_artes(i, sections[i], artes[i])
            newbinary = append_section(newbinary, sections[i])
    assert(len(binary) == len(newbinary))
    return newbinary

def recompile_operations(l7cdir, csvdir, outputdir):
    items = read_artes_csv(csvdir)
    with open(l7cdir / '_Data/System/OperationDataPack.dat', 'rb') as f:
        binary = f.read()
    binary = insert_artes(binary, items)
    outputdir = outputdir / '_Data/System'
    outputdir.mkdir(parents=True, exist_ok=True)
    with open(outputdir / 'OperationDataPack.dat', 'wb') as f:
        f.write(binary)