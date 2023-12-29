from . import ScriptInstruction, ScriptInstructionWithArgs
import struct

class ScriptObjectDirPlayer(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBH', opcode)

class ScriptObjectDirDefault(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBH', opcode)

class ScriptObjectVisible(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)

class ScriptObjectMotionChange(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BHBL', opcode)
        
class ScriptObjectMovePointFrame(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBHHB', opcode)

class ScriptObjectMovePointSpeed(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBHBfB', opcode)

class ScriptObjectMoveWait(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptObjectMouseAction(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptObjectModelLoad(ScriptInstruction):
    pass

class ScriptObjectDirPoint(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBBH', opcode)

class ScriptObjectDirWait(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptObjectDirObject(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBBH', opcode)

class ScriptObjectDirMoveAbs(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BHBH', opcode)

class ScriptObjectCostumeSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BH', opcode)

class ScriptObjectEyeAnime(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)

class ScriptObjectMotionWait(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptObjectMotionFrameSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BL', opcode)

class ScriptObjectNeckRel(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BHHBH', opcode)

class ScriptObjectNeckDefault(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBH', opcode)

class ScriptObjectDirMoveRel(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BHBH', opcode)

class ScriptObjectNeckWait(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptObjectWeaponVisible(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)

class ScriptObjectEyeChange(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)

class ScriptObjectShadowDisp(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBH', opcode)

class ScriptObjectNeckPlayer(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBH', opcode)

class ScriptObjectNeckObject(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBBH', opcode)

class ScriptObjectMotionLoop(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBLL', opcode)

class ScriptObjectCollisionSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)

class ScriptObjectAlphaMove(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBH', opcode)

class ScriptObjectMoveDirAbs(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BHHHBLB', opcode)

class ScriptObjectAlphaWait(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptObjectMotionSpeedSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BL', opcode)

class ScriptObjectNeckPoint(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBBH', opcode)

class ScriptObjectMoveDirRel(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BHHHBLB', opcode)

class ScriptObjectActive(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)

class ScriptObjectPathSwitch(ScriptInstruction):
    def __init__(self, opcode):
        self.opcode = opcode

    def decode(self, buffer, offset):
        self.args = list(struct.unpack_from('<BB', buffer, offset))
        offset += 2
        self.cases = []
        for _ in range(self.args[1]):
            case = list(struct.unpack_from('<BLB', buffer, offset))
            offset += 6
            self.cases.append(case)
        return offset

    def encode(self):
        binary = struct.pack('<BBB', self.opcode, *self.args)
        for case in self.cases:
            binary += struct.pack('<BLB', *case)
        return binary

    def pretty_print(self):
        string = super().pretty_print() + '\n'
        for case in self.cases:
            string += '  Case(' + ', '.join([str(x) for x in case]) + ')\n'
        return string

class ScriptObjectPathAction(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<HHHH', opcode)
