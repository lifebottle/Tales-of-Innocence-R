import struct
from ...text import encode_text

def read_sections(binary):
    count, = struct.unpack_from('<L', binary, 0)
    sections = []
    for i in range(count):
        offset, size = struct.unpack_from('<LL', binary, 0x10 + i * 8)
        sections.append(binary[offset:offset+size])
    return sections

def read_dat_header(binary):
    first_offset, = struct.unpack_from('<L', binary, 0x10)
    return binary[:first_offset]

#def read_dat_header(binary):
#    first_offset, = struct.unpack_from('<L', binary, 0x00)
#    return binary[:first_offset]


def append_section(dest, section):
    if len(dest) % 16 != 0:
        dest += bytes(16 - len(dest) % 16)
    dest += section
    return dest

def encode_section_text(section, text, offset, max_length, id):
    encoded = encode_text(text)
    if len(encoded) > max_length:
        print(f'"{id}" is too long ({max_length} bytes allowed), truncating...')
        encoded = encoded[:max_length - 1] # one less for trailing zero
    encoded += bytes(max_length - len(encoded))
    section[offset:offset+max_length] = encoded

