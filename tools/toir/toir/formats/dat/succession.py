from .datfile import DatFile
from .sections import *
from ...csvhelper import write_csv_data, read_csv_file, read_csv_data
import struct
import io
from ...text import decode_text, encode_text
import csv

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


def read_artes_csv(csvdir):
    artes = {}
    with open(csvdir / 'SuccessionData.csv', 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f, ['category', 'index', 'field', 'japanese', 'english'])
        for row in reader:
            category = row['category']
            if not category:
                continue
            category = int(category)
            index = int(row['index'])
            field = row['field']
            english = row['english']
            
            if category not in artes:
                artes[category] = {}
            if index not in artes[category]:
                artes[category][index] = {}
            if field == 'name':
                artes[category][index]['name'] = english
            elif field == 'description':
                artes[category][index]['description'] = english
            else:
                raise ValueError('unknown field in SuccessionData.csv')
    #print(artes)
    return artes

def write_artes(category, section, artes):
    count, = struct.unpack_from('<L', section, 0)
    for i in range(count):
        #print(artes[i]['name'])
        #print(artes[i]['description'])
        encode_section_text(section, artes[i]['name'], 0x09 + i * 0xD0, max_length=0x28,
                            id=f'SuccessionData.csv:{category},{i},name')
        encode_section_text(section, artes[i]['description'], 0x42 + i * 0xD0, max_length=0x89,
                            id=f'SuccessionData.csv:{category},{i},description')

def insert_artes(binary, artes):
    newbinary = binary#made only binary cause no section
    sections = [bytearray(binary)]#remove the junk keep only binary
    for i in range(0, len(sections)):#the for loop can be remove
        if i in artes:
            write_artes(i, sections[i], artes[i])#if you remove the for loop put sections[0]
            newbinary = sections[i]#remove the append or else append end of file

    assert(len(binary) == len(newbinary))
    return newbinary

def recompile_succession(l7cdir, csvdir, outputdir):
    items = read_artes_csv(csvdir)
    with open(l7cdir / '_Data/System/SuccessionData.dat', 'rb') as f:
        binary = f.read()
    binary = insert_artes(binary, items)
    outputdir = outputdir / '_Data/System'
    outputdir.mkdir(parents=True, exist_ok=True)
    with open(outputdir / 'SuccessionData.dat', 'wb') as f:
        f.write(binary)