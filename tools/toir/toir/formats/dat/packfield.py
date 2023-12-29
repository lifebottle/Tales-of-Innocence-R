from .sections import encode_section_text
from .datfile import DatFile
import struct
import io
from ...text import decode_text
from ...csvhelper import read_csv_data
import csv

def write_csv_data(f, format, col_names, data):
    writer = csv.DictWriter(f, col_names)
    if format[0] == 'i':
        if isinstance(data, list):
            for i, value in enumerate(data):
                writer.writerow({
                    col_names[0]: i,
                    col_names[-1]: value,
                })
        elif isinstance(data, dict):
            for i, value in data.items():
                writer.writerow({
                    col_names[0]: i,
                    col_names[-1]: value,
                })

def read_pack_field(l7cdir):#read_chara_names
    with open(l7cdir / '_Data/Field/PackFieldData.dat', 'rb') as f:
        binary = f.read()
    dat = DatFile(io.BytesIO(binary))
    
    namesdat = dat.read_section(30)
    count, = struct.unpack_from('<H', namesdat, 0)
    names = []
    for i in range(count):
        names.append(decode_text(namesdat, 2 + i * 0x24))

    section = dat.read_section(32)
    count, = struct.unpack_from('<H', section, 0)
    locations = []
    for i in range(count):
        locations.append(decode_text(section, 2 + i * 0x30))

    #added by pegi
    section = dat.read_section(33)
    count, = struct.unpack_from('<H', section, 0)
    locations2 = []
    for i in range(count):
        locations2.append(decode_text(section, 2 + i * 0x30))
    
    #added by pegi
    section = dat.read_section(34)
    count, = struct.unpack_from('<H', section, 0)
    locations3 = []
    for i in range(count):
        locations3.append(decode_text(section, 2 + i * 0x30))  

    section = dat.read_section(36)
    count, = struct.unpack_from('<H', section, 0)
    movie = []
    for i in range(count):
        movie.append(decode_text(section, 2 + i * 0x50)) 
    
    section = dat.read_section(37)
    count, = struct.unpack_from('<H', section, 0)
    skits = []
    for i in range(count):
        file_index = struct.unpack_from('<H', section, i * 0x74 + 0x12)
        skits.append((file_index, decode_text(section, i * 0x74 + 0x14)))
    return names, locations, locations2, locations3, movie, skits

def extract_pack_field(l7cdir, outputdir):
    names, locations, locations2, locations3, movie, skits = read_pack_field(l7cdir)
    
    with open(outputdir / 'CharaNames.csv', 'w', encoding='utf-8', newline='') as f:
        write_csv_data(f, 'i', ['index', 'japanese'], names)
        
    with open(outputdir / 'Locations.csv', 'w', encoding='utf-8', newline='') as f:
        write_csv_data(f, 'i', ['index', 'japanese'], locations)
        
    with open(outputdir / 'Locations2.csv', 'w', encoding='utf-8', newline='') as f:
        write_csv_data(f, 'i', ['index', 'japanese'], locations2)
        
    with open(outputdir / 'Locations3.csv', 'w', encoding='utf-8', newline='') as f:
        write_csv_data(f, 'i', ['index', 'japanese'], locations3)
        
    with open(outputdir / 'Movies.csv', 'w', encoding='utf-8', newline='') as f:
        write_csv_data(f, 'i', ['index', 'japanese'], movie)      
        
    with open(outputdir / 'SkitNames.csv', 'w', encoding='utf-8', newline='') as f:
        write_csv_data(f, 'i', ['index', 'japanese'], skits)

def recompile_pack_field(l7cdir, csvdir, outputdir):
#open the csv
    with open(csvdir / 'CharaNames.csv', 'r', encoding='utf-8', newline='') as f:
        chara_names = read_csv_data(f, 'is', ['#', 'English'])
        
    with open(csvdir / 'Locations.csv', 'r', encoding='utf-8', newline='') as f:
        locations = read_csv_data(f, 'is', ['#', 'English'])
        
    with open(csvdir / 'Locations2.csv', 'r', encoding='utf-8', newline='') as f:
        locations2 = read_csv_data(f, 'is', ['#', 'English'])
        
    with open(csvdir / 'Locations3.csv', 'r', encoding='utf-8', newline='') as f:
        locations3 = read_csv_data(f, 'is', ['#', 'English'])
        
    with open(csvdir / 'Movie.csv', 'r', encoding='utf-8', newline='') as f:
        movies = read_csv_data(f, 'is', ['#', 'English'])
        
    with open(csvdir / 'SkitNames.csv', 'r', encoding='utf-8', newline='') as f:
        skit_names = read_csv_data(f, 'is', ['#', 'English'])      

#open the original dat
    with open(l7cdir / '_Data/Field/PackFieldData.dat', 'rb') as f:
        binary = f.read()
    dat = DatFile(io.BytesIO(binary))

#read the csv and insert in dat
    section = bytearray(dat.read_section(30))
    for i, name in chara_names.items():
        encode_section_text(section, name, 2 + i * 0x24, max_length=0x20, id=f'CharaNames.csv:{i}')
    dat.sections[30].blob = section
    
    section = bytearray(dat.read_section(32))
    for i, location in locations.items():
        encode_section_text(section, location, 2 + i * 0x30, max_length=0x28, id=f'Locations.csv:{i}')
    dat.sections[32].blob = section
    
    section = bytearray(dat.read_section(33))
    for i, location2 in locations2.items():
        encode_section_text(section, location2, 2 + i * 0x30, max_length=0x30, id=f'Locations2.csv:{i}')
    dat.sections[33].blob = section
    
    section = bytearray(dat.read_section(34))
    for i, location3 in locations3.items():
        encode_section_text(section, location3, 2 + i * 0x30, max_length=0x28, id=f'Locations3.csv:{i}')
    dat.sections[34].blob = section
    
    section = bytearray(dat.read_section(36))
    for i, movie in movies.items():
        encode_section_text(section, movie, 2 + i * 0x50, max_length=0x28, id=f'Movie.csv:{i}')
    dat.sections[36].blob = section
    
    section = bytearray(dat.read_section(37))
    for i, skit in skit_names.items():
        encode_section_text(section, skit, i * 0x74 + 0x14, max_length=0x36, id=f'SkitNames.csv:{i}')
    dat.sections[37].blob = section
    
#save the dat in new location and align 16 for some reason 
    outputfile = outputdir / '_Data/Field/PackFieldData.dat'
    outputfile.parent.mkdir(parents=True, exist_ok=True)
    with open(outputfile, 'wb') as f:
        dat.save(f)
