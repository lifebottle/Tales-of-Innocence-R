from .datfile import DatFile
from ...text import decode_text, remove_redundant_cc
from ...csvhelper import write_csv_data
import struct

def _extract_shops(f):
    dat = DatFile(f)
    names = {}
    for i in range(dat.count):        
        section = dat.read_section(i)
        names[i] = decode_text(section, 4)
    return names

def extract_shops(l7cdir, outputdir):
    with open(l7cdir / '_Data/System/ShopDataPack.dat', 'rb') as f:
        styles = _extract_shops(f)
    with open(outputdir / 'ShopDataPack.csv', 'w', encoding='utf-8', newline='') as f:
        write_csv_data(f, 'is', ['index', 'japanese'], styles)
