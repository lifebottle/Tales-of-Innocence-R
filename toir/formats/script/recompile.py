from .script import Script, OffsetSizeMismatchError, UnknownOpcodeError
import csv

def _read_story(csvdir):
    story = {}
    with open(csvdir / 'Story.csv', 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            file = row['File']
            if file not in story:
                story[file] = {}
            translation = row['English']

            if '/' in row['#']:
                index, subindex = row['#'].split('/')
                index, subindex = int(index), int(subindex)
                if index not in story[file]:
                    story[file][index] = {}
                story[file][index][subindex] = translation
            else:
                story[file][int(row['#'])] = translation
           
    return story

def recompile_story(l7cdir, csvdir, outputdir, check_integrity=False):
    story = _read_story(csvdir)
    for file, lines in story.items():
        with open(l7cdir / f'_Data/Script/{file}', 'rb') as f:
            dat = f.read()
        script = Script.decompile(dat)
        script.replace_texts(lines)
        new_dat = script.recompile()
        if check_integrity:
            try:
                _ = Script.decompile(new_dat)
            except Exception as e:
                with open('story_error.txt', 'w', encoding='utf-8') as f:
                    script.dump(f)
                    if isinstance(e, OffsetSizeMismatchError) or isinstance(e, UnknownOpcodeError):
                        e.script.dump(f)
                raise e
        output = outputdir / '_Data/Script' / file
        datadir = output.parent
        datadir.mkdir(parents=True, exist_ok=True)
        with open(output, 'wb') as f:
            f.write(new_dat)
