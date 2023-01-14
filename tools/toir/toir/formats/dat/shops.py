from .datfile import DatFile
from ...text import decode_text, remove_redundant_cc
from ...csvhelper import write_csv_data, read_csv_data
import struct
import io
from .sections import encode_section_text

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

#need to modify the variables names
def recompile_shop_names(l7cdir, csvdir, outputdir):
#open the csv
    with open(csvdir / 'ShopNames.csv', 'r', encoding='utf-8', newline='') as f:
        shops = read_csv_data(f, 'is', ['#', 'English'])

#open the dat        
    with open(l7cdir / '_Data/System/ShopDataPack.dat', 'rb') as f:
        binary = f.read()
    dat = DatFile(io.BytesIO(binary))
        
#read the csv and insert in dat    0x90 of space between entries #max_lenght=0x2C   
    section = bytearray(dat.sections[1])
    for i, shop in shops.items():
        encode_section_text(section, shop, 4, max_length=0x2C, id=f'ShopNames.csv:{i}')
    section = bytearray(dat.sections[1])    
 
 #save the dat                               
    dat.save_to_file(outputdir / '_Data/System/ShopDataPack.dat')