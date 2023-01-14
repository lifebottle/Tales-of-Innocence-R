from . import ScriptInstruction, ScriptInstructionWithArgs
import struct

class ScriptEventSkipSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptEventFlagSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<HB', opcode)

    @property
    def flag_index(self):
        return self.args[0]

    @property
    def flag_value(self):
        return self.args[1]

class ScriptEventFrameEnable(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)

class ScriptEventFlagRandSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<HBB', opcode)
        
class ScriptEventFlagAdd(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<HB', opcode)
        
class ScriptEventFlagCalculate(ScriptInstruction):
    def decode(self, buffer, offset):
        self.flag_index, term_count = struct.unpack_from('<HB', buffer, offset)
        offset += 3
        self.terms = []
        for _ in range(term_count):
            term = list(struct.unpack_from('<BBBLL', buffer, offset))
            offset += 11
            self.terms.append(term)
        return offset
        
    def encode(self):
        binary = struct.pack('<BHB', self.opcode, self.flag_index, len(self.terms))
        for term in self.terms:
            binary += struct.pack('<BBBLL', *term)
        return binary

class ScriptEventFlagFill(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<HHB', opcode)
