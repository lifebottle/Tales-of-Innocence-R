from .skit import SkitLineAddition, skit_extract_text, SkitLine, SkitChoices
from ..dat.datfile import DatFile
from ...text import decode_text
import csv
import struct
import io

def split_speakers(speakers):
    split = []
    for i in range(0, 16):
        if (speakers & (1 << i)) != 0:
            split.append(i)
    return split
    #return ','.join(split)

def extract_skit_names(l7cdir):
    with open(l7cdir / '_Data/Field/Test/PackFieldData.dat', 'rb') as f:
        binary = f.read()
    dat = DatFile(io.BytesIO(binary))
    section = dat.read_section(37)
    count, = struct.unpack_from('<H', section, 0)
    skits = {}
    for i in range(count):
        file_index, = struct.unpack_from('<H', section, i * 0x74 + 0x12)
        skits[file_index] = (i, decode_text(section, i * 0x74 + 0x14))
    return skits

def extract_skits(l7cdir, outputdir):
    skit_names = 1 #extract_skit_names(l7cdir)

    skits = {}
    for file in l7cdir.glob('_Data/Field/Skit/Data/Test/*.dat'):
        with file.open('rb') as f:
            binary = f.read()
            path = file.relative_to(l7cdir / '_Data/Field/Skit/Data/Test')
            try:
                skits['/'.join(path.parts)] = skit_extract_text(binary)
            except Exception as e:
                print(file)
                raise e

    with open(outputdir / 'Skit.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['R', 'File', 'Field', 'Index', 'Speakers', 'Japanese'])
        r, c = 0, 0
        rows = []
        for path, text in skits.items():
            # write title
            index = int(path[0:4])
            if index in skit_names:                
                writer.writerow([r, path, 'title', skit_names[index][0], '', skit_names[index][1]])
                r += 10
            # write speakers
            for i, speaker in enumerate(text[0]):
                writer.writerow([r, path, 'speaker', i, '', speaker])
                r += 10
            # write content
            for i, line in enumerate(text[1]):
                if isinstance(line, SkitLine):
                    if line.speakerName:
                        writer.writerow([r, path, 'line_speaker', line.index, '', line.speakerName])
                        r += 10
                    speakers = split_speakers(line.speakers)
                    speakers = '\n'.join(f'{i} [{text[0][i]}]' for i in speakers)
                    writer.writerow([r, path, 'line', line.index, speakers, line.text])
                    r += 10
                    c = 0
                elif isinstance(line, SkitChoices):                    
                    for j, choice in enumerate(line.choices):
                        writer.writerow([r, path, 'choice', line.index, j, choice])                        
                        r += 10
                    c = 0
                elif isinstance(line, SkitLineAddition):
                    rows.append([r + c - 9, path, 'line_addition', line.index, '', line.text])
                    c += 1
        for row in rows:
            writer.writerow(row)
