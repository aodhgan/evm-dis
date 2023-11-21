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
import Instructions
import BinaryDecoder
import LinSegments
import Splitter
import SegBuilder
import ProofObject
import PrettyIns
import PrettyPrinters
import ProofObjectBuilder
import ArgParser
import SeqOfSets
import PartitionMod
import Automata
import Minimiser
import CFGraph
import LoopResolver
import BuildCFGraph

# Module: Driver

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def Main(args):
        d_811_optionParser_: ArgParser.ArgumentParser
        nw1_ = ArgParser.ArgumentParser()
        nw1_.ctor__(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "<string>")))
        d_811_optionParser_ = nw1_
        (d_811_optionParser_).AddOption(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "-d")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "--dis")), 0, _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Disassemble <string>")))
        (d_811_optionParser_).AddOption(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "-p")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "--proof")), 0, _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Generate proof object for <string>")))
        (d_811_optionParser_).AddOption(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "-s")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "--segment")), 0, _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Print segment of <string>")))
        (d_811_optionParser_).AddOption(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "-a")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "--all")), 0, _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Same as -d -p")))
        (d_811_optionParser_).AddOption(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "-l")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "--lib")), 1, _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "The path to the Dafny-EVM source code. Used to add includes files in the proof object. ")))
        (d_811_optionParser_).AddOption(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "-c")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "--cfg")), 1, _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Max depth. Control flow graph in DOT format")))
        (d_811_optionParser_).AddOption(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "-r")), _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "--raw")), 1, _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Display non-minimised and minimised CFGs")))
        if ((len(args)) < (2)) or (((args)[1]) == (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "--help")))):
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Not enough arguments\n"))).VerbatimString(False))
            (d_811_optionParser_).PrintHelp()
        elif (len(args)) == (2):
            d_812_x_: _dafny.Seq
            d_812_x_ = BinaryDecoder.default__.Disassemble((args)[1], _dafny.SeqWithoutIsStrInference([]), 0)
            PrettyPrinters.default__.PrintInstructions(d_812_x_)
        elif (((args)[1]) == (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "--help")))) or (((args)[1]) == (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "-h")))):
            (d_811_optionParser_).PrintHelp()
        elif True:
            d_813_stringToProcess_: _dafny.Seq
            d_813_stringToProcess_ = (args)[(len(args)) - (1)]
            d_814_optArgs_: _dafny.Seq
            d_814_optArgs_ = _dafny.SeqWithoutIsStrInference((args)[1:(len(args)) - (1):])
            d_815_x_: _dafny.Seq
            d_815_x_ = BinaryDecoder.default__.Disassemble(d_813_stringToProcess_, _dafny.SeqWithoutIsStrInference([]), 0)
            source67_ = (d_811_optionParser_).GetArgs(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "--dis")), d_814_optArgs_)
            if source67_.is_Success:
                d_816___mcc_h0_ = source67_.v
                PrettyPrinters.default__.PrintInstructions(d_815_x_)
            elif True:
                d_817___mcc_h1_ = source67_.msg
                pass
            source68_ = (d_811_optionParser_).GetArgs(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "--segment")), d_814_optArgs_)
            if source68_.is_Success:
                d_818___mcc_h2_ = source68_.v
                _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Segments:\n"))).VerbatimString(False))
                d_819_y_: _dafny.Seq
                d_819_y_ = Splitter.default__.SplitUpToTerminal(d_815_x_, _dafny.SeqWithoutIsStrInference([]), _dafny.SeqWithoutIsStrInference([]))
                PrettyPrinters.default__.PrintSegments(d_819_y_, 0)
            elif True:
                d_820___mcc_h3_ = source68_.msg
                pass
            source69_ = (d_811_optionParser_).GetArgs(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "--proof")), d_814_optArgs_)
            if source69_.is_Success:
                d_821___mcc_h4_ = source69_.v
                d_822_pathToDafnyLib_: _dafny.Seq
                def lambda41_(source70_):
                    if source70_.is_Success:
                        d_823___mcc_h6_ = source70_.v
                        def iife45_(_pat_let22_0):
                            def iife46_(d_824_p_):
                                return (d_824_p_)[0]
                            return iife46_(_pat_let22_0)
                        return iife45_(d_823___mcc_h6_)
                    elif True:
                        d_825___mcc_h7_ = source70_.msg
                        return _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, ""))

                d_822_pathToDafnyLib_ = lambda41_((d_811_optionParser_).GetArgs(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "--lib")), d_814_optArgs_))
                d_826_y_: _dafny.Seq
                d_826_y_ = Splitter.default__.SplitUpToTerminal(d_815_x_, _dafny.SeqWithoutIsStrInference([]), _dafny.SeqWithoutIsStrInference([]))
                d_827_z_: _dafny.Seq
                d_827_z_ = ProofObjectBuilder.default__.BuildProofObject(d_826_y_)
                PrettyPrinters.default__.PrintProofObjectToDafny(d_827_z_, d_822_pathToDafnyLib_)
            elif True:
                d_828___mcc_h5_ = source69_.msg
                pass
            source71_ = (d_811_optionParser_).GetArgs(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "--all")), d_814_optArgs_)
            if source71_.is_Success:
                d_829___mcc_h8_ = source71_.v
                PrettyPrinters.default__.PrintInstructions(d_815_x_)
                d_830_pathToDafnyLib_: _dafny.Seq
                def lambda42_(source72_):
                    if source72_.is_Success:
                        d_831___mcc_h10_ = source72_.v
                        def iife47_(_pat_let23_0):
                            def iife48_(d_832_p_):
                                return (d_832_p_)[0]
                            return iife48_(_pat_let23_0)
                        return iife47_(d_831___mcc_h10_)
                    elif True:
                        d_833___mcc_h11_ = source72_.msg
                        return _dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, ""))

                d_830_pathToDafnyLib_ = lambda42_((d_811_optionParser_).GetArgs(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "--lib")), d_814_optArgs_))
                d_834_y_: _dafny.Seq
                d_834_y_ = Splitter.default__.SplitUpToTerminal(d_815_x_, _dafny.SeqWithoutIsStrInference([]), _dafny.SeqWithoutIsStrInference([]))
                d_835_z_: _dafny.Seq
                d_835_z_ = ProofObjectBuilder.default__.BuildProofObject(d_834_y_)
                PrettyPrinters.default__.PrintProofObjectToDafny(d_835_z_, d_830_pathToDafnyLib_)
            elif True:
                d_836___mcc_h9_ = source71_.msg
                pass
            source73_ = (d_811_optionParser_).GetArgs(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "--cfg")), d_814_optArgs_)
            if source73_.is_Success:
                d_837___mcc_h12_ = source73_.v
                d_838_m_ = d_837___mcc_h12_
                _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "CFG:\n"))).VerbatimString(False))
                d_839_y_: _dafny.Seq
                d_839_y_ = Splitter.default__.SplitUpToTerminal(d_815_x_, _dafny.SeqWithoutIsStrInference([]), _dafny.SeqWithoutIsStrInference([]))
                if (len(d_839_y_)) == (0):
                    _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "No segment found\n"))).VerbatimString(False))
                elif ((len((d_838_m_)[0])) == (0)) or (not(default__.IsNatNumber((d_838_m_)[0]))):
                    _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Argument to --cfg is not a nat.\n"))).VerbatimString(False))
                elif True:
                    d_840_maxDepth_: int
                    d_840_maxDepth_ = default__.StringToNat((d_838_m_)[0], 0)
                    _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "maxDepth is:"))).VerbatimString(False))
                    _dafny.print(_dafny.string_of(d_840_maxDepth_))
                    _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n"))).VerbatimString(False))
                    d_841_startAddress_: int
                    d_841_startAddress_ = ((d_839_y_)[0]).StartAddress()
                    pat_let_tv47_ = d_841_startAddress_
                    d_842_startState_: State.AState
                    def iife49_(_pat_let24_0):
                        def iife50_(d_843_dt__update__tmp_h0_):
                            def iife51_(_pat_let25_0):
                                def iife52_(d_844_dt__update_hpc_h0_):
                                    return State.AState_EState(d_844_dt__update_hpc_h0_, (d_843_dt__update__tmp_h0_).stack)
                                return iife52_(_pat_let25_0)
                            return iife51_(pat_let_tv47_)
                        return iife50_(_pat_let24_0)
                    d_842_startState_ = iife49_(State.default__.DEFAULT__VALIDSTATE)
                    if (((d_839_y_)[0]).StartAddress()) != (0):
                        _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Segment 0 does not start at address 0.\n"))).VerbatimString(False))
                    elif True:
                        d_845_g_: CFGraph.BoolCFGraph
                        d_845_g_ = BuildCFGraph.default__.BuildCFGV4(d_839_y_, d_840_maxDepth_, 0, State.default__.DEFAULT__VALIDSTATE, _dafny.SeqWithoutIsStrInference([CFGraph.CFGNode_CFGNode(_dafny.SeqWithoutIsStrInference([]), MiscTypes.Option_Some(0))]), _dafny.SeqWithoutIsStrInference([0]), _dafny.SeqWithoutIsStrInference([]))
                        if ((d_811_optionParser_).GetArgs(_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "--raw")), d_814_optArgs_)).is_Success:
                            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Raw CFG\n"))).VerbatimString(False))
                            _dafny.print(((d_845_g_).DOTPrint(d_839_y_)).VerbatimString(False))
                        _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Computing Minimised CFG\n"))).VerbatimString(False))
                        d_846_g_k_: CFGraph.BoolCFGraph
                        d_846_g_k_ = (d_845_g_).Minimise()
                        if not((d_846_g_k_).IsValid()):
                            raise _dafny.HaltException("src/dafny/Driver.dfy(138,14): " + (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "expectation violation"))).VerbatimString(False))
                        _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "Minimised CFG\n"))).VerbatimString(False))
                        _dafny.print(((d_846_g_k_).DOTPrint(d_839_y_)).VerbatimString(False))
            elif True:
                d_847___mcc_h13_ = source73_.msg
                pass

    @staticmethod
    def CharToDigit(c):
        if (c) == (_dafny.CodePoint('0')):
            return MiscTypes.Option_Some(0)
        elif (c) == (_dafny.CodePoint('1')):
            return MiscTypes.Option_Some(1)
        elif (c) == (_dafny.CodePoint('2')):
            return MiscTypes.Option_Some(2)
        elif (c) == (_dafny.CodePoint('3')):
            return MiscTypes.Option_Some(3)
        elif (c) == (_dafny.CodePoint('4')):
            return MiscTypes.Option_Some(4)
        elif (c) == (_dafny.CodePoint('5')):
            return MiscTypes.Option_Some(5)
        elif (c) == (_dafny.CodePoint('6')):
            return MiscTypes.Option_Some(6)
        elif (c) == (_dafny.CodePoint('7')):
            return MiscTypes.Option_Some(7)
        elif (c) == (_dafny.CodePoint('8')):
            return MiscTypes.Option_Some(8)
        elif (c) == (_dafny.CodePoint('9')):
            return MiscTypes.Option_Some(9)
        elif True:
            return MiscTypes.Option_None()

    @staticmethod
    def IsNatNumber(s):
        while True:
            with _dafny.label():
                if (len(s)) == (1):
                    return (default__.CharToDigit((s)[0])).is_Some
                elif True:
                    source74_ = default__.CharToDigit((s)[0])
                    if source74_.is_None:
                        return False
                    elif True:
                        d_848___mcc_h0_ = source74_.v
                        d_849_v_ = d_848___mcc_h0_
                        in142_ = _dafny.SeqWithoutIsStrInference((s)[1::])
                        s = in142_
                        raise _dafny.TailCall()
                break

    @staticmethod
    def StringToNat(s, lastVal):
        if (len(s)) == (1):
            return (default__.CharToDigit((s)[0])).v
        elif True:
            d_850_v_ = (default__.CharToDigit((s)[(len(s)) - (1)])).v
            return (d_850_v_) + ((10) * (default__.StringToNat(_dafny.SeqWithoutIsStrInference((s)[:(len(s)) - (1):]), 0)))

