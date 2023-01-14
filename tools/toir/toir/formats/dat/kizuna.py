from .datfile import DatFile
from ...text import decode_text, remove_redundant_cc
from ...csvhelper import write_csv_data
import struct

def _extract_kizuna(f):
    dat = DatFile(f)
    kizuna = {}
    for i in range(dat.count):
        section = dat.read_section(i)
        count = 80
        kizuna[i] = [decode_text(section, 0x31 * j) for j in range(count)]
    return kizuna

def extract_kizuna(l7cdir, outputdir):
    with open(l7cdir / '_Data/System/KizunaDataPack.dat', 'rb') as f:
        kizuna = _extract_kizuna(f)
    with open(outputdir / 'KizunaDataPack.csv', 'w', encoding='utf-8', newline='') as f:
        write_csv_data(f, 'iis', ['category', 'index', 'japanese'], kizuna)
