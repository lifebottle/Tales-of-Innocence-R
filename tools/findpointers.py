import struct
import csv

strings = {}
with open('strings_ghidra.csv', 'r', encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f, ['location', 'value'])
    for row in reader:
        strings[int(row['location'], 16)] = {
            'value': row['value'],
            'refs': [],
        }

def look_for_string(location):
    if location in strings:
        return strings[location]

with open('boot.elf', 'rb') as f:
    eboot = f.read()

# THUMB instructions
for i in range(0x1000, 0x170000, 2):
    hw1, hw2 = struct.unpack_from('<HH', eboot, i)
    if (hw1 & 0b1111101111110000) == 0b1111001001000000 and hw2 & 0x8000 == 0:
        rdw = (hw2 >> 8) & 0xf
        immw = ((hw1 & 0xf) << 12) + ((hw1 & 0x400) << 1) + ((hw2 & 0x7000) >> 4) + (hw2 & 0xff)
        for j in range(i + 4, i + 20, 2):
            hw1, hw2 = struct.unpack_from('<HH', eboot, j)
            if (hw1 & 0b1111101111110000) == 0b1111001011000000 and hw2 & 0x8000 == 0:
                rdt = (hw2 >> 8) & 0xf
                if rdt == rdw:
                    immt = ((hw1 & 0xf) << 12) + ((hw1 & 0x400) << 1) + ((hw2 & 0x7000) >> 4) + (hw2 & 0xff)
                    string = look_for_string((immt << 16) + immw)
                    if string:
                        string['refs'].append((i + 0x80FFF000, j + 0x80FFF000))

"""
# ARM instructions
for i in range(0x1000, 0x170000, 4):
    w, = struct.unpack_from('<L', eboot, i)
    if (w & 0x0ff00000) == 0x03000000:
        print(hex(i + 0x80FFF000))
        rdw = (w >> 12) & 0xf
        immw = ((w & 0xf0000) >> 4) + (w & 0xfff)
        for j in range(i + 4, i + 20, 4):
            w, = struct.unpack_from('<L', eboot, j)
            if (w & 0x0ff00000) == 0x03400000:
                rdt = (w >> 12) & 0xf
                if rdt == rdw:
                    immt = ((w & 0xf0000) >> 4) + (w & 0xfff)
                    target = (immt << 16) + immw
                    string = look_for_string(target)
                    if string:
                        string['refs'].append((i + 0x80FFF000, j + 0x80FFF000))
"""

with open('embeddedptrs.py', 'w') as f:
    f.write('EMBEDDED_POINTERS = [\n')
    for target, string in strings.items():
        if string['refs']:
            f.write(f'    (0x{target:08X}, [\n')
            for ref in string['refs']:
                f.write(f'        (0x{ref[0]:08X}, 0x{ref[1]:08X}),\n')
            f.write('     ]),\n')
        else:
            print(f'not referenced by embedded pointer: {target:08X} {string["value"]}')
    f.write(']\n')
