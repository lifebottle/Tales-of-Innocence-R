from .datfile import DatFile
from .sections import *
from ...csvhelper import write_csv_data, read_csv_file, read_csv_data
import struct
import io
from ...text import decode_text, encode_text
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


def read_artes_csv(csvdir):
    artes = {}
    with open(csvdir / 'CharaAbility.csv', 'r', encoding='utf-8', newline='') as f:
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
                raise ValueError('unknown field in CharaAbility.csv')
    #print(artes)
    return artes

def write_artes(category, section, artes):
    count, = struct.unpack_from('<L', section, 0)
    for i in range(count):
        #print(artes[i]['name'])
        #print(artes[i]['description'])
        encode_section_text(section, artes[i]['name'], 0x17 + i * 0xC8, max_length=0x28,
                            id=f'CharaAbility.csv:{category},{i},name')
        encode_section_text(section, artes[i]['description'], 0x40 + i * 0xC8, max_length=0x89,
                            id=f'CharaAbility.csv:{category},{i},description')

def insert_artes(binary, artes):
    newbinary = read_dat_header(binary)
    sections = [bytearray(section) for section in read_sections(binary)]
    for i in range(0, len(sections)):
        if i in artes:
            write_artes(i, sections[i], artes[i])
            newbinary = append_section(newbinary, sections[i])
            print(artes)
    assert(len(binary) == len(newbinary))
    return newbinary

def recompile_chara_ability(l7cdir, csvdir, outputdir):
    items = read_artes_csv(csvdir)
    with open(l7cdir / '_Data/System/CharaAbility.dat', 'rb') as f:
        binary = f.read()
    binary = insert_artes(binary, items)
    outputdir = outputdir / '_Data/System'
    outputdir.mkdir(parents=True, exist_ok=True)
    with open(outputdir / 'CharaAbility.dat', 'wb') as f:
        f.write(binary)




#####################################################TEST
#def recompile_chara_ability(l7cdir, csvdir, outputdir):
##open the csv
#    with open(csvdir / 'CharaAbility.csv', 'r', encoding='utf-8', newline='') as f:
#        abilites = read_csv_data(f, 'iss', ['index', 'field', 'English'])
#
##open the dat        
#    with open(l7cdir / '_Data/System/CharaAbility.dat', 'rb') as f:
#        binary = f.read()
#    dat = DatFile(io.BytesIO(binary))
#        
##read the csv and insert in dat        
#    section = bytearray(dat.sections[1])
#    for i, ability in abilites.items():
#        encode_section_text(section, ability[i], 0x17 + i * 0xC8, max_length=0x28, id=f'CharaAbility.csv:{i}.name')
#        encode_section_text(section, ability[i], 0x40 + i * 0xC8, max_length=0x80, id=f'CharaAbility.csv:{i}.description')
#    dat.sections[1] = section    
# 
# #save the dat                               
#    dat.save_to_file(outputdir / '_Data/System/CharaAbility.dat')
#


#        encode_section_text(section, artes[i]['name'], start + 0x24, max_length=0x28, id=f'CharaAbility.csv:{category},{i},name')
#        encode_section_text(section, artes[i]['description'], start + 0x4D, max_length=0x90, id=f'CharaAbility.csv:{category},{i},description'


#chatgpt
#def _recompile_chara_abilities(abilities):
#   count = len(abilities)
#   binary = struct.pack('<L', count)
#   for i in range(count):
#       ability = abilities[i]
#       binary += encode_text(ability['name'], 0x17 + i * 0xC8)
#       binary += encode_text(ability['description'], 0x40 + i * 0xC8)
#   return binary
#
#def recompile_chara_ability(l7cdir, csvdir, outputdir):
#   abilities = {}
#   with open(csvdir / 'CharaAbility.csv', 'r', encoding='utf-8', newline='') as f:    
#       reader = csv.DictReader(f)
#       for row in reader:
#           i = int(row['index'])
#           if i not in abilities:
#               abilities[i] = {
#                   'name': '',
#                   'description': '',
#               }
#           abilities[i][row['field']] = row['English']
#   binary = _recompile_chara_abilities(abilities)
#   with open(l7cdir / '_Data/System/CharaAbility.dat', 'wb') as f:
#       f.write(binary)