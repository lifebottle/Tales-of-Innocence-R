from .instructions import ScriptInstruction, ScriptMsg, ScriptSelectCommand
import struct
from collections import namedtuple

class DecompilationException(Exception):
    pass

class OffsetSizeMismatchError(DecompilationException):
    def __init__(self, offset, size, script):
        self.offset = offset
        self.size = size
        self.script = script

    def __str__(self):
        return f'offset ({self.offset})/size ({self.size}) mismatch during decompilation'

class UnknownOpcodeError(DecompilationException):
    def __init__(self, opcode, offset, script):
        self.opcode = opcode
        self.offset = offset
        self.script = script

    def __str__(self):
        return f'opcode {self.opcode:02X} at offset {self.offset} unknown'

TextWithSpeaker = namedtuple('TextWithSpeaker', ['speaker', 'text'])

class Script:
    @staticmethod
    def decompile(buffer):
        count, = struct.unpack_from('<H', buffer, 0)
        offset = 2
        script = Script()
        for _ in range(count):
            try:
                instruction = ScriptInstruction.from_opcode(buffer[offset])
            except IndexError as e:
                raise UnknownOpcodeError(buffer[offset], offset, script)
            start_offset = offset
            offset += 1
            offset = instruction.decode(buffer, offset)
            instruction._offset = start_offset
            script.append(instruction)
        if offset != len(buffer):
            raise OffsetSizeMismatchError(offset, len(buffer), script)
        return script

    def __init__(self):
        self.instructions = []
    
    def append(self, instruction):
        self.instructions.append(instruction)

    def collect_texts(self):
        texts = {}
        for i, instruction in enumerate(self.instructions):
            if isinstance(instruction, ScriptMsg):
                texts[f'{i}'] = TextWithSpeaker(instruction.speaker, instruction.text)
            elif isinstance(instruction, ScriptSelectCommand):
                for j, command in enumerate(instruction.commands):
                    texts[f'{i}/{j}'] = TextWithSpeaker(None, command)

        return texts
    
    def replace_texts(self, texts):
        for i, content in texts.items():
            instruction = self.instructions[i]
            if isinstance(instruction, ScriptMsg):
                self.instructions[i].text = content
            elif isinstance(instruction, ScriptSelectCommand):
                for j in range(len(instruction.commands)):
                    instruction.commands[j] = content[j]

    def dump(self, f):
        for i, instruction in enumerate(self.instructions):
            f.write(f'[{i:3}:{instruction._offset:04X}] 0x{instruction.opcode:02X} ')
            f.write(instruction.pretty_print())
            f.write('\n')

    def recompile(self):
        binary = struct.pack('<H', len(self.instructions))
        for instruction in self.instructions:
            binary += instruction.encode()
        return binary