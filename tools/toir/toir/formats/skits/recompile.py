from .skit import Skit, SkitLine, SkitLineAddition, SkitChoices, skit_replace_text
import csv

def _read_skits(csvdir):
    skits = {}
    with open(csvdir / 'Skit.csv', 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            path = row['File']
            field = row['Field']
            index = int(row['Index'])
            text = row['English']

            if path not in skits:
                skits[path] = {}
                skits[path]['index'] = -1
                skits[path]['title'] = ''
                skits[path]['lines'] = {}
                skits[path]['line_speakers'] = {}
                skits[path]['line_additions'] = {}
                skits[path]['choices'] = {}
                skits[path]['indices'] = set()
                skits[path]['speakers'] = {}

            skit = skits[path]
            try:
                if field == 'speaker':
                    skit['speakers'][index] = text
                elif field == 'title':
                    skit['title'] = text
                    skit['index'] = index
                elif field == 'line':
                    skit['lines'][index] = text
                    skit['indices'].add(index)
                elif field == 'line_speaker':
                    skit['line_speakers'][index] = text
                    #skit['indices'].add(index)
                elif field == 'line_addition':
                    skit['line_additions'][index] = text
                    skit['indices'].add(index)
                elif field == 'choice':
                    if index not in skit['choices']:
                        skit['choices'][index] = {}
                    skit['choices'][index][int(row['Speakers'])] = text
                    skit['indices'].add(index)
            except Exception as e:
                print(path, field, index)
                raise e

    new_skits = {}
    for path, skit in skits.items():
        try:
            speakers = [skit['speakers'][i] for i in sorted(skit['speakers'])]
            new_skit = Skit(skit['index'], skit['title'], speakers)
        except Exception as e:
            print(path)
            raise e
        for i in sorted(skit['indices']):
            if i in skit['lines']:
                speaker = None if i not in skit['line_speakers'] else skit['line_speakers'][i]
                new_line = SkitLine(i, [], skit['lines'][i], speaker)
            elif i in skit['line_additions']:
                new_line = SkitLineAddition(i, skit['line_additions'][i])
            elif i in skit['choices']:
                #print(path, i, sorted(skit['choices']))
                choices = [skit['choices'][i][j] for j in sorted(skit['choices'][i])]
                new_line = SkitChoices(i, choices)
            else:
                assert(False)
            new_skit.lines.append(new_line)
        new_skits[path] = new_skit

    return new_skits

def recompile_skits(l7cdir, csvdir, outputdir):
    skits = _read_skits(csvdir)
    datadir = outputdir / '_Data/Field/Skit/Data'
    datadir.mkdir(parents=True, exist_ok=True)
    for file, skit in skits.items():
        #print(file, skit.title, [line.index for line in skit.lines])
        with open(l7cdir / f'_Data/Field/Skit/Data/{file}', 'rb') as f:
            dat = f.read()
        try:
            dat = skit_replace_text(dat, skit)
        except Exception as e:
            print(file, skit.title, [line.text for line in skit.lines])
            raise e
        with open(datadir / file, 'wb') as f:
            f.write(dat)