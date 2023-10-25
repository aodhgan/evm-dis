/*
 * Copyright 2023 Franck Cassez
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software dis-
 * tributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

include "./int.dfy"
include "../utils/MiscTypes.dfy"
include "./OpcodesConstants.dfy"
  /**
    *  Provides EVM Opcodes.
    */
module EVMOpcodes {

  import opened Int
  import opened MiscTypes
  import opened EVMConstants

  /**
    * The different types of Opcodes supported by the EVM.
    */
  datatype Opcode =
    | ArithOp(name: string, opcode: u8, minCapacity: nat := 0,
              minOperands: nat := 2, pushes: nat := 1, pops: nat := 2)
    | CompOp(name: string, opcode: u8, minCapacity: nat := 0,
             minOperands: nat := 2, pushes: nat := 1, pops: nat := 2)
    | BitwiseOp(name: string, opcode: u8, minCapacity: nat := 0,
                minOperands: nat := 2, pushes: nat := 1, pops: nat := 2)
    | KeccakOp(name: string, opcode: u8, minCapacity: nat := 0,
               minOperands: nat := 2, pushes: nat := 1, pops: nat := 2)
    | EnvOp(name: string, opcode: u8, minCapacity: nat := 1,
            minOperands: nat := 0, pushes: nat := 1, pops: nat := 0)
    | MemOp(name: string, opcode: u8, minCapacity: nat := 0,
            minOperands: nat := 0, pushes: nat := 0, pops: nat := 0)
    | StorageOp(name: string, opcode: u8, minCapacity: nat := 0,
                minOperands: nat := 0, pushes: nat := 0, pops: nat := 0)
    | JumpOp(name: string, opcode: u8, minCapacity: nat := 0,
             minOperands: nat := 0, pushes: nat := 0, pops: nat := 0)
    | RunOp(name: string, opcode: u8, minCapacity: nat := 0,
            minOperands: nat := 0, pushes: nat := 0, pops: nat := 0)
    | StackOp(name: string, opcode: u8, minCapacity: nat := 0,
              minOperands: nat := 0, pushes: nat := 0, pops: nat := 0)
    | LogOp(name: string, opcode: u8, minCapacity: nat := 0,
            minOperands: nat := 0, pushes: nat := 0, pops: nat := 0)
    | SysOp(name: string, opcode: u8, minCapacity: nat := 0,
            minOperands: nat := 0, pushes: nat := 0, pops: nat := 0)
  {

    predicate IsValid()
    {
      match this
      case ArithOp(_, op, _, _, _, _)     => ADD <= op <= SIGNEXTEND
      case CompOp(_, op, _, _, _, _)      => LT <= op <= ISZERO
      case BitwiseOp(_, op, _, _, _, _)   => AND <= op <= SAR
      case KeccakOp(_, op, _, _, _, _)    => op == KECCAK256
      case EnvOp(_, op, _, _, _, _)       => ADDRESS <= op <= BASEFEE
      case MemOp(_, op, _, _, _, _)       => MLOAD <= op <= MSTORE8
      case StorageOp(_, op, _, _, _, _)   => SLOAD <= op <= SSTORE
      case JumpOp(_, op, _, _, _, _)      => JUMP <= op <= JUMPI || JUMPDEST <= op <= RJUMPV
      case RunOp(_, op, _, _, _, _)       => PC <= op <= GAS
      case StackOp(_, op, _, _, _, _)     => op == POP || PUSH0 <= op <= SWAP16
      case LogOp(_, op, _, _, _, _)       => LOG0 <= op <= LOG4
      case SysOp(_, op, _, _, _, _)       => op == STOP || op == EOF || CREATE <= op <= SELFDESTRUCT
    }
    // Helpers

    /**
      * The expected number of u8 arguments for an opcode.
      * @note   Only `PUSHk` instructions have arguments, and `PUSHk` has
      *         exactly k u8 arguments.
      */
    function Args(): nat
      ensures 0 <= Args() <= 32
    {
      if PUSH1 <= opcode <= PUSH32 then (opcode - PUSH0) as nat
      else 0
    }

    /**
      * Whether an opcode is terminal (branching).
      */
    predicate IsTerminal()
    {
      match this.opcode
      case STOP   => true
      case JUMP   => true
      case JUMPI  => true
      case RJUMP  => true
      case RJUMPI => true
      case RJUMPV => true
      case RETURN => true
      case REVERT => true
      case _      => false
    }

    /**
      * The readable name of an Opcode.
      */
    function Name(): string
    {
      name
    }

    function StackEffect(): int
    {
      pushes - pops
    }

    /**
      *  Determine the minimum of operands needed before the
      *  instruction is executed to ensure that
      *  1. the instruction does not trigger a Stack underflow
      *  2. there are at least k operands on the stack after execuitng the instruction.
      *
      *  @example    POP: pushes 0, pops 1, minOperands 1
      *              k = 0 => Max(1, 0 -(-1)) = 1 
      *              k = 3 => Max(1, 3 - (- 1)) = 4
      *  @example    SWAP2 pushes 0, pops 0, minOperands 3
      *              k = 0 => r = 0 
      *              k = 1 => r = 1
      *              k => r = k!
      */
    function WeakestPreOperands(post: nat := 0): (r: nat)
    {
      Max(minOperands, post - StackEffect())
    }

    /**
      *  Determine the minimum of capacity needed before the
      *  instruction is executed to ensure that
      *  1. the instruction does not trigger a Stack overflow
      *  2. there are at least k free slots on the stack after executing the instruction.
      *
      *  @example    POP: pushes 0, pops 1, minCapacity = 0
      *              k = 0 => Max(0, 0 + (-1)) = 0
      *              k = 3 => Max(1, 3 + (- 1)) = 2
      *  @example    SWAP2 pushes 0, pops 0, minCapacity = 0
      *              k = 0 => Max(0, 0 + 0) = 0
      *              k = 1 => Max(0, 1 + 0) = 1
      */
    function WeakestPreCapacity(post: nat := 0): (r: nat)
    {
      Max(minCapacity, post + StackEffect())
    }
  }

}