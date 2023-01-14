from . import ScriptInstructionWithArgs, ScriptInstruction

class ScriptPlayerVisible(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptPlayerMovePointFrame(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BHHB', opcode)

class ScriptPlayerDirObject(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBH', opcode)

class ScriptPlayerDirMoveAbs(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<HBH', opcode)
        
class ScriptPlayerMotionPackSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<H', opcode)

class ScriptPlayerMoveWait(ScriptInstruction):
    pass

class ScriptPlayerPushCancel(ScriptInstruction):
    pass

class ScriptPlayerMotionChange(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<HBL', opcode)

class ScriptPlayerModelLoad(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBB', opcode)

class ScriptPlayerWeaponVisible(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptPlayerDirWait(ScriptInstruction):
    pass

class ScriptPlayerMoveDirAbs(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<HHHBfB', opcode)

class ScriptPlayerDirPoint(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBH', opcode)

class ScriptPlayerMovePointSpeed(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BHBLB', opcode)

class ScriptPlayerChangeType(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptPlayerMotionWait(ScriptInstruction):
    pass

class ScriptPlayerCollisionSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptPlayerAlphaMove(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BH', opcode)

class ScriptPlayerAlphaWait(ScriptInstruction):
    pass

class ScriptPlayerDirMoveRel(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<HBH', opcode)

class ScriptPlayerMoveDirRel(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<HHHBLB', opcode)

class ScriptPlayerShadowDisp(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BH', opcode)
