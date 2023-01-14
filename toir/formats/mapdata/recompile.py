from ..script.script import Script, DecompilationException, TextWithSpeaker
import csv
import io
from ..dat import DatFile

def read_from_csv(file):
    script = {}
    with open(file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            path = row['Path']
            section = int(row['Section'])
            translation = row['English']

            if path not in script:
                script[path] = {}
            if section not in script[path]:
                script[path][section] = {}

            section = script[path][section]

            if '/' in row['#']:
                index, subindex = row['#'].split('/')
                index, subindex = int(index), int(subindex)
                if index not in section:
                    section[index] = {}
                section[index][subindex] = translation
            else:
                section[int(row['#'])] = translation

    return script

def recompile_map_data(l7cdir, csvdir, outputdir):
    script = read_from_csv(csvdir / 'MapData.csv')

    for path, sections in script.items():
        with open(l7cdir / f'_Data/Field/MapData/{path}', 'rb') as f:
            dat = DatFile(f)
            section = io.BytesIO(dat.read_section(0))
            subdat = DatFile(section)
            for section_idx, lines in sections.items():
                decompiled = Script.decompile(subdat.sections[section_idx])
                decompiled.replace_texts(lines)
                subdat.sections[section_idx] = decompiled.recompile()
            new_subdat = io.BytesIO()
            subdat.save(new_subdat)
            dat.sections[0] = new_subdat.getvalue()

        datadir = (outputdir / f'_Data/Field/MapData/{path}').parent
        datadir.mkdir(parents=True, exist_ok=True)
        with open(outputdir / f'_Data/Field/MapData/{path}', 'wb') as f:
            dat.save(f)
