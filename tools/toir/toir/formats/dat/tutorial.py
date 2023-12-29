from .datfile import DatFile
from ...text import decode_text, remove_redundant_cc
from ...csvhelper import write_csv_data
from ...lib_lifebottle import *
import struct
import pandas as pd
import shutil

def _extract_tutorial_text(f):
    dat = DatFile(f)
    tutorial = {}
    for i in range(dat.count):
        section = dat.read_section(i)
        count, = struct.unpack_from('<L', section, 0)
        tutorial[i] = [remove_redundant_cc(decode_text(section, 4 + 0x106 * j))
                        for j in range(count)]
    return tutorial

def extract_tutorial(l7cdir, outputdir):
    with open(l7cdir / '_Data/Battle/TutorialData.dat', 'rb') as f:
        items = _extract_tutorial_text(f)
    with open(outputdir / 'TutorialData.csv', 'w', encoding='utf-8', newline='') as f:
        write_csv_data(f, 'iis', ['section', 'index', 'japanese'], items)

def read_tutorial_csv(path:str):
  columns = ['StructId', 'LineNumber', 'Jap', 'Eng']
  df_translations = pd.read_csv(path, delimiter=',', encoding='utf-8')
  df_translations.columns = columns
  df_translations['StructId'] = df_translations['StructId'].astype(int)
  df_translations['Eng'].fillna('', inplace=True)
  return df_translations

def insert_tutorial(file_path:str, df_translations):
  

  with open(file_path, 'rb+') as f:
      
    #Read nb of structs
    nb_structs = read_u32(f)
    struct_offsets = [] 
    struct_infos = []

    #Store all the strucs offsets in a list
    f.seek(0x10)
    for _ in range(nb_structs):
      offset = read_u32(f)
      struct_offsets.append(offset)
      f.read(4)


    for struct_id, struct_offset in enumerate(struct_offsets):
      f.seek(struct_offset)
      f.read(4)
      df_struct = df_translations[df_translations['StructId'] == struct_id]['Eng']

      line_offset = f.tell()
      for line_number, line_english in enumerate(df_struct):
         
        #Write Line Number and Line text
        f.seek(line_offset)
        line_bytes = text_to_bytes(text=line_english)
        f.write(line_bytes)
        rest = 0xF6 - len(line_bytes)
        f.write(b'\x00' * rest)
        line_offset += 0x106


def recompile_tutorial(l7cdir, csvdir, outputdir):
    df_translations = read_tutorial_csv(csvdir / 'TutorialGame.csv')
    end = '_Data/Battle/TutorialData.dat'
    original_path = l7cdir / end
    final_path = outputdir / end
    final_path.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy(original_path, final_path)
    insert_tutorial(final_path, df_translations)
    