import struct

class ScriptInstruction:
    @staticmethod
    def from_opcode(opcode):
        try:
            return _OPCODE_MAP[opcode](opcode)
        except:
            raise IndexError(f'invalid opcode {hex(opcode)}')

    def __init__(self, opcode):
        self.opcode = opcode
        self.args = []

    def decode(self, buffer, offset):
        return offset

    def encode(self):
        return bytes([self.opcode])

    def pretty_print(self):
        if self.args:
            args = ', '.join([str(x) for x in self.args])
            return f'{self.__class__.__name__}({args})'
        else:
            return f'{self.__class__.__name__}()'

class ScriptInstructionWithArgs(ScriptInstruction):
    def __init__(self, format, opcode):
        super().__init__(opcode)
        self._format = format

    def decode(self, buffer, offset):
        self.args = list(struct.unpack_from(self._format, buffer, offset))
        return offset + struct.calcsize(self._format)

    def encode(self):
        return bytes([self.opcode]) + struct.pack(self._format, *self.args)

from .controlflow import *
from .objects import *
from .player import *
from .camera import *
from .effects import *
from .audio import *
from .event import *
from .msg import *

class ScriptWaitKey(ScriptInstruction):
    pass

class ScriptFilterSetup(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBBB', opcode)

class ScriptFilterFade(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BH', opcode)

class ScriptFilterWait(ScriptInstruction):
    pass

class ScriptFadeType(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptFadeIn(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptFadeWait(ScriptInstruction):
    pass

class ScriptMotionPackLoad(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<H', opcode)

class ScriptMotionPackSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BH', opcode)

class ScriptMotionPackRelease(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<H', opcode)

class ScriptImageLoad(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)

class ScriptWait(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<H', opcode)

class ScriptEmotionSetObject(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBBBHH', opcode)

class ScriptEmotionWait(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptItemAdd(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<HBBB', opcode)

class ScriptSkitCall(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<H', opcode)

class ScriptSceneTownName(ScriptInstruction):
    pass

class ScriptSceneWait(ScriptInstruction):
    pass

class ScriptSceneRelease(ScriptInstruction):
    pass

class ScriptFadeOut(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptEquipChange(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBH', opcode)

class ScriptStoryLvSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<H', opcode)

class ScriptSystemLock(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)

class ScriptArtsSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBH', opcode)

class ScriptBattleBookSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptResultTalkPeriodSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)

class ScriptStoryBookStepAdd(ScriptInstruction):
    pass

class ScriptSceneMoviePlay(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptSceneMovieWait(ScriptInstruction):
    pass

class ScriptSceneMovieEnd(ScriptInstruction):
    pass

class ScriptMapFadeColor(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBBB', opcode)

class ScriptMapVisible(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptArtsLearning(ScriptInstruction):
    pass

class ScriptPartyRest(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptPartyDamage(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptScriptEntry(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<H', opcode)

class ScriptBattleSetting(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BL', opcode)

class ScriptBattleStart(ScriptInstruction):
    def decode(self, buffer, offset):
        count = buffer[offset]
        offset += 1
        self.args1 = []
        for _ in range(count):
            args = list(struct.unpack_from('<HBB', buffer, offset))
            offset += 4
            self.args1.append(args)
        self.args2 = list(struct.unpack_from('<BHBB', buffer, offset))
        return offset + 5

    def encode(self):
        binary = struct.pack('<BB', self.opcode, len(self.args1))
        for arg in self.args1:
            binary += struct.pack('<HBB', *arg)
        binary += struct.pack('<BHBB', *self.args2)
        return binary

class ScriptMapChange(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBBB', opcode)

class ScriptImageRelease(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptAbilityPlateOpen(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)

class ScriptPartyAdd(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptPartyModelLoad(ScriptInstruction):
    pass

class ScriptShopLVSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)

class ScriptPartyKeep(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptPartyTopSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptRaveLVSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptPartyBack(ScriptInstruction):
    pass

class ScriptSkitWait(ScriptInstruction):
    pass

class ScriptEmotionSetPlayer(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBBHH', opcode)

class ScriptMoneyAdd(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<L', opcode)

class ScriptSeVolume(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BHH', opcode)

class ScriptPartyRemove(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptMapChangeEnable(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)

class ScriptFarViewVisible(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptWeatherEnable(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptMsgActionOff(ScriptInstruction):
    pass

class ScriptFarViewPosSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptMoneyDisp(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptAircraftTypeSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptPartySelect(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptParamAdd(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBH', opcode)

class ScriptSceneConcentration(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BBBBHB', opcode)

class ScriptNaviMapFullOpen(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptNaviMapChange(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptMapFadeAlpha(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)

class ScriptSkitSearch(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)

class ScriptEncountControl(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptSuperArtsSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptShipTypeSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptWeatherChange(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptPartyLvAvgSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptShipPointSet(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptFreeFrameEnable(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<BB', opcode)

class ScriptCookingStateReset(ScriptInstructionWithArgs):
    def __init__(self, opcode):
        super().__init__('<B', opcode)

class ScriptSuccessionJump(ScriptInstruction):
    pass

_OPCODE_MAP = {
    0x00: ScriptLabel,
    0x01: ScriptJump,
    0x02: ScriptIf,
    0x03: ScriptSwitch,
    0x04: ScriptWait,
    0x05: ScriptWaitKey,
    0x06: ScriptFadeOut,
    0x07: ScriptFadeIn,
    0x08: ScriptFadeType,
    0x09: ScriptFadeWait,
    0x0A: ScriptEventFlagSet,
    0x0B: ScriptEventFlagAdd,
    0x0C: ScriptEventFlagFill,
    0x0D: ScriptEventFlagRandSet,
    0x0E: ScriptPlayerMovePointSpeed,
    0x0F: ScriptPlayerMovePointFrame,
    0x10: ScriptPlayerMoveDirRel,
    0x11: ScriptPlayerMoveWait,
    0x12: ScriptPlayerDirMoveRel,
    0x13: ScriptPlayerDirPoint,
    0x14: ScriptPlayerDirObject,
    0x15: ScriptPlayerDirWait,
    0x16: ScriptPlayerMotionChange,
    0x17: ScriptPlayerVisible,
    0x18: ScriptObjectMovePointSpeed,
    0x19: ScriptObjectMovePointFrame,
    0x1A: ScriptObjectMoveDirRel,
    0x1B: ScriptObjectMoveWait,
    0x1C: ScriptObjectDirMoveRel,
    0x1D: ScriptObjectDirPoint,
    0x1E: ScriptObjectDirPlayer,
    0x1F: ScriptObjectDirObject,
    0x20: ScriptObjectDirDefault,
    0x21: ScriptObjectDirWait,
    0x22: ScriptObjectMotionChange,
    0x23: ScriptObjectVisible,
    0x24: ScriptObjectActive,
    0x25: ScriptCameraDefault,
    0x26: ScriptCameraSet,
    0x27: ScriptCameraScenePlay,
    0x28: ScriptCameraSceneWait,
    0x29: ScriptCameraLockPlayer,
    0x2A: ScriptCameraLockObject,
    0x2C: ScriptCameraLockRelease,
    0x2D: ScriptMapChange,
    0x2E: ScriptMapChangeEnable,
    0x2F: ScriptFreeFrameEnable,
    0x30: ScriptEncountControl,
    0x31: ScriptNaviMapFullOpen,
    0x32: ScriptMoneyAdd,
    0x34: ScriptItemAdd,
    0x35: ScriptPartyAdd,
    0x36: ScriptPartyRemove,
    0x37: ScriptBgmDefaultPlay,
    0x38: ScriptBgmPlay,
    0x39: ScriptBgmLockReset,
    0x3A: ScriptBgmVolume,
    0x3B: ScriptBgmPause,
    0x3C: ScriptBgmResume,
    0x3E: ScriptObjectEyeAnime,
    0x43: ScriptObjectNeckDefault,
    0x44: ScriptObjectNeckPoint,
    0x45: ScriptObjectNeckPlayer,
    0x46: ScriptObjectNeckObject,
    0x47: ScriptObjectNeckWait,
    0x48: ScriptWeatherChange,
    0x4D: ScriptMsg,
    0x4E: ScriptMsgWait,
    0x4F: ScriptChoice,
    0x51: ScriptShopJump,
    0x54: ScriptWeatherEnable,
    0x55: ScriptBattleStart,
    0x56: ScriptBattleSetting,
    0x58: ScriptObjectPathSwitch,
    0x59: ScriptObjectPathAction,
    0x5A: ScriptEventSkipSet,
    0x5B: ScriptScriptEntry,
    0x5C: ScriptSubScriptStart,
    0x5D: ScriptSubScriptStop,
    0x5E: ScriptMoneyDisp,
    0x5F: ScriptInnJump,
    0x60: ScriptPartyKeep,
    0x61: ScriptPartyBack,
    0x62: ScriptSkitCall,
    0x63: ScriptSkitSearch,
    0x64: ScriptPartyRest,
    0x66: ScriptSystemLock,
    0x67: ScriptArtsLearning,
    0x68: ScriptEmotionSetPlayer,
    0x69: ScriptEmotionSetObject,
    0x6A: ScriptEmotionWait,
    0x6B: ScriptObjectModelLoad,
    0x6C: ScriptMapFadeColor,
    0x6D: ScriptMapFadeAlpha,
    0x6E: ScriptSceneTownName,
    0x6F: ScriptSceneWait,
    0x70: ScriptPartySelect,
    0x71: ScriptPlayerModelLoad,
    0x72: ScriptSelectCommand,
    0x73: ScriptSelectCancel,
    0x74: ScriptImageLoad,
    0x75: ScriptImageRelease,
    0x76: ScriptEffectSpriteAssign,
    0x77: ScriptEffectVisible,
    0x78: ScriptEffectPosSet,
    0x79: ScriptEffectPointSet,
    0x7A: ScriptEffectLoop,
    0x7B: ScriptEffectSpriteCellNo,
    0x7C: ScriptEffectSpriteAnimeNo,
    0x7D: ScriptEffectBlendMode,
    0x7E: ScriptEffectDispType,
    0x7F: ScriptMenuJump,
    0x80: ScriptResultTalkPeriodSet,
    0x81: ScriptBattleBookSet,
    0x82: ScriptShopLVSet,
    0x83: ScriptSuperArtsSet,
    0x84: ScriptCookingStateReset,
    0x85: ScriptRaveLVSet,
    0x86: ScriptAbilityPlateOpen,
    0x87: ScriptShipTypeSet,
    0x88: ScriptAircraftTypeSet,
    0x89: ScriptShipPointSet,
    0x8A: ScriptPlayerChangeType,
    0x8C: ScriptPlayerAlphaMove,
    0x8D: ScriptPlayerAlphaWait,
    0x93: ScriptSkitPlayerJump,
    0x94: ScriptMoviePlayerJump,
    0x95: ScriptStoryBookStepAdd,
    0x97: ScriptPartyModelLoad,
    0x98: ScriptPlayerWeaponVisible,
    0x9A: ScriptObjectEyeChange,
    0x9F: ScriptCameraShake,
    0xA0: ScriptCameraShakeWait,
    0xA3: ScriptScriptJump,
    0xA2: ScriptEventFrameEnable,
    0xA4: ScriptMsgWindowSet,
    0xA5: ScriptSceneRelease,
    0xA6: ScriptPlayerMoveDirAbs,
    0xA7: ScriptPlayerDirMoveAbs,
    0xA8: ScriptObjectMoveDirAbs,
    0xA9: ScriptObjectDirMoveAbs,
    0xAA: ScriptCameraMovePlayer,
    0xAB: ScriptCameraMoveObject,
    0xAC: ScriptCameraMovePoint,
    0xAD: ScriptCameraMoveWait,
    0xAE: ScriptFilterSetup,
    0xAF: ScriptFilterFade,
    0xB0: ScriptFilterWait,
    0xB1: ScriptStoryLvSet,
    0xB2: ScriptMapVisible,
    0xB3: ScriptPlayerCollisionSet,
    0xB4: ScriptObjectCollisionSet,
    0xB5: ScriptEffectModelLoad,
    0xB6: ScriptEffectModelRelease,
    0xB7: ScriptEffectModelAssign,
    0xB9: ScriptObjectNeckRel,
    0xBA: ScriptSceneConcentration,
    0xBB: ScriptEffectMovePointSpeed,
    0xBC: ScriptEffectMovePointFrame,
    0xBD: ScriptEffectMoveWait,
    0xBE: ScriptEffectDirMoveAbs,
    0xC1: ScriptEffectScaleMove,
    0xC2: ScriptEffectScaleWait,
    0xC3: ScriptEffectAlphaMove,
    0xC4: ScriptEffectAlphaWait,
    0xC5: ScriptSceneMoviePlay,
    0xC6: ScriptEquipChange,
    0xC7: ScriptPlayerPushCancel,
    0xC8: ScriptSkitWait,
    0xC9: ScriptPartyDamage,
    0xCA: ScriptVoicePlay,
    0xCB: ScriptEffectMovePosFrame,
    0xCC: ScriptBgmStop,
    0xCD: ScriptVoiceStop,
    0xCE: ScriptObjectAlphaMove,
    0xCF: ScriptObjectAlphaWait,
    0xD0: ScriptObjectMotionLoop,
    0xD1: ScriptObjectMotionWait,
    0xD3: ScriptPlayerMotionWait,
    0xD4: ScriptCameraMovePlayerSpeed,
    0xD5: ScriptCameraMoveObjectSpeed,
    0xD6: ScriptCameraMovePointSpeed,
    0xD7: ScriptMsgActionOff,
    0xD8: ScriptObjectMouseAction,
    0xD9: ScriptObjectWeaponVisible,
    0xDA: ScriptMotionPackLoad,
    0xDB: ScriptMotionPackRelease,
    0xDC: ScriptPlayerMotionPackSet,
    0xDD: ScriptMotionPackSet,
    0xDE: ScriptSELoad,
    0xDF: ScriptSEUnLoad,
    0xE0: ScriptSEPlay,
    0xE1: ScriptSEStop,
    0xE2: ScriptSEWait,
    0xE5: ScriptEventFlagCalculate,
    0xE7: ScriptSceneMovieWait,
    0xE8: ScriptSceneMovieEnd,
    0xE9: ScriptObjectMotionFrameSet,
    0xEA: ScriptEffectWait,
    0xEC: ScriptObjectCostumeSet,
    0xED: ScriptPlayerShadowDisp,
    0xEE: ScriptObjectShadowDisp,
    0xEF: ScriptSeVolume,
    0xF0: ScriptFarViewVisible,
    0xF1: ScriptFarViewPosSet,
    0xF2: ScriptInfoMsg,
    0xF3: ScriptObjectMotionSpeedSet,
    0xF4: ScriptNaviMapChange,
    0xF5: ScriptArtsSet,
    0xF6: ScriptParamAdd,
    0xF7: ScriptStaffRollJump,
    0xF8: ScriptClearSaveJump,
    0xF9: ScriptSuccessionJump,
    0xFA: ScriptPartyTopSet,
    0xFB: ScriptPartyLvAvgSet,
}