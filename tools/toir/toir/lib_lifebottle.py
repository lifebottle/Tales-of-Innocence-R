import struct
import re
import string
COMMON_TAG = r"(\{[\w/]+:?\w+\})"
HEX_TAG = r"(\{[0-9A-F]{2}\})"
PRINTABLE_CHARS = "".join(
            (string.digits, string.ascii_letters, string.punctuation, " ")
        )

tags = {
    "Code": {
      "icon":"404040",
      "button":"404040",
      "unknown41":"404140",
      "control41":"404140",
      "color":"4001"
    },
    "Color": {
      "red": "4001",
      "cyan": "4002",
      "blue": "4003",
      "white": "4004" 
      
    }
}

def read_u16(f):
   return struct.unpack('<H', f.read(2))[0]


def read_u32(f):
   return struct.unpack('<I', f.read(4))[0]

def write_u32(f, value:int):
   f.write(struct.pack('<I', value))

def write_u16(f, value:int):
   f.write(struct.pack('<H', value))
   
def write_u8(f, value:int):
   f.write(struct.pack('<B', value))

def text_to_bytes(text:str):

  multi_regex = (HEX_TAG + "|" + COMMON_TAG + r"|(\n)")
  tokens = [sh for sh in re.split(multi_regex, text) if sh]
  
  output = b''
  if text != '' and text != 'nan':
    for t in tokens:
        # Hex literals
        if re.match(HEX_TAG, t):
            output += struct.pack("B", int(t[1:3], 16))
        
        elif t.count(':') >= 2:
          print(f'Warning double :: in a string is found, please update tags in {text}')
        # Tags
        elif re.match(COMMON_TAG, t):
            tag, param, *_ = t[1:-1].split(":") + [None]
            tag = tag.lower()

            #Handle cases like <icon:0CBD>
            if tag in tags['Code']:
              #print(f'Tag found: {tag} with val: {param}')
              #Convert tag from dictionnary 4001 to b\x40\x01
              #Uses big endian
              byte_tag = bytes.fromhex(tags['Code'][tag])
              param_padded = ''

              if tag in ['icon', 'button', 'color']:
                param_padded = '0' * (4 - len(param)) + param

              elif tag in ['control41', 'unknown41']:
                param_padded = '0' * (2 - len(param)) + param
                
              #Convert C3D tb 0C3D to b'\x3D\x0C'
              #[::-1] will reverse the bytes for little endian
              byte_param = bytes.fromhex(param_padded)[::-1]
              output += byte_tag + byte_param

              
            #Handle cases like <Red>
            elif tag in tags['Color']:
              bytes_color = bytes.fromhex(tags['Code']['color']) + bytes.fromhex(tags['Color'][tag])
              output += bytes_color
              
              
            else:
              print(f'Warning case not handled: tag: {tag}')

        # Actual text
        elif t == "\n":
            output += b"\x0D\x0A"

        elif t != "\r":
            for c in t:
                output += c.encode("utf-8")
       
  return output