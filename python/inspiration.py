import struct

with open('boot.elf', 'rb') as f:
    binary = f.read()

start = 0x175B10
end = 0x175B18

for offset in range(start, end, 4):
    dest, = struct.unpack_from('<L', binary, offset)
    dest -= 0x80FFF000
    end_dest = dest
    while binary[end_dest] != 0:
        end_dest += 1
    print(binary[dest:end_dest].decode('utf-8'))
