from ..script.script import Script, DecompilationException, TextWithSpeaker
from .. import DatFile, read_pack_field
import io
import csv

def _extract_text(binary, id):
    try:
        script = Script.decompile(binary)
    except DecompilationException as e:
        print(f'MapData: error while decompiling {id}: {e}')
        with open(f'error.scr', 'w', encoding='utf-8') as f:
            e.script.dump(f)
        raise e
    except Exception as e:
        print(f'MapData: unknown error while decompiling {id}: {e}')
        raise e
    return script.collect_texts()

def _extract_dat(file):
    dat = DatFile(file.open('rb'))
    texts = {}
    if dat.sections[0].size > 0:
        section = io.BytesIO(dat.read_section(0))
        try:
            subdat = DatFile(section)
        except:
            print(f'Warning: {file} apparently has no script')
            return texts

        #if not (0xb <= dat.count <= 0xc):
            #print(file, dat.count)

        for i in range(subdat.count - 1):
            text = _extract_text(subdat.read_section(i), id=f'{file},{i}')
            if text:
                texts[i] = text
    return texts

def write_to_csv(script, outputdir):
    with open(outputdir / 'MapData.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, ['path', 'section', 'id', 'speaker', 'text'])
        for location, texts in script.items():
            for i, text in texts.items():
                for id, line in text.items():
                    writer.writerow({
                        'path': location,
                        'section': i,
                        'id': id,
                        'speaker': line.speaker if line.speaker else '',
                        'text': line.text,
                    })

def extract_dats(l7cdir):
    locations = {}
    files = l7cdir.glob('_Data/Field/MapData/*/*/*.dat')
    for file in files:
        if 'NaviMap' in file.name:
            continue
        texts = _extract_dat(file)
        if texts:
            path = file.relative_to(l7cdir / '_Data/Field/MapData')
            locations['/'.join(path.parts)] = texts
    return locations

def replace_speakers(l7cdir, script):
    names = read_pack_field(l7cdir)[0]
    for _, texts in script.items():
        for i, text in texts.items():
            for id, line in text.items():
                if line.speaker:
                    text[id] = TextWithSpeaker(names[line.speaker], line.text)

def extract_map_data(l7cdir, outputdir):
    script = extract_dats(l7cdir)
    replace_speakers(l7cdir, script)
    write_to_csv(script, outputdir)
