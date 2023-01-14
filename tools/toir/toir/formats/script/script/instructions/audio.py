from . import ScriptInstruction, ScriptInstructionWithArgs
import struct

class ScriptBgmPause(ScriptInstruction):
    pass

class ScriptBgmResume(ScriptInstruction):
    pass

class ScriptBgmLockReset(ScriptInstruction):
    pass

class ScriptBgmVolume(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)

class ScriptVoicePlay(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<HH', opcode)

class ScriptVoiceStop(ScriptInstruction):
    pass

class ScriptSEUnLoad(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptBgmStop(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)
        
class ScriptBgmPlay(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBB', opcode)

class ScriptBgmDefaultPlay(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)
        
class ScriptSEPlay(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBB', opcode)

class ScriptSEWait(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptSEStop(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BH', opcode)

class ScriptSELoad(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)
