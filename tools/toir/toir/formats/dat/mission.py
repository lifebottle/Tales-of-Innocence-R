from .sections import encode_section_text
from .datfile import DatFile
from ...text import decode_text, encode_text
from ...csvhelper import write_csv_data
import struct
import io
from ...csvhelper import read_csv_data
import csv
from ...lib_lifebottle import *
import struct
import pandas as pd
import shutil

def _extract_mission(f):
    binary = f.read()
    mission = {}
    count, = struct.unpack_from('<L', binary, 0)
    
    for i in range(count):
        mission[i] = {
            'line_1': decode_text(binary, 4 + i * 0xA8),
            'line_2': decode_text(binary, 4 + i * 0xA8 + 0x41),
            'target': decode_text(binary, 4 + i * 0xA8 + 0x82),
        }
    return mission
        

def extract_mission(l7cdir, outputdir):
    with open(l7cdir / '_Data/Battle/MissionData.dat', 'rb') as f:
        mission = _extract_mission(f)
    with open(outputdir / 'MissionData.csv', 'w', encoding='utf-8', newline='') as f:
        write_csv_data(f, 'ifs', ['Section', 'Type', 'Japanese'], mission)

#New Code inspired by Stewie

#New insertion with stewies method
def read_mission_csv(path:str):
  columns = ['StructId', 'Type', 'Jap', 'Eng']
  df_translations = pd.read_csv(path, delimiter=',', encoding='utf-8')
  df_translations.columns = columns
  df_translations['StructId'] = df_translations['StructId'].astype(int)
  df_translations['Eng'] = df_translations['Eng'].str.replace('<', '{')
  df_translations['Eng'] = df_translations['Eng'].str.replace('>', '}')
  df_translations['Eng'].fillna('', inplace=True)
  return df_translations
  
LINE_MAX = 0x41
TARGET_MAX = 0x22
  
def insert_mission(file_path:str, df_translations):
  

  with open(file_path, 'rb+') as f:
      
    #Read nb of structs
    nb_structs = read_u32(f)
    
    #i = 0
    f.seek(0x4)
    for i in range(nb_structs):
      #f.seek(0x4)
      #f.read(4)
      df_struct = df_translations[df_translations['StructId'] == i]
      line_1_row = df_struct[df_struct['Type'] == 'line_1']
      line_1_english = line_1_row['Eng'].tolist()[0]
      line_1_bytes = text_to_bytes(text=line_1_english)
      f.write(line_1_bytes) 
      #Pad with 00 until Line 1 max size
      rest = LINE_MAX - len(line_1_bytes)
      f.write(b'\x00' * rest)  

      line_2_row = df_struct[df_struct['Type'] == 'line_2']
      line_2_english = line_2_row['Eng'].tolist()[0]
      line_2_bytes = text_to_bytes(text=line_2_english)
      f.write(line_2_bytes) 
      #Pad with 00 until Line 2 max size
      rest = LINE_MAX - len(line_2_bytes)
      f.write(b'\x00' * rest)      
         
      target_row = df_struct[df_struct['Type'] == 'target']
      target_english = target_row['Eng'].tolist()[0]
      target_bytes = text_to_bytes(text=target_english)
      f.write(target_bytes) 
      #Pad with 00 until Target max size
      rest = TARGET_MAX - len(target_bytes)
      f.write(b'\x00' * rest)  
      f.read(0x4)
      
      
         

def recompile_mission(l7cdir, csvdir, outputdir):
    df_translations = read_mission_csv(csvdir / 'MissionData.csv')
    end = '_Data/Battle/MissionData.dat'
    original_path = l7cdir / end
    final_path = outputdir / end
    final_path.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy(original_path, final_path)
    insert_mission(final_path, df_translations)