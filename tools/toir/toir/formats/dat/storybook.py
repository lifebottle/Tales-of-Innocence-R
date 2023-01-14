from .datfile import DatFile
from ...text import decode_text, remove_redundant_cc
from ...csvhelper import write_csv_data
import struct

def _extract_story_book(f):
    dat = DatFile(f)
    story_book = {}
    for i in range(dat.count):        
        story_book[i] = {}
        section = dat.read_section(i)
        count, = struct.unpack_from('<L', section, 0)
        story_book[i]['title'] = [decode_text(section, 4)]
        story_book[i]['line'] = {}
        for j in range(count):
            story_book[i]['line'][j] = decode_text(section, 0x2E + 0x61 * j)
    return story_book

def extract_story_book(l7cdir, outputdir):
    with open(l7cdir / '_Data/System/StoryBookDataPack.dat', 'rb') as f:
        story_book = _extract_story_book(f)
    with open(outputdir / 'StoryBookDataPack.csv', 'w', encoding='utf-8', newline='') as f:
        write_csv_data(f, 'ifis', ['category', 'field', 'index', 'japanese'], story_book)
