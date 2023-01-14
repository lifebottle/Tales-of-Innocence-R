import struct
from collections import namedtuple

DatSection = namedtuple('DatSection', ['offset', 'size'])

class DatFile:
    def __init__(self, f):
        self._f = f
        binary = self._f.read(16)
        self.count, = struct.unpack_from('<L', binary, 0)
        header = self._f.read(self.count * 8)
        
        self.sections = []
        for i in range(self.count):
            offset, size = struct.unpack_from('<LL', header, i * 8)
            #self.sections.append(DatSection(offset, size))
            self._f.seek(offset)
            self.sections.append(self._f.read(size))

    def read_section(self, i):
        #self._f.seek(self.sections[i].offset)
        #return self._f.read(self.sections[i].size)
        return self.sections[i]

    def save(self, f):
        header_len = 8 * len(self.sections) + 16
        header_len = (header_len + 15) & 0xfffffff0
        header = bytearray(header_len)
        struct.pack_into('<L', header, 0, len(self.sections))
        offset = header_len
        for i, section in enumerate(self.sections):
            size = (len(section) + 15) & 0xfffffff0
            struct.pack_into('<LL', header, 0x10 + i * 8, offset, len(section))
            offset += size
        f.write(header)
        for section in self.sections:
            f.write(section)
            if len(section) % 16 != 0:
                f.write(bytes(16 - (len(section) % 16)))

    def save_to_file(self, path):
        with open(path, 'wb') as f:
            self.save(f)