import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_
import _dafny
import System_
import Int
import MiscTypes
import EVMConstants
import EVMOpcodes
import OpcodeDecoder
import Hex
import StackElement
import WeakPre
import State

# Module: Instructions

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def GetArgValuePush(xc):
        d_183_pad_ = _dafny.SeqWithoutIsStrInference([_dafny.CodePoint('0') for d_184___v164_ in range((64) - (len(xc)))])
        return (Hex.default__.HexToU256((d_183_pad_) + (xc))).Extract()


class ValidInstruction:
    def  __init__(self):
        pass

    @staticmethod
    def default():
        return Instruction_Instruction(EVMOpcodes.Opcode_SysOp(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "STOP")), EVMConstants.default__.STOP, 0, 0, 0, 0), _dafny.SeqWithoutIsStrInference([]), 0)

class Instruction:
    @classmethod
    def default(cls, ):
        return lambda: Instruction_Instruction(EVMOpcodes.ValidOpcode.default(), _dafny.Seq({}), int(0))
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_Instruction(self) -> bool:
        return isinstance(self, Instruction_Instruction)
    def IsValid(self):
        def lambda2_(forall_var_2_):
            d_185_k_: int = forall_var_2_
            return not (((0) <= (d_185_k_)) and ((d_185_k_) < (len((self).arg)))) or (Hex.default__.IsHex(((self).arg)[d_185_k_]))

        return ((((self).op).opcode) == (EVMConstants.default__.INVALID)) or ((not (((EVMConstants.default__.PUSH0) <= (((self).op).opcode)) and ((((self).op).opcode) <= (EVMConstants.default__.PUSH32))) or (((len((self).arg)) == ((2) * ((((self).op).opcode) - (EVMConstants.default__.PUSH0)))) and (_dafny.quantifier(_dafny.IntegerRange(0, len((self).arg)), True, lambda2_)))) and (not (not(((EVMConstants.default__.PUSH0) <= (((self).op).opcode)) and ((((self).op).opcode) <= (EVMConstants.default__.PUSH32)))) or ((len((self).arg)) == (0))))

    def ToString(self):
        d_186_x_ = (self).arg
        if (((self).op).opcode) == (EVMConstants.default__.INVALID):
            return ((((self).op).Name()) + (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, " ")))) + (d_186_x_)
        elif True:
            return (((self).op).Name()) + (((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, " 0x"))) + (d_186_x_) if (len(d_186_x_)) > (0) else _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, ""))))

    def IsTerminal(self):
        return ((self).op).IsTerminal()

    def IsJumpDest(self):
        return ((self).op).IsJumpDest()

    def StackEffect(self):
        return ((self).op).StackEffect()

    def WeakestPreOperands(self, post):
        return ((self).op).WeakestPreOperands(post)

    def WeakestPreCapacity(self, post):
        return ((self).op).WeakestPreCapacity(post)

    def StackPosBackWardTracker(self, pos_k):
        source32_ = (self).op
        if source32_.is_ArithOp:
            d_187___mcc_h0_ = source32_.name
            d_188___mcc_h1_ = source32_.opcode
            d_189___mcc_h2_ = source32_.minCapacity
            d_190___mcc_h3_ = source32_.minOperands
            d_191___mcc_h4_ = source32_.pushes
            d_192___mcc_h5_ = source32_.pops
            d_193_pops_ = d_192___mcc_h5_
            d_194_pushes_ = d_191___mcc_h4_
            if (pos_k) >= (1):
                return MiscTypes.Either_Right((pos_k) + (1))
            elif True:
                return MiscTypes.Either_Left(StackElement.StackElem_Random(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "More than one predecessor. Arithmetic operator with target 0"))))
        elif source32_.is_CompOp:
            d_195___mcc_h6_ = source32_.name
            d_196___mcc_h7_ = source32_.opcode
            d_197___mcc_h8_ = source32_.minCapacity
            d_198___mcc_h9_ = source32_.minOperands
            d_199___mcc_h10_ = source32_.pushes
            d_200___mcc_h11_ = source32_.pops
            d_201_pops_ = d_200___mcc_h11_
            d_202_pushes_ = d_199___mcc_h10_
            if (pos_k) >= (1):
                return MiscTypes.Either_Right(((pos_k) + (d_201_pops_)) - (d_202_pushes_))
            elif True:
                return MiscTypes.Either_Left(StackElement.StackElem_Random(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "More than one predecessor. Comparison operator with target 0"))))
        elif source32_.is_BitwiseOp:
            d_203___mcc_h12_ = source32_.name
            d_204___mcc_h13_ = source32_.opcode
            d_205___mcc_h14_ = source32_.minCapacity
            d_206___mcc_h15_ = source32_.minOperands
            d_207___mcc_h16_ = source32_.pushes
            d_208___mcc_h17_ = source32_.pops
            return MiscTypes.Either_Left(StackElement.StackElem_Random(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Not implemented"))))
        elif source32_.is_KeccakOp:
            d_209___mcc_h18_ = source32_.name
            d_210___mcc_h19_ = source32_.opcode
            d_211___mcc_h20_ = source32_.minCapacity
            d_212___mcc_h21_ = source32_.minOperands
            d_213___mcc_h22_ = source32_.pushes
            d_214___mcc_h23_ = source32_.pops
            return MiscTypes.Either_Left(StackElement.StackElem_Random(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Not implemented"))))
        elif source32_.is_EnvOp:
            d_215___mcc_h24_ = source32_.name
            d_216___mcc_h25_ = source32_.opcode
            d_217___mcc_h26_ = source32_.minCapacity
            d_218___mcc_h27_ = source32_.minOperands
            d_219___mcc_h28_ = source32_.pushes
            d_220___mcc_h29_ = source32_.pops
            return MiscTypes.Either_Left(StackElement.StackElem_Random(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Not implemented"))))
        elif source32_.is_MemOp:
            d_221___mcc_h30_ = source32_.name
            d_222___mcc_h31_ = source32_.opcode
            d_223___mcc_h32_ = source32_.minCapacity
            d_224___mcc_h33_ = source32_.minOperands
            d_225___mcc_h34_ = source32_.pushes
            d_226___mcc_h35_ = source32_.pops
            return MiscTypes.Either_Left(StackElement.StackElem_Random(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Not implemented"))))
        elif source32_.is_StorageOp:
            d_227___mcc_h36_ = source32_.name
            d_228___mcc_h37_ = source32_.opcode
            d_229___mcc_h38_ = source32_.minCapacity
            d_230___mcc_h39_ = source32_.minOperands
            d_231___mcc_h40_ = source32_.pushes
            d_232___mcc_h41_ = source32_.pops
            return MiscTypes.Either_Left(StackElement.StackElem_Random(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Not implemented"))))
        elif source32_.is_JumpOp:
            d_233___mcc_h42_ = source32_.name
            d_234___mcc_h43_ = source32_.opcode
            d_235___mcc_h44_ = source32_.minCapacity
            d_236___mcc_h45_ = source32_.minOperands
            d_237___mcc_h46_ = source32_.pushes
            d_238___mcc_h47_ = source32_.pops
            d_239_opcode_ = d_234___mcc_h43_
            if (d_239_opcode_) == (EVMConstants.default__.JUMPDEST):
                return MiscTypes.Either_Right(pos_k)
            elif ((EVMConstants.default__.JUMP) <= (d_239_opcode_)) and ((d_239_opcode_) <= (EVMConstants.default__.JUMPI)):
                d_240_k_ = ((d_239_opcode_) - (EVMConstants.default__.JUMP)) + (1)
                return MiscTypes.Either_Right((pos_k) + (d_240_k_))
            elif True:
                return MiscTypes.Either_Left(StackElement.StackElem_Random(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Not implemented"))))
        elif source32_.is_RunOp:
            d_241___mcc_h48_ = source32_.name
            d_242___mcc_h49_ = source32_.opcode
            d_243___mcc_h50_ = source32_.minCapacity
            d_244___mcc_h51_ = source32_.minOperands
            d_245___mcc_h52_ = source32_.pushes
            d_246___mcc_h53_ = source32_.pops
            return MiscTypes.Either_Left(StackElement.StackElem_Random(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Not implemented"))))
        elif source32_.is_StackOp:
            d_247___mcc_h54_ = source32_.name
            d_248___mcc_h55_ = source32_.opcode
            d_249___mcc_h56_ = source32_.minCapacity
            d_250___mcc_h57_ = source32_.minOperands
            d_251___mcc_h58_ = source32_.pushes
            d_252___mcc_h59_ = source32_.pops
            d_253_opcode_ = d_248___mcc_h55_
            if ((EVMConstants.default__.PUSH0) <= (d_253_opcode_)) and ((d_253_opcode_) <= (EVMConstants.default__.PUSH32)):
                if (pos_k) == (0):
                    return MiscTypes.Either_Left(StackElement.StackElem_Value(default__.GetArgValuePush((self).arg)))
                elif True:
                    return MiscTypes.Either_Right((pos_k) - (1))
            elif ((EVMConstants.default__.DUP1) <= (d_253_opcode_)) and ((d_253_opcode_) <= (EVMConstants.default__.DUP16)):
                return MiscTypes.Either_Right(((d_253_opcode_) - (EVMConstants.default__.DUP1) if (pos_k) == (0) else (pos_k) - (1)))
            elif ((EVMConstants.default__.SWAP1) <= (d_253_opcode_)) and ((d_253_opcode_) <= (EVMConstants.default__.SWAP16)):
                d_254_k_ = ((d_253_opcode_) - (EVMConstants.default__.SWAP1)) + (1)
                return MiscTypes.Either_Right((d_254_k_ if (pos_k) == (0) else (0 if (pos_k) == (d_254_k_) else pos_k)))
            elif True:
                return MiscTypes.Either_Right((pos_k) + (1))
        elif source32_.is_LogOp:
            d_255___mcc_h60_ = source32_.name
            d_256___mcc_h61_ = source32_.opcode
            d_257___mcc_h62_ = source32_.minCapacity
            d_258___mcc_h63_ = source32_.minOperands
            d_259___mcc_h64_ = source32_.pushes
            d_260___mcc_h65_ = source32_.pops
            return MiscTypes.Either_Left(StackElement.StackElem_Random(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Not implemented"))))
        elif True:
            d_261___mcc_h66_ = source32_.name
            d_262___mcc_h67_ = source32_.opcode
            d_263___mcc_h68_ = source32_.minCapacity
            d_264___mcc_h69_ = source32_.minOperands
            d_265___mcc_h70_ = source32_.pushes
            d_266___mcc_h71_ = source32_.pops
            return MiscTypes.Either_Left(StackElement.StackElem_Random(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Not implemented"))))

    def NextState(self, s, cond):
        source33_ = (self).op
        if source33_.is_ArithOp:
            d_267___mcc_h0_ = source33_.name
            d_268___mcc_h1_ = source33_.opcode
            d_269___mcc_h2_ = source33_.minCapacity
            d_270___mcc_h3_ = source33_.minOperands
            d_271___mcc_h4_ = source33_.pushes
            d_272___mcc_h5_ = source33_.pops
            d_273_pops_ = d_272___mcc_h5_
            d_274_pushes_ = d_271___mcc_h4_
            if (((s).Size()) >= (d_273_pops_)) and (not(cond)):
                return (((s).PopN(d_273_pops_)).PushNRandom(d_274_pushes_)).Skip(1)
            elif True:
                return State.AState_Error(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Stack underflow")))
        elif source33_.is_CompOp:
            d_275___mcc_h6_ = source33_.name
            d_276___mcc_h7_ = source33_.opcode
            d_277___mcc_h8_ = source33_.minCapacity
            d_278___mcc_h9_ = source33_.minOperands
            d_279___mcc_h10_ = source33_.pushes
            d_280___mcc_h11_ = source33_.pops
            d_281_pops_ = d_280___mcc_h11_
            d_282_pushes_ = d_279___mcc_h10_
            if (((s).Size()) >= (d_281_pops_)) and (not(cond)):
                return (((s).PopN(d_281_pops_)).PushNRandom(d_282_pushes_)).Skip(1)
            elif True:
                return State.AState_Error(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Stack underflow")))
        elif source33_.is_BitwiseOp:
            d_283___mcc_h12_ = source33_.name
            d_284___mcc_h13_ = source33_.opcode
            d_285___mcc_h14_ = source33_.minCapacity
            d_286___mcc_h15_ = source33_.minOperands
            d_287___mcc_h16_ = source33_.pushes
            d_288___mcc_h17_ = source33_.pops
            d_289_pops_ = d_288___mcc_h17_
            d_290_pushes_ = d_287___mcc_h16_
            if (((s).Size()) >= (d_289_pops_)) and (not(cond)):
                return (((s).PopN(d_289_pops_)).PushNRandom(d_290_pushes_)).Skip(1)
            elif True:
                return State.AState_Error(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Stack underflow")))
        elif source33_.is_KeccakOp:
            d_291___mcc_h18_ = source33_.name
            d_292___mcc_h19_ = source33_.opcode
            d_293___mcc_h20_ = source33_.minCapacity
            d_294___mcc_h21_ = source33_.minOperands
            d_295___mcc_h22_ = source33_.pushes
            d_296___mcc_h23_ = source33_.pops
            d_297_pops_ = d_296___mcc_h23_
            d_298_pushes_ = d_295___mcc_h22_
            if (((s).Size()) >= (2)) and (not(cond)):
                return (((s).PopN(2)).Push(StackElement.StackElem_Random(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, ""))))).Skip(1)
            elif True:
                return State.AState_Error(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Stack underflow")))
        elif source33_.is_EnvOp:
            d_299___mcc_h24_ = source33_.name
            d_300___mcc_h25_ = source33_.opcode
            d_301___mcc_h26_ = source33_.minCapacity
            d_302___mcc_h27_ = source33_.minOperands
            d_303___mcc_h28_ = source33_.pushes
            d_304___mcc_h29_ = source33_.pops
            d_305_pops_ = d_304___mcc_h29_
            d_306_pushes_ = d_303___mcc_h28_
            if (((s).Size()) >= (d_305_pops_)) and (not(cond)):
                return (((s).PopN(d_305_pops_)).PushNRandom(d_306_pushes_)).Skip(1)
            elif True:
                return State.AState_Error(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "EnvOp error")))
        elif source33_.is_MemOp:
            d_307___mcc_h30_ = source33_.name
            d_308___mcc_h31_ = source33_.opcode
            d_309___mcc_h32_ = source33_.minCapacity
            d_310___mcc_h33_ = source33_.minOperands
            d_311___mcc_h34_ = source33_.pushes
            d_312___mcc_h35_ = source33_.pops
            d_313_pops_ = d_312___mcc_h35_
            d_314_pushes_ = d_311___mcc_h34_
            if (((s).Size()) >= (d_313_pops_)) and (not(cond)):
                return (((s).PopN(d_313_pops_)).PushNRandom(d_314_pushes_)).Skip(1)
            elif True:
                return State.AState_Error(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "MemOp error")))
        elif source33_.is_StorageOp:
            d_315___mcc_h36_ = source33_.name
            d_316___mcc_h37_ = source33_.opcode
            d_317___mcc_h38_ = source33_.minCapacity
            d_318___mcc_h39_ = source33_.minOperands
            d_319___mcc_h40_ = source33_.pushes
            d_320___mcc_h41_ = source33_.pops
            d_321_pops_ = d_320___mcc_h41_
            d_322_pushes_ = d_319___mcc_h40_
            if (((s).Size()) >= (d_321_pops_)) and (not(cond)):
                return (((s).PopN(d_321_pops_)).PushNRandom(d_322_pushes_)).Skip(1)
            elif True:
                return State.AState_Error(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Storage Op error")))
        elif source33_.is_JumpOp:
            d_323___mcc_h42_ = source33_.name
            d_324___mcc_h43_ = source33_.opcode
            d_325___mcc_h44_ = source33_.minCapacity
            d_326___mcc_h45_ = source33_.minOperands
            d_327___mcc_h46_ = source33_.pushes
            d_328___mcc_h47_ = source33_.pops
            d_329_pops_ = d_328___mcc_h47_
            d_330_pushes_ = d_327___mcc_h46_
            d_331_opcode_ = d_324___mcc_h43_
            if (d_331_opcode_) == (EVMConstants.default__.JUMPDEST):
                if not(cond):
                    return (s).Skip(1)
                elif True:
                    return State.AState_Error(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Cannot execute JUMPDEST/exit true")))
            elif (d_331_opcode_) == (EVMConstants.default__.JUMP):
                if (((s).Size()) >= (1)) and (cond):
                    source34_ = (s).Peek(0)
                    if source34_.is_Value:
                        d_332___mcc_h72_ = source34_.v
                        d_333_v_ = d_332___mcc_h72_
                        return ((s).Pop()).Goto(d_333_v_)
                    elif True:
                        d_334___mcc_h73_ = source34_.s
                        return State.AState_Error(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Jump to Random() error")))
                elif True:
                    return State.AState_Error(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Cannot execute JUMP/exit false or stack underflow")))
            elif (d_331_opcode_) == (EVMConstants.default__.JUMPI):
                if ((s).Size()) >= (2):
                    source35_ = (s).Peek(0)
                    if source35_.is_Value:
                        d_335___mcc_h74_ = source35_.v
                        d_336_v_ = d_335___mcc_h74_
                        if cond:
                            return ((s).PopN(2)).Goto(d_336_v_)
                        elif True:
                            return ((s).PopN(2)).Skip(1)
                    elif True:
                        d_337___mcc_h75_ = source35_.s
                        return State.AState_Error(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "JumpI to Random() error")))
                elif True:
                    return State.AState_Error(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Cannot execute JUMPI/strack underflow")))
            elif True:
                return State.AState_Error(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "RJUMPs not implemented")))
        elif source33_.is_RunOp:
            d_338___mcc_h48_ = source33_.name
            d_339___mcc_h49_ = source33_.opcode
            d_340___mcc_h50_ = source33_.minCapacity
            d_341___mcc_h51_ = source33_.minOperands
            d_342___mcc_h52_ = source33_.pushes
            d_343___mcc_h53_ = source33_.pops
            d_344_pops_ = d_343___mcc_h53_
            d_345_pushes_ = d_342___mcc_h52_
            if not(cond):
                return ((s).Push(StackElement.StackElem_Random(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, ""))))).Skip(1)
            elif True:
                return State.AState_Error(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "RunOp error")))
        elif source33_.is_StackOp:
            d_346___mcc_h54_ = source33_.name
            d_347___mcc_h55_ = source33_.opcode
            d_348___mcc_h56_ = source33_.minCapacity
            d_349___mcc_h57_ = source33_.minOperands
            d_350___mcc_h58_ = source33_.pushes
            d_351___mcc_h59_ = source33_.pops
            d_352_pops_ = d_351___mcc_h59_
            d_353_pushes_ = d_350___mcc_h58_
            d_354_opcode_ = d_347___mcc_h55_
            if (((d_354_opcode_) == (EVMConstants.default__.POP)) and (((s).Size()) >= (1))) and (not(cond)):
                return ((s).Pop()).Skip(1)
            elif (((EVMConstants.default__.PUSH0) <= (d_354_opcode_)) and ((d_354_opcode_) <= (EVMConstants.default__.PUSH32))) and (not(cond)):
                return ((s).Push(StackElement.StackElem_Value(default__.GetArgValuePush((self).arg)))).Skip((1) + ((d_354_opcode_) - (EVMConstants.default__.PUSH0)))
            elif ((((EVMConstants.default__.DUP1) <= (d_354_opcode_)) and ((d_354_opcode_) <= (EVMConstants.default__.DUP16))) and (((s).Size()) >= (((d_354_opcode_) - (EVMConstants.default__.DUP1)) + (1)))) and (not(cond)):
                return ((s).Dup(((d_354_opcode_) - (EVMConstants.default__.DUP1)) + (1))).Skip(1)
            elif ((((EVMConstants.default__.SWAP1) <= (d_354_opcode_)) and ((d_354_opcode_) <= (EVMConstants.default__.SWAP16))) and (((s).Size()) > (((d_354_opcode_) - (EVMConstants.default__.SWAP1)) + (1)))) and (not(cond)):
                return ((s).Swap(((d_354_opcode_) - (EVMConstants.default__.SWAP1)) + (1))).Skip(1)
            elif True:
                return State.AState_Error(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Stack Op error")))
        elif source33_.is_LogOp:
            d_355___mcc_h60_ = source33_.name
            d_356___mcc_h61_ = source33_.opcode
            d_357___mcc_h62_ = source33_.minCapacity
            d_358___mcc_h63_ = source33_.minOperands
            d_359___mcc_h64_ = source33_.pushes
            d_360___mcc_h65_ = source33_.pops
            d_361_pops_ = d_360___mcc_h65_
            d_362_pushes_ = d_359___mcc_h64_
            if (((s).Size()) >= (d_361_pops_)) and (not(cond)):
                return ((s).PopN(d_361_pops_)).Skip(1)
            elif True:
                return State.AState_Error(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "LogOp error")))
        elif True:
            d_363___mcc_h66_ = source33_.name
            d_364___mcc_h67_ = source33_.opcode
            d_365___mcc_h68_ = source33_.minCapacity
            d_366___mcc_h69_ = source33_.minOperands
            d_367___mcc_h70_ = source33_.pushes
            d_368___mcc_h71_ = source33_.pops
            d_369_pops_ = d_368___mcc_h71_
            d_370_pushes_ = d_367___mcc_h70_
            if (((s).Size()) >= (d_369_pops_)) and (not(cond)):
                return (((s).PopN(d_369_pops_)).PushNRandom(d_370_pushes_)).Skip(1)
            elif True:
                return State.AState_Error(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "SysOp error")))

    def WPre(self, c):
        source36_ = (self).op
        if source36_.is_ArithOp:
            d_371___mcc_h0_ = source36_.name
            d_372___mcc_h1_ = source36_.opcode
            d_373___mcc_h2_ = source36_.minCapacity
            d_374___mcc_h3_ = source36_.minOperands
            d_375___mcc_h4_ = source36_.pushes
            d_376___mcc_h5_ = source36_.pops
            d_377_pops_ = d_376___mcc_h5_
            d_378_pushes_ = d_375___mcc_h4_
            if (0) in ((c).TrackedPos()):
                return WeakPre.Cond_StFalse()
            elif True:
                def lambda3_(d_380_pos_):
                    return (d_380_pos_) + (1)

                d_379_shiftByOne_ = MiscTypes.default__.Map((c).TrackedPos(), lambda3_)
                return WeakPre.Cond_StCond(d_379_shiftByOne_, (c).TrackedVals())
        elif source36_.is_CompOp:
            d_381___mcc_h6_ = source36_.name
            d_382___mcc_h7_ = source36_.opcode
            d_383___mcc_h8_ = source36_.minCapacity
            d_384___mcc_h9_ = source36_.minOperands
            d_385___mcc_h10_ = source36_.pushes
            d_386___mcc_h11_ = source36_.pops
            d_387_pops_ = d_386___mcc_h11_
            d_388_pushes_ = d_385___mcc_h10_
            if (0) in ((c).TrackedPos()):
                return WeakPre.Cond_StFalse()
            elif True:
                def lambda4_(d_390_pops_, d_391_pushes_):
                    def lambda5_(d_392_pos_):
                        return ((d_392_pos_) + (d_390_pops_)) - (d_391_pushes_)

                    return lambda5_

                d_389_shiftBy_ = MiscTypes.default__.Map((c).TrackedPos(), lambda4_(d_387_pops_, d_388_pushes_))
                return WeakPre.Cond_StCond(d_389_shiftBy_, (c).TrackedVals())
        elif source36_.is_BitwiseOp:
            d_393___mcc_h12_ = source36_.name
            d_394___mcc_h13_ = source36_.opcode
            d_395___mcc_h14_ = source36_.minCapacity
            d_396___mcc_h15_ = source36_.minOperands
            d_397___mcc_h16_ = source36_.pushes
            d_398___mcc_h17_ = source36_.pops
            d_399_pops_ = d_398___mcc_h17_
            d_400_pushes_ = d_397___mcc_h16_
            if (0) in ((c).TrackedPos()):
                return WeakPre.Cond_StFalse()
            elif True:
                def lambda6_(d_402_pops_, d_403_pushes_):
                    def lambda7_(d_404_pos_):
                        return ((d_404_pos_) + (d_402_pops_)) - (d_403_pushes_)

                    return lambda7_

                d_401_shiftBy_ = MiscTypes.default__.Map((c).TrackedPos(), lambda6_(d_399_pops_, d_400_pushes_))
                return WeakPre.Cond_StCond(d_401_shiftBy_, (c).TrackedVals())
        elif source36_.is_KeccakOp:
            d_405___mcc_h18_ = source36_.name
            d_406___mcc_h19_ = source36_.opcode
            d_407___mcc_h20_ = source36_.minCapacity
            d_408___mcc_h21_ = source36_.minOperands
            d_409___mcc_h22_ = source36_.pushes
            d_410___mcc_h23_ = source36_.pops
            d_411_pops_ = d_410___mcc_h23_
            d_412_pushes_ = d_409___mcc_h22_
            if (0) in ((c).TrackedPos()):
                return WeakPre.Cond_StFalse()
            elif True:
                def lambda8_(d_414_pos_):
                    return (d_414_pos_) + (1)

                d_413_shiftByOne_ = MiscTypes.default__.Map((c).TrackedPos(), lambda8_)
                return WeakPre.Cond_StCond(d_413_shiftByOne_, (c).TrackedVals())
        elif source36_.is_EnvOp:
            d_415___mcc_h24_ = source36_.name
            d_416___mcc_h25_ = source36_.opcode
            d_417___mcc_h26_ = source36_.minCapacity
            d_418___mcc_h27_ = source36_.minOperands
            d_419___mcc_h28_ = source36_.pushes
            d_420___mcc_h29_ = source36_.pops
            d_421_pops_ = d_420___mcc_h29_
            d_422_pushes_ = d_419___mcc_h28_
            if ((d_422_pushes_) == (1)) and ((d_421_pops_) == (0)):
                if (0) in ((c).TrackedPos()):
                    return WeakPre.Cond_StFalse()
                elif True:
                    def lambda9_(d_424_pos_):
                        return (d_424_pos_) - (1)

                    d_423_shiftByOne_ = MiscTypes.default__.Map((c).TrackedPos(), lambda9_)
                    return WeakPre.Cond_StCond(d_423_shiftByOne_, (c).TrackedVals())
            elif ((d_422_pushes_) == (1)) and ((d_421_pops_) == (1)):
                if (0) in ((c).TrackedPos()):
                    return WeakPre.Cond_StFalse()
                elif True:
                    return c
            elif True:
                def lambda10_(d_426_pops_, d_427_pushes_):
                    def lambda11_(d_428_pos_):
                        return ((d_428_pos_) + (d_426_pops_)) - (d_427_pushes_)

                    return lambda11_

                d_425_shiftBy_ = MiscTypes.default__.Map((c).TrackedPos(), lambda10_(d_421_pops_, d_422_pushes_))
                return WeakPre.Cond_StCond(d_425_shiftBy_, (c).TrackedVals())
        elif source36_.is_MemOp:
            d_429___mcc_h30_ = source36_.name
            d_430___mcc_h31_ = source36_.opcode
            d_431___mcc_h32_ = source36_.minCapacity
            d_432___mcc_h33_ = source36_.minOperands
            d_433___mcc_h34_ = source36_.pushes
            d_434___mcc_h35_ = source36_.pops
            d_435_pops_ = d_434___mcc_h35_
            d_436_pushes_ = d_433___mcc_h34_
            if (d_436_pushes_) == (0):
                def lambda12_(d_438_pos_):
                    return (d_438_pos_) + (2)

                d_437_shiftByTwo_ = MiscTypes.default__.Map((c).TrackedPos(), lambda12_)
                return WeakPre.Cond_StCond(d_437_shiftByTwo_, (c).TrackedVals())
            elif True:
                if (0) in ((c).TrackedPos()):
                    return WeakPre.Cond_StFalse()
                elif True:
                    return c
        elif source36_.is_StorageOp:
            d_439___mcc_h36_ = source36_.name
            d_440___mcc_h37_ = source36_.opcode
            d_441___mcc_h38_ = source36_.minCapacity
            d_442___mcc_h39_ = source36_.minOperands
            d_443___mcc_h40_ = source36_.pushes
            d_444___mcc_h41_ = source36_.pops
            d_445_pops_ = d_444___mcc_h41_
            d_446_pushes_ = d_443___mcc_h40_
            if (d_446_pushes_) == (0):
                def lambda13_(d_448_pos_):
                    return (d_448_pos_) + (2)

                d_447_shiftByTwo_ = MiscTypes.default__.Map((c).TrackedPos(), lambda13_)
                return WeakPre.Cond_StCond(d_447_shiftByTwo_, (c).TrackedVals())
            elif True:
                if (0) in ((c).TrackedPos()):
                    return WeakPre.Cond_StFalse()
                elif True:
                    return c
        elif source36_.is_JumpOp:
            d_449___mcc_h42_ = source36_.name
            d_450___mcc_h43_ = source36_.opcode
            d_451___mcc_h44_ = source36_.minCapacity
            d_452___mcc_h45_ = source36_.minOperands
            d_453___mcc_h46_ = source36_.pushes
            d_454___mcc_h47_ = source36_.pops
            d_455_opcode_ = d_450___mcc_h43_
            if (d_455_opcode_) == (EVMConstants.default__.JUMPDEST):
                return c
            elif ((EVMConstants.default__.JUMP) <= (d_455_opcode_)) and ((d_455_opcode_) <= (EVMConstants.default__.JUMPI)):
                d_456_k_ = ((d_455_opcode_) - (EVMConstants.default__.JUMP)) + (1)
                def lambda14_(d_458_k_):
                    def lambda15_(d_459_pos_):
                        return (d_459_pos_) + (d_458_k_)

                    return lambda15_

                d_457_shiftBy_ = MiscTypes.default__.Map((c).TrackedPos(), lambda14_(d_456_k_))
                return WeakPre.Cond_StCond(d_457_shiftBy_, (c).TrackedVals())
            elif True:
                return WeakPre.Cond_StFalse()
        elif source36_.is_RunOp:
            d_460___mcc_h48_ = source36_.name
            d_461___mcc_h49_ = source36_.opcode
            d_462___mcc_h50_ = source36_.minCapacity
            d_463___mcc_h51_ = source36_.minOperands
            d_464___mcc_h52_ = source36_.pushes
            d_465___mcc_h53_ = source36_.pops
            d_466_opcode_ = d_461___mcc_h49_
            if (0) in ((c).TrackedPos()):
                return WeakPre.Cond_StFalse()
            elif True:
                def lambda16_(d_468_pos_):
                    return (d_468_pos_) - (1)

                d_467_shiftByOne_ = MiscTypes.default__.Map((c).TrackedPos(), lambda16_)
                return WeakPre.Cond_StCond(d_467_shiftByOne_, (c).TrackedVals())
        elif source36_.is_StackOp:
            d_469___mcc_h54_ = source36_.name
            d_470___mcc_h55_ = source36_.opcode
            d_471___mcc_h56_ = source36_.minCapacity
            d_472___mcc_h57_ = source36_.minOperands
            d_473___mcc_h58_ = source36_.pushes
            d_474___mcc_h59_ = source36_.pops
            d_475_opcode_ = d_470___mcc_h55_
            if ((EVMConstants.default__.PUSH0) <= (d_475_opcode_)) and ((d_475_opcode_) <= (EVMConstants.default__.PUSH32)):
                source37_ = MiscTypes.default__.Find((c).TrackedPos(), 0)
                if source37_.is_None:
                    def lambda17_(d_477_pos_):
                        return (d_477_pos_) - (1)

                    d_476_shiftByMinusOne_ = MiscTypes.default__.Map((c).TrackedPos(), lambda17_)
                    return WeakPre.Cond_StCond(d_476_shiftByMinusOne_, (c).TrackedVals())
                elif True:
                    d_478___mcc_h72_ = source37_.v
                    d_479_i_ = d_478___mcc_h72_
                    d_480_argVal_ = Hex.default__.HexToU256((_dafny.SeqWithoutIsStrInference([_dafny.CodePoint('0') for d_481___v157_ in range((64) - (len((self).arg)))])) + ((self).arg))
                    if ((c).TrackedValAt(d_479_i_)) == ((d_480_argVal_).Extract()):
                        d_482_filtered_ = (_dafny.SeqWithoutIsStrInference(((c).TrackedPos())[:d_479_i_:])) + (_dafny.SeqWithoutIsStrInference(((c).TrackedPos())[(d_479_i_) + (1)::]))
                        if (len(d_482_filtered_)) == (0):
                            return WeakPre.Cond_StTrue()
                        elif True:
                            def lambda18_(d_484_pos_):
                                return (d_484_pos_) - (1)

                            d_483_shiftByMinusOne_ = MiscTypes.default__.Map(d_482_filtered_, lambda18_)
                            return WeakPre.Cond_StCond(d_483_shiftByMinusOne_, (_dafny.SeqWithoutIsStrInference(((c).TrackedVals())[:d_479_i_:])) + (_dafny.SeqWithoutIsStrInference(((c).TrackedVals())[(d_479_i_) + (1)::])))
                    elif True:
                        return WeakPre.Cond_StFalse()
            elif ((EVMConstants.default__.DUP1) <= (d_475_opcode_)) and ((d_475_opcode_) <= (EVMConstants.default__.DUP16)):
                source38_ = MiscTypes.default__.Find((c).TrackedPos(), 0)
                if source38_.is_None:
                    def lambda19_(d_486_pos_):
                        return (d_486_pos_) - (1)

                    d_485_shiftByMinusOneButZero_ = MiscTypes.default__.Map((c).TrackedPos(), lambda19_)
                    return WeakPre.Cond_StCond(d_485_shiftByMinusOneButZero_, (c).TrackedVals())
                elif True:
                    d_487___mcc_h73_ = source38_.v
                    d_488_index0_ = d_487___mcc_h73_
                    source39_ = MiscTypes.default__.Find((c).TrackedPos(), ((d_475_opcode_) - (EVMConstants.default__.DUP1)) + (1))
                    if source39_.is_None:
                        def lambda20_(d_490_opcode_):
                            def lambda21_(d_491_pos_):
                                return ((d_490_opcode_) - (EVMConstants.default__.DUP1) if (d_491_pos_) == (0) else (d_491_pos_) - (1))

                            return lambda21_

                        d_489_shiftByMinusOneButZero_ = MiscTypes.default__.Map((c).TrackedPos(), lambda20_(d_475_opcode_))
                        return WeakPre.Cond_StCond(d_489_shiftByMinusOneButZero_, (c).TrackedVals())
                    elif True:
                        d_492___mcc_h74_ = source39_.v
                        d_493_index_ = d_492___mcc_h74_
                        if ((c).TrackedValAt(d_488_index0_)) == ((c).TrackedValAt(d_493_index_)):
                            d_494_filtered_ = (_dafny.SeqWithoutIsStrInference(((c).TrackedPos())[:d_488_index0_:])) + (_dafny.SeqWithoutIsStrInference(((c).TrackedPos())[(d_488_index0_) + (1)::]))
                            def lambda22_(d_496_pos_):
                                return (d_496_pos_) - (1)

                            d_495_shiftByMinusOne_ = MiscTypes.default__.Map(d_494_filtered_, lambda22_)
                            return WeakPre.Cond_StCond(d_495_shiftByMinusOne_, (_dafny.SeqWithoutIsStrInference(((c).TrackedVals())[:d_488_index0_:])) + (_dafny.SeqWithoutIsStrInference(((c).TrackedVals())[(d_488_index0_) + (1)::])))
                        elif True:
                            return WeakPre.Cond_StFalse()
            elif ((EVMConstants.default__.SWAP1) <= (d_475_opcode_)) and ((d_475_opcode_) <= (EVMConstants.default__.SWAP16)):
                d_497_k_ = ((d_475_opcode_) - (EVMConstants.default__.SWAP1)) + (1)
                def lambda23_(d_499_k_):
                    def lambda24_(d_500_pos_):
                        return (d_499_k_ if (d_500_pos_) == (0) else (0 if (d_500_pos_) == (d_499_k_) else d_500_pos_))

                    return lambda24_

                d_498_swapZeroAndk_ = MiscTypes.default__.Map((c).TrackedPos(), lambda23_(d_497_k_))
                return WeakPre.Cond_StCond(d_498_swapZeroAndk_, (c).TrackedVals())
            elif True:
                def lambda25_(d_502_i_):
                    return (d_502_i_) + (1)

                d_501_shiftByOne_ = MiscTypes.default__.Map((c).TrackedPos(), lambda25_)
                return WeakPre.Cond_StCond(d_501_shiftByOne_, (c).TrackedVals())
        elif source36_.is_LogOp:
            d_503___mcc_h60_ = source36_.name
            d_504___mcc_h61_ = source36_.opcode
            d_505___mcc_h62_ = source36_.minCapacity
            d_506___mcc_h63_ = source36_.minOperands
            d_507___mcc_h64_ = source36_.pushes
            d_508___mcc_h65_ = source36_.pops
            d_509_pops_ = d_508___mcc_h65_
            d_510_pushes_ = d_507___mcc_h64_
            d_511_opcode_ = d_504___mcc_h61_
            def lambda26_(d_513_pops_):
                def lambda27_(d_514_pos_):
                    return (d_514_pos_) + (d_513_pops_)

                return lambda27_

            d_512_shiftBy_ = MiscTypes.default__.Map((c).TrackedPos(), lambda26_(d_509_pops_))
            return WeakPre.Cond_StCond(d_512_shiftBy_, (c).TrackedVals())
        elif True:
            d_515___mcc_h66_ = source36_.name
            d_516___mcc_h67_ = source36_.opcode
            d_517___mcc_h68_ = source36_.minCapacity
            d_518___mcc_h69_ = source36_.minOperands
            d_519___mcc_h70_ = source36_.pushes
            d_520___mcc_h71_ = source36_.pops
            d_521_pops_ = d_520___mcc_h71_
            d_522_pushes_ = d_519___mcc_h70_
            d_523_opcode_ = d_516___mcc_h67_
            if (d_522_pushes_) == (0):
                def lambda28_(d_525_pops_):
                    def lambda29_(d_526_pos_):
                        return (d_526_pos_) + (d_525_pops_)

                    return lambda29_

                d_524_shiftBy_ = MiscTypes.default__.Map((c).TrackedPos(), lambda28_(d_521_pops_))
                return WeakPre.Cond_StCond(d_524_shiftBy_, (c).TrackedVals())
            elif True:
                if (0) in ((c).TrackedPos()):
                    return WeakPre.Cond_StFalse()
                elif True:
                    def lambda30_(d_528_pops_):
                        def lambda31_(d_529_pos_):
                            return (d_529_pos_) + (d_528_pops_)

                        return lambda31_

                    d_527_shiftBy_ = MiscTypes.default__.Map((c).TrackedPos(), lambda30_(d_521_pops_))
                    return WeakPre.Cond_StCond(d_527_shiftBy_, (c).TrackedVals())


class Instruction_Instruction(Instruction, NamedTuple('Instruction', [('op', Any), ('arg', Any), ('address', Any)])):
    def __dafnystr__(self) -> str:
        return f'Instructions.Instruction.Instruction({_dafny.string_of(self.op)}, {self.arg.VerbatimString(True)}, {_dafny.string_of(self.address)})'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Instruction_Instruction) and self.op == __o.op and self.arg == __o.arg and self.address == __o.address
    def __hash__(self) -> int:
        return super().__hash__()

