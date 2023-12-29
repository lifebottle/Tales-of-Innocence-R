from .sections import *
from .datfile import DatFile
from ...text import decode_text, remove_redundant_cc
from ...csvhelper import *
from ...lib_lifebottle import *
import struct
import pandas as pd
import shutil

def _extract_operation(f):
    dat = DatFile(f)

    section = dat.read_section(0)
    count, = struct.unpack_from('<L', section, 0)
    operation = {}
    operation[0] = [{
            'name': decode_text(section, 0x13 + 0xB2 * i),
            'description': decode_text(section, 0x24 + 0xB2 * i)
        } for i in range(count)]

    section = dat.read_section(1)
    count, = struct.unpack_from('<L', section, 0)
    operation[1] = [{
            'name': decode_text(section, 0x09 + 0xC0 * i),
            'description': decode_text(section, 0x32 + 0xC0 * i)
        } for i in range(count)]

    section = dat.read_section(3)
    count, = struct.unpack_from('<L', section, 0)
    operation[3] = [{
            'name': decode_text(section, 0x08 + 0xAF * i),
            'description': decode_text(section, 0x21 + 0xAF * i)
        } for i in range(count)]

    return operation

def extract_operation(l7cdir, outputdir):
    with open(l7cdir / '_Data/System/OperationDataPack.dat', 'rb') as f:
        operation = _extract_operation(f)
        
    with open(outputdir / 'OperationDataPack.csv', 'w', encoding='utf-8', newline='') as f:
        write_csv_data(f, 'iifs', ['category', 'index', 'field', 'japanese'], operation)

def read_operations_csv(path:str):
  columns = ['StructId', 'Line', 'Type','Jap', 'Eng']
  df_translations = pd.read_csv(path, delimiter=',', encoding='utf-8')
  df_translations.columns = columns
  df_translations['StructId'] = df_translations['StructId'].astype(int)
  df_translations['Eng'].fillna('', inplace=True)
  return df_translations

def insert_operations(file_path:str, df_translations):
  

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
    
    structs_infos = {
       0:{
          "pad_number": 0xF,
          "name_size": 0x11,
          "desc_size": 0x92
       },
       1:{
          "pad_number": 0x5,
          "name_size": 0x29,
          "desc_size": 0x92
       },
       3:{
          "pad_number": 0x4,
          "name_size": 0x19,
          "desc_size": 0x92
       }
    }
    

    for struct_id, struct_offset in enumerate(struct_offsets):
      
      if struct_id in [0,1,3]:
        f.seek(struct_offset)
        f.read(4)

        df_struct = df_translations[df_translations['StructId'] == struct_id]
        max_line = df_struct['Line'].max()+1


        for line_id in range(max_line):
            print(structs_infos[struct_id])
            f.read(structs_infos[struct_id]['pad_number'])
            df_line = df_struct[df_struct['Line'] == line_id]
                
            line_1_row = df_line[df_line['Type'] == 'name']
            line_1_english = line_1_row['Eng'].tolist()[0]
            line_1_bytes = text_to_bytes(text=line_1_english)
            f.write(line_1_bytes) 
            #Pad with 00 until Line 1 max size
            rest = structs_infos[struct_id]['name_size'] - len(line_1_bytes)
            f.write(b'\x00' * rest)  

            line_2_row = df_line[df_line['Type'] == 'description']
            line_2_english = line_2_row['Eng'].tolist()[0]
            line_2_bytes = text_to_bytes(text=line_2_english)
            f.write(line_2_bytes) 
            #Pad with 00 until Line 2 max size
            rest = structs_infos[struct_id]['desc_size'] - len(line_2_bytes)
            f.write(b'\x00' * rest)      

def recompile_operations(l7cdir, csvdir, outputdir):
    df_translations = read_operations_csv(csvdir / 'Operation.csv')
    end = '_Data/System/OperationDataPack.dat'
    original_path = l7cdir / end
    final_path = outputdir / end
    final_path.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy(original_path, final_path)
    insert_operations(final_path, df_translations)
    