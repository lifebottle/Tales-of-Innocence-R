import struct
from ...text import decode_text_fixed, remove_redundant_cc, decode_text, encode_text, decode_text_and_offset

class SkitText:
    pass

class SkitLine(SkitText):
    def __init__(self, index, speakers, text, speakerName=None):
        self.speakers = speakers
        self.text = text
        self.speakerName = speakerName
        self.index = index

class SkitLineAddition(SkitText):
    def __init__(self, index, text):
        self.text = text
        self.index = index

class SkitChoices(SkitText):
    def __init__(self, index, choices):
        self.index = index
        self.choices = choices

class Skit:
    def __init__(self, index, title, speakers):
        #self.title = title
        self.index = index
        self.speakers = speakers
        self.lines = []

    def set_speaker(self, index, speaker):
        self.speakers[index] = speaker    

class SkitDeCompiler:
    def __init__(self, skit_dat):
        self.dat = skit_dat

    def extract_text(self):
        self.speakers = self._extract_speakers()
        lines = self._extract_lines()
        return self.speakers, lines

    def _extract_speakers(self):
        speaker_count = self.dat[4]
        speaker_base, = struct.unpack_from('<L', self.dat, 8)
        speakers = []
        for i in range(speaker_count):
            length, offset = struct.unpack_from('<HL', self.dat, speaker_base + i * 0x10 + 10)
            text = decode_text_fixed(self.dat, offset, length - 1)
            speakers.append(text)
        return speakers

    def _extract_lines(self):
        base, = struct.unpack_from('<L', self.dat, 12)
        count, = struct.unpack_from('<H', self.dat, 6)
        i = 0
        texts = []
        self._text_offsets = {}
        while i < count:
            offset, = struct.unpack_from('<L', self.dat, base + i * 4)
            opcode = self.dat[offset]
            if opcode == 0x17:
                texts.append(self._extract_line(i, offset))
            elif opcode == 0x1F:
                texts.append(self._extract_choices(i, offset))
            elif opcode == 0x22:
                i += 1
            elif opcode == 0x25:
                texts.append(self._extract_line_addition(i, offset))
            i += 1
        self._check_completion()
        return texts

    def _check_completion(self):
        """
        Check that all text has been extracted. This is done by checking
        whether the found strings (aligned to 16 bytes) completely cover
        the file until its end.
        """

        offset = None
        for next in sorted(self._text_offsets):
            if offset:
                if offset != next:
                    raise ValueError(f'skit extraction not complete ({offset:04X} vs {next:04X})')
            else:
                offset = next
            offset += self._text_offsets[next]
            if offset % 16 != 0:
                offset += 16 - (offset % 16)
        if offset != len(self.dat):
            raise ValueError('skit extraction not complete (not reaching EOF)')

    def _decode(self, offset, length=None):
        text, next = decode_text_and_offset(self.dat, offset, length)
        # If length is not None, the terminating 0x00 might not be decoded.
        if next < len(self.dat) and self.dat[next] == 0x00:
            next += 1
        # Save offset end encoded length for checking if all texts were found.
        self._text_offsets[offset] = next - offset
        return text


    def _extract_line(self, index, offset):
        speaker, flag, length, speakerOffset, line_offset = struct.unpack_from('<H3xB2xH4xLL', self.dat, offset + 2)
        tempSpeaker = None
        if flag != 0:
            tempSpeaker = self._decode(speakerOffset)
        text = self._decode(line_offset, length)
        return SkitLine(index, speaker, remove_redundant_cc(text), tempSpeaker)

    def _extract_line_addition(self, index, offset):
        length, line_offset = struct.unpack_from('<BxL', self.dat, offset + 2)
        text = self._decode(line_offset, length)
        return SkitLineAddition(index, remove_redundant_cc(text))

    def _extract_choices(self, index, offset):
        count, = struct.unpack_from('B', self.dat, offset + 1)
        choices = []
        for i in range(count):
            choice_offset, = struct.unpack_from('<L', self.dat, offset + 4 + i * 4)
            text = self._decode(choice_offset)
            choices.append(remove_redundant_cc(text))
        return SkitChoices(index, choices)

    def replace_text(self, skit):
        self.dat = bytearray(self.dat)
        self._text = bytes()
        self._base_offset = self._determine_base_offset()
        self._replace_speakers(skit.speakers)
        self._replace_lines(skit.lines)
        self.dat = self.dat[:self._base_offset] + self._text
        return self.dat

    def _determine_base_offset(self):
        base, = struct.unpack_from('<L', self.dat, 8)
        offset, = struct.unpack_from('<L', self.dat, base + 12)
        return offset

    def _replace_speakers(self, speakers):
        base, = struct.unpack_from('<L', self.dat, 8)
        count = self.dat[4]
        if count != len(speakers):
            raise ValueError('number of speakers does not match')
        
        for i, speaker in enumerate(speakers):
            offset, length = self._allocate_text(speaker)
            struct.pack_into('<HL', self.dat, base + i * 0x10 + 10, length, offset)

    def _replace_lines(self, lines):
        base, = struct.unpack_from('<L', self.dat, 12)
        count, = struct.unpack_from('<H', self.dat, 6)

        for line in lines:
            if line.index >= count:
                raise ValueError(f'invalid skit instruction index: {line.index} / {count}')
            offset, = struct.unpack_from('<L', self.dat, base + line.index * 4)
            if isinstance(line, SkitLine):
                self._replace_line(offset, line)
            elif isinstance(line, SkitChoices):
                self._replace_choices(offset, line)
            elif isinstance(line, SkitLineAddition):
                self._replace_line_addition(offset, line)
            else:
                raise ValueError('unknown SkitText')

    def _replace_line(self, offset, line):
        if line.speakerName:
            speaker_offset, length = self._allocate_text(line.speakerName)
            struct.pack_into('<L', self.dat, offset + 16, speaker_offset)
        text_offset, length = self._allocate_text(line.text)
        struct.pack_into('<H', self.dat, offset + 10, length)
        struct.pack_into('<L', self.dat, offset + 20, text_offset)

    def _replace_line_addition(self, offset, line):
        text_offset, length = self._allocate_text(line.text)
        struct.pack_into('<B', self.dat, offset + 1, length)
        struct.pack_into('<L', self.dat, offset + 4, text_offset)

    def _replace_choices(self, offset, choices):
        expected = struct.unpack_from('B', self.dat, offset+1)[0]
        if expected != len(choices.choices):
            raise ValueError(f'expected {expected} choices, got {len(choices.choices)}')
        for i, choice in enumerate(choices.choices):
            text_offset, _ = self._allocate_text(choice)
            struct.pack_into('<L', self.dat, offset + i * 4 + 4, text_offset)

    def _allocate_text(self, text):
        binary = encode_text(text)
        offset = len(self._text)
        self._text += binary
        if len(self._text) % 16 != 0:
            self._text += bytes(16 - (len(self._text) % 16))
        return self._base_offset + offset, len(binary)

def skit_extract_text(skit_dat):
    return SkitDeCompiler(skit_dat).extract_text()

def skit_replace_text(skit_dat, skit):
    return SkitDeCompiler(skit_dat).replace_text(skit)
