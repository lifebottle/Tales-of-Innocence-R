from .datfile import DatFile
from ...text import decode_text, remove_redundant_cc
from ...csvhelper import write_csv_data, read_csv_data, read_csv_file
import struct
import io
from .sections import *
from ...lib_lifebottle import *
import csv
import pandas as pd
import shutil

#need to adjust them
MAX_SIZE = 0x24


def _extract_shops(f):
    dat = DatFile(f)
    names = {}
    for i in range(dat.count):        
        section = dat.read_section(i)
        names[i] = decode_text(section, 4)
    return names

def extract_shops(l7cdir, outputdir):
    with open(l7cdir / '_Data/System/ShopDataPack.dat', 'rb') as f:
        shops = _extract_shops(f)
    with open(outputdir / 'ShopDataPack.csv', 'w', encoding='utf-8', newline='') as f:
        write_csv_data(f, 'is', ['index', 'japanese'], shops)

#Insertion with Stewie's method
#need to remove type and linenumber in csv reader
def read_shopnames_csv(path:str):
  columns = ['StructId','Jap', 'Eng']
  df_translations = pd.read_csv(path, delimiter=',', encoding='utf-8')
  df_translations.columns = columns
  df_translations['StructId'] = df_translations['StructId'].astype(int)
  df_translations['Eng'] = df_translations['Eng'].str.replace('<', '{')
  df_translations['Eng'] = df_translations['Eng'].str.replace('>', '}')
  df_translations['Eng'].fillna('', inplace=True)
  return df_translations

def insert_shopname(file_path:str, df_translations):
  

  with open(file_path, 'rb+') as f:
      
    #Read nb of structs basicly the first u32 of the file
    nb_structs = read_u32(f)
    #intialize the two list for offset and size
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
      df_struct = df_translations[df_translations['StructId'] == struct_id]

      #Write Shop Name
      shopname_english = df_struct['Eng'].tolist()[0]
      shop_bytes = text_to_bytes(text=shopname_english)
      f.write(shop_bytes)

      #Pad with 00 until shop max size
      rest = MAX_SIZE - len(shop_bytes)
      f.write(b'\x00' * rest)

     

def recompile_shop_names(l7cdir, csvdir, outputdir):
    df_translations = read_shopnames_csv(csvdir / 'ShopNames.csv')
    end = '_Data/System/ShopDataPack.dat'
    original_path = l7cdir / end
    final_path = outputdir / end
    final_path.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy(original_path, final_path)
    insert_shopname(final_path, df_translations)
    