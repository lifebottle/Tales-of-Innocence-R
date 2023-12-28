from .sections import read_sections
import struct
from ...text import decode_text
from ...lib_lifebottle import *
import csv
import pandas as pd
import shutil

LINE_SIZE = 0x81
TITLE_SIZE = 0x2A
STRUCT_SIZE = 0x4D0
STRUCT_PAD = 16
STRUCT_MAX_LINE = 9

def read_battle_book(section):
    count, = struct.unpack_from('<L', section, 0)
    title = decode_text(section, 4);
    text = []
    for i in range(count):
        text.append(decode_text(section, 0x30 + 0x83 * i))
    return title, text

def _extract_battle_book(binary):
    battle_book = {}
    sections = read_sections(binary)
    for i in range(0, len(sections)):
        battle_book[i] = read_battle_book(sections[i])
    return battle_book

def extract_battle_book(l7cdir, outputdir):
    with open(l7cdir / '_Data/System/BattleBookDataPack.dat', 'rb') as f:
        binary = f.read()
    items = _extract_battle_book(binary)
    with open(outputdir / 'BattleBookDataPack.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, ['category', 'field', 'index', 'text'])
        for category, entry in items.items():
            writer.writerow({
                'category': category,
                'field': 'title',
                'index': '',
                'text': entry[0],
            })
            for i, text in enumerate(entry[1]):
                writer.writerow({
                    'category': category,
                    'field': 'text',
                    'index': i,
                    'text': text,
                })




def read_battlebook_csv(path:str):
  columns = ['StructId', 'Type', 'LineNumber', 'Jap', 'Eng']
  df_translations = pd.read_csv(path, delimiter=',', encoding='utf-8')
  df_translations.columns = columns
  df_translations['StructId'] = df_translations['StructId'].astype(int)
  df_translations['Eng'] = df_translations['Eng'].str.replace('<', '{')
  df_translations['Eng'] = df_translations['Eng'].str.replace('>', '}')
  df_translations['Eng'].fillna('', inplace=True)
  return df_translations

def insert_battlebook(file_path:str, df_translations):
  

  with open(file_path, 'rb+') as f:
      
    #Read nb of structs
    nb_structs = read_u32(f)
    struct_offsets = [] 
    struct_infos = []

    #Store all the strucs offsets in a list
    #f.seek(0x10)
    #for _ in range(nb_structs):
    #  offset = read_u32(f)
    #  struct_offsets.append(offset)
    #  f.read(4)

    f.seek(0x10)
    start_struct = read_u32(f)
    f.seek(start_struct)
    for struct_id in range(nb_structs):
      
      df_struct = df_translations[df_translations['StructId'] == struct_id]

      #Write Lines number
      nb_lines = int(df_struct['LineNumber'].max() + 1)
      write_u32(f,nb_lines)

      #Write Title
      title_row = df_struct[df_struct['Type'] == 'title']
      title_english = title_row['Eng'].tolist()[0]
      title_bytes = text_to_bytes(text=title_english)
      f.write(title_bytes)

      #Pad with 00 until Title max size
      rest = TITLE_SIZE - len(title_bytes)
      f.write(b'\x00' * rest)

      #Look for all the lines in the struct
      df_lines = df_struct[df_struct['Type'] == 'text']['Eng']
      for line_number, line_english in enumerate(df_lines):
         
        #Write Line Number and Line text
        write_u16(f, line_number)
        line_bytes = text_to_bytes(text=line_english)
        f.write(line_bytes)
        rest = 0x81 - len(line_bytes)
        f.write(b'\x00' * rest)

      #Add new size to the list
      
      struct_size = f.tell() - start_struct - 1
      struct_infos.append((start_struct, struct_size))
      #print(f'Struct id: {struct_id} ..............')
      #print(f'Struct Start offset: {hex(start_struct)}')
      #print(f'Struct size: {hex(struct_size)}')
      #print(f'Struct End offset: {hex(f.tell())}\n')

      

      #Pad end of struct at 16
      rest = 16 - f.tell() % 16
      f.write(b'\x00' * rest)

      start_struct = f.tell()
  
    #Update all the struct sizes in the table
    f.seek(0x10)
    for start_offset, new_size in struct_infos:
       write_u32(f, start_offset)
       write_u32(f, new_size)



def recompile_battlebook(l7cdir, csvdir, outputdir):
    df_translations = read_battlebook_csv(csvdir / 'Battlebook.csv')
    end = '_Data/System/BattleBookDataPack.dat'
    original_path = l7cdir / end
    final_path = outputdir / end
    final_path.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy(original_path, final_path)
    insert_battlebook(final_path, df_translations)
    
