from . import ScriptInstruction, ScriptInstructionWithArgs
import struct

class ScriptEffectPointSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)

class ScriptEffectDispType(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)

class ScriptEffectScaleMove(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BLH', opcode)

class ScriptEffectSpriteAnimeNo(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)

class ScriptEffectBlendMode(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)

class ScriptEffectVisible(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)

class ScriptEffectLoop(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBLL', opcode)
        
class ScriptEffectSpriteAssign(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)
        
class ScriptEffectSpriteCellNo(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)

class ScriptEffectPosSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BHH', opcode)
        
class ScriptEffectModelLoad(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)

class ScriptEffectModelAssign(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)

class ScriptEffectAlphaMove(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBH', opcode)

class ScriptEffectModelRelease(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)
        
class ScriptEffectMovePointFrame(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBH', opcode)

class ScriptEffectMoveWait(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)
        
class ScriptEffectMovePointSpeed(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBL', opcode)
        
class ScriptEffectWait(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)
        
class ScriptEffectDirMoveAbs(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BHHHH', opcode)
        
class ScriptEffectScaleWait(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)
        
class ScriptEffectMovePosFrame(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BHHH', opcode)
        
class ScriptEffectAlphaWait(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)
