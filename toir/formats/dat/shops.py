from .datfile import DatFile
from ...text import decode_text, remove_redundant_cc
from ...csvhelper import write_csv_data, read_csv_data, read_csv_file
import struct
import io
from .sections import *


def _extract_shops(f):
    dat = DatFile(f)
    names = {}
    for i in range(dat.count):        
        section = dat.read_section(i)
        names[i] = decode_text(section, 4)
    return names

def extract_shops(l7cdir, outputdir):
    with open(l7cdir / '_Data/System/ShopDataPack.dat', 'rb') as f:
        shops = _extract_shops(f)
    with open(outputdir / 'ShopDataPack.csv', 'w', encoding='utf-8', newline='') as f:
        write_csv_data(f, 'is', ['index', 'japanese'], shops)


#ef recompile_shop_names(l7cdir, csvdir, outputdir):
#   with open(csvdir / 'ShopNames.csv', 'r', encoding='utf-8', newline='') as f:
#       shops = read_csv_data(f, 'is', ['#', 'English'])
#      
#   with open(l7cdir / '_Data/System/ShopDataPack.dat', 'rb') as f:
#       binary = f.read()
#   dat = DatFile(io.BytesIO(binary))
#       
#   section = bytearray(dat.sections[1])
#   for i, shop in shops.items():
#       encode_section_text(section, shop, 4, max_length=0x2C, id=f'ShopNames.csv:{i}')
#   section = bytearray(dat.sections[1])    
##save the dat                               
#   dat.save_to_file(outputdir / '_Data/System/ShopDataPack.dat')

#################################################
def read_shops_csv(csvdir):
    with open(csvdir / 'ShopNames.csv', 'r', encoding='utf-8', newline='') as f:
        shops = read_csv_data(f, 'is', ['#', 'English'])
    return shops

def write_shops(section, shops):
    #count, = struct.unpack_from('<L', section, 0)
    for i in range(36):
        encode_section_text(section, shops, 4, max_length=0x2C, id=f'ShopNames.csv:{i}')

def insert_shops(binary, shops):
    newbinary = read_dat_header(binary)
    sections = [bytearray(section) for section in read_sections(binary)]
    for i in range(0, len(sections)):
        write_shops(sections, shops[i])
        newbinary = append_section(newbinary, sections[i])
    assert(len(binary) == len(newbinary))
    return newbinary

def recompile_shop_names(l7cdir, csvdir, outputdir):
    shops = read_shops_csv(csvdir)
    with open(l7cdir / '_Data/System/ShopDataPack.dat', 'rb') as f:
        binary = f.read()
    binary = insert_shops(binary, shops)
    outputdir = outputdir / '_Data/System'
    outputdir.mkdir(parents=True, exist_ok=True)
    with open(outputdir / 'ShopDataPack.dat', 'wb') as f:
        f.write(binary)