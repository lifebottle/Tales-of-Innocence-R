from . import ScriptInstruction, ScriptInstructionWithArgs
import struct

class ScriptLabel(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptJump(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptIfBox:
    def __init__(self):
        self.operators = []
        self.children = []
        self.child_type = 0

    def decode(self, buffer, offset):
        self.childCount = buffer[offset]
        offset += 1
        if self.childCount > 0:            
            self.operators = list(buffer[offset:offset+self.childCount-1])
            offset += self.childCount - 1
            for _ in range(self.childCount):
                child_type = buffer[offset]
                offset += 1
                if child_type == 0:
                    child = ScriptIfBox()
                elif child_type == 1:
                    child = ScriptIfChild()
                offset = child.decode(buffer, offset)
                self.children.append(child)
        return offset

    def encode(self):
        binary = bytes([self.childCount])
        binary += bytes(self.operators)
        for child in self.children:
            binary += bytes([child.child_type])
            binary += child.encode()
        return binary

    def pretty_print(self, indent=0):
        string = ' ' * (indent * 2) + f'box({self.operators})\n'
        for child in self.children:
            string += child.pretty_print(indent + 1)
        return string

class ScriptIfChild:
    def __init__(self):
        self.child_type = 1

    def decode(self, buffer, offset):
        self.arg1 = buffer[offset]
        self.arg2 = buffer[offset + 1]
        self.arg3, self.arg4 = struct.unpack_from('<LL', buffer, offset + 2)
        self.arg5 = buffer[offset + 10]
        return offset + 11

    def encode(self):
        return struct.pack('<BBLLB', self.arg1, self.arg2, self.arg3, self.arg4, self.arg5)

    def pretty_print(self, indent=0):
        return ' ' * (indent * 2) + f'child({self.arg1}, {self.arg2}, {self.arg3}, {self.arg4}, {self.arg5})\n'

class ScriptIf(ScriptInstruction):
    def __init__(self, opcode):
        self.opcode = opcode
        self.box = None

    def decode(self, buffer, offset):
        self.label = buffer[offset]
        self.arg2 = buffer[offset + 1]
        self.arg3 = buffer[offset + 2]
        self.box = ScriptIfBox()
        return self.box.decode(buffer, offset + 3)      

    def encode(self):
        binary = bytes([self.opcode]) + struct.pack('<BBB', self.label, self.arg2, self.arg3)
        binary += self.box.encode()
        return binary

    def pretty_print(self):
        string = f'ScriptIf(label={self.label}, {self.arg2}, {self.arg3})\n'
        string += self.box.pretty_print(1)
        return string

class ScriptSwitch(ScriptInstruction):
    def decode(self, buffer, offset):
        self.args = list(struct.unpack_from('<BLB', buffer, offset))
        offset += 6
        self.cases = []
        for _ in range(self.args[2]):
            case = list(struct.unpack_from('<BLB', buffer, offset))
            offset += 6
            self.cases.append(case)
        return offset

    def encode(self):
        binary = struct.pack('<BBLB', self.opcode, *self.args)
        for case in self.cases:
            binary += struct.pack('<BLB', *case)
        return binary

    def pretty_print(self):
        string = super().pretty_print() + '\n'
        for case in self.cases:
            string += '  Case(' + ', '.join([str(x) for x in case]) + ')\n'
        return string

class ScriptSkitPlayerJump(ScriptInstruction):
    pass

class ScriptMoviePlayerJump(ScriptInstruction):
    pass

class ScriptMenuJump(ScriptInstruction):
    pass

class ScriptShopJump(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptClearSaveJump(ScriptInstruction):
    pass

class ScriptInnJump(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BHBBBB', opcode)

class ScriptScriptJump(ScriptInstruction):
    def decode(self, buffer, offset):
        self.target, = struct.unpack_from('<H', buffer, offset)
        return offset + 2

    def encode(self):
        return struct.pack('<BH', self.opcode, self.target)

    def pretty_print(self):
        return f'ScriptScriptJump(target="{self.target:03}.dat")'

class ScriptSubScriptStart(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BH', opcode)

class ScriptSubScriptStop(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptStaffRollJump(ScriptInstruction):
    pass
