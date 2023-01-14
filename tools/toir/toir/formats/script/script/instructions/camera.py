from . import ScriptInstruction, ScriptInstructionWithArgs
import struct

class ScriptCameraDefault(ScriptInstruction):
    pass

class ScriptCameraLockRelease(ScriptInstruction):
    pass

class ScriptCameraSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptCameraScenePlay(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptCameraSceneWait(ScriptInstruction):
    pass

class ScriptCameraLockPlayer(ScriptInstruction):
    pass

class ScriptCameraLockObject(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptCameraShake(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<HH', opcode)

class ScriptCameraShakeWait(ScriptInstruction):
    pass

class ScriptCameraMoveObject(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BH', opcode)

class ScriptCameraMovePoint(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BH', opcode)

class ScriptCameraMoveWait(ScriptInstruction):
    pass

class ScriptCameraMovePlayer(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<H', opcode)

class ScriptCameraMovePointSpeed(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BL', opcode)

class ScriptCameraMovePlayerSpeed(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<L', opcode)
    
class ScriptCameraMoveObjectSpeed(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BL', opcode)
