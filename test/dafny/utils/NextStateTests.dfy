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


include "../../../src/dafny/utils/State.dfy"
include "../../../src/dafny/utils/Instructions.dfy"
  // include "../utils/MiscTypes.dfy"
include "../../../src/dafny/disassembler/OpcodeDecoder.dfy"
include "../../../src/dafny/utils/int.dfy"
  // include "../../../src/dafny/disassembler/OpcodeDecoder.dfy"

/**
  * Test correct computation of back propagation of a given position.
  * 
  */
module PosTrackerTests {

  //   import opened EVMOpcodes
  import opened MiscTypes
  import opened OpcodeDecoder
  import opened EVMConstants
  import opened Instructions
  import Int
  import opened State

  /** Arithmetic instruction. Proofs. */
  method Ariths(k: nat, op: Int.u8, s: ValidState)
    requires ADD <= op <= SIGNEXTEND
  {
    {
      var i := Instruction(Decode(op));
      assert i.NextState(s, true).Error?;
    }
    {
      var i := Instruction(Decode(op));
      if s.Size() >= 2 {
        assert i.NextState(s, false).EState?;
        assert i.NextState(s, false).PC() == s.PC() + 1;
        assert i.NextState(s, false).Size() == s.Size() - 1;
        assert i.NextState(s, false).stack[1..] == s.stack[2..];
      } else {
        assert i.NextState(s, false).Error?;
      }
    }
  }

  /** Concrete tests. */
  method {:test} ArithsTests()
  {
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := [Random(), Random()]);
      var i := Instruction(Decode(ADD));
      expect i.NextState(s, false).EState?;
      expect i.NextState(s, true).Error?;
      expect  i.NextState(s, false).pc == 5;
    }
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := [Random()]);
      var i := Instruction(Decode(SIGNEXTEND));
      expect i.NextState(s, true).Error?;
      expect i.NextState(s, false).Error?;
    }
  }

  /** Comparison instructions. */
  method Comps1(k: nat, op: Int.u8)
    requires LT <= op <= ISZERO
  {
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := [Random()]);
      var i := Instruction(Decode(op));
      assert i.NextState(s, true).Error?;
      assert op != ISZERO ==>  i.NextState(s, false).Error?;
    }
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := [Random(), Random()]);
      var i := Instruction(Decode(op));
      assert i.NextState(s, true).Error?;
      assert i.NextState(s, false).EState?;
    }
  }


  /** Concrete tests. */
  method {:test} CompsTests()
  {
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := [Random()]);
      var i := Instruction(Decode(LT));
      assert i.NextState(s, true).Error?;
    }
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := [Random(), Value(10)]);
      var i := Instruction(Decode(LT));
      assert i.NextState(s, true).Error?;
      assert i.NextState(s, false).EState?;
      expect  i.NextState(s, false).pc == 5;
    }

    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := [Random()]);
      var i := Instruction(Decode(ISZERO));
      assert i.NextState(s, true).Error?;
      assert i.NextState(s, false).EState?;
      expect  i.NextState(s, false).pc == 5;
    }
  }

  method {:test} BitWiseTests()
  {
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := [Random()]);
      var i := Instruction(Decode(AND));
      assert i.NextState(s, true).Error?;
    }
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := [Random(), Value(10)]);
      var i := Instruction(Decode(OR));
      assert i.NextState(s, true).Error?;
      assert i.NextState(s, false).EState?;
      expect  i.NextState(s, false).pc == 5;
      expect  i.NextState(s, false).Peek(0) == Random();
    }

    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := [Random()]);
      var i := Instruction(Decode(NOT));
      assert i.NextState(s, true).Error?;
      assert i.NextState(s, false).EState?;
      expect  i.NextState(s, false).pc == 5;
      expect  i.NextState(s, false).Peek(0) == Random();
    }
  }

  method {:test} KeccakTests()
  {
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := [Random()]);
      var i := Instruction(Decode(KECCAK256));
      assert i.NextState(s, false).Error?;
      assert i.NextState(s, true).Error?;
    }
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := [Random(), Random()]);
      var i := Instruction(Decode(KECCAK256));
      assert i.NextState(s, false).EState?;
      assert i.NextState(s, false).pc == 5;
      assert i.NextState(s, false).Peek(0) == Random();
      assert i.NextState(s, true).Error?;
    }
  }

  method {:test} EnvTests()
  {
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := [Random()]);
      var i := Instruction(Decode(ADDRESS));
      expect i.NextState(s, false).EState?;
      expect i.NextState(s, false).pc == 5;
      expect i.NextState(s, false).Peek(0) == Random();
      expect i.NextState(s, true).Error?;
    }
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := [Random()]);
      var i := Instruction(Decode(BASEFEE));
      expect i.NextState(s, false).EState?;
      expect i.NextState(s, false).pc == 5;
      expect i.NextState(s, false).Peek(0) == Random();
      expect i.NextState(s, true).Error?;
    }
  }

  method {:test} MemTests()
  {
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := [Random(), Random()]);
      var i := Instruction(Decode(MSTORE));
      expect i.NextState(s, false).EState?;
      expect i.NextState(s, false).pc == 5;
      expect i.NextState(s, false).Peek(0) == Random();
      expect i.NextState(s, true).Error?;
    }
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := [Random()]);
      var i := Instruction(Decode(MSTORE8));
      expect i.NextState(s, false).Error?;
      expect i.NextState(s, true).Error?;
    }
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := [Random()]);
      var i := Instruction(Decode(MLOAD));
      expect i.NextState(s, false).EState?;
      expect i.NextState(s, false).pc == 5;
      expect i.NextState(s, false).Peek(0) == Random();
      expect i.NextState(s, true).Error?;
    }
  }

  method {:test} StorageTests()
  {
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := [Random(), Random()]);
      var i := Instruction(Decode(SSTORE));
      expect i.NextState(s, false).EState?;
      expect i.NextState(s, false).pc == 5;
      expect i.NextState(s, false).Peek(0) == Random();
      expect i.NextState(s, true).Error?;
    }
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := [Random()]);
      var i := Instruction(Decode(SSTORE));
      expect i.NextState(s, false).Error?;
      expect i.NextState(s, true).Error?;
    }
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := [Random()]);
      var i := Instruction(Decode(SLOAD));
      expect i.NextState(s, false).EState?;
      expect i.NextState(s, false).pc == 5;
      expect i.NextState(s, false).Peek(0) == Random();
      expect i.NextState(s, true).Error?;
    }
  }

  method {:test} RunTests()
  {
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := []);
      var i := Instruction(Decode(PC));
      expect i.NextState(s, false).EState?;
      expect i.NextState(s, false).pc == 5;
      expect i.NextState(s, false).Peek(0) == Random();
      expect i.NextState(s, true).Error?;
    }
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := []);
      var i := Instruction(Decode(GAS));
      expect i.NextState(s, false).EState?;
      expect i.NextState(s, false).pc == 5;
      expect i.NextState(s, false).Peek(0) == Random();
      expect i.NextState(s, true).Error?;
    }
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := []);
      var i := Instruction(Decode(MSIZE));
      expect i.NextState(s, false).EState?;
      expect i.NextState(s, false).pc == 5;
      expect i.NextState(s, false).Peek(0) == Random();
      expect i.NextState(s, true).Error?;
    }
  }

  /**   Jump instructions.
    *   Reminder: jump woth condition false is an error.
    *   Only true condition is valid for JUMP.
    */
  method {:test} Jumps()
  {
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := [Random()]);
      var i := Instruction(Decode(JUMP));
      expect i.NextState(s, true).Error?;
      expect i.NextState(s, false).Error?;
    }
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := []);
      var i := Instruction(Decode(JUMP));
      expect i.NextState(s, true).Error?;
      expect i.NextState(s, false).Error?;
    }
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := [Value(10), Random()]);
      var i := Instruction(Decode(JUMP));
      expect i.NextState(s, true).EState?;
      expect i.NextState(s, false).Error?;
      expect i.NextState(s, true).pc == 10;
    }
  }

  method {:test} JumpDests()
  {
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := []);
      var i := Instruction(Decode(JUMPDEST));
      expect i.NextState(s, true).Error?;
      expect i.NextState(s, false).EState?;
      expect i.NextState(s, false).pc == 5;
    }
  }

  method {:test} JumpIs()
  {
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := []);
      var i := Instruction(Decode(JUMPI));
      expect i.NextState(s, true).Error?;
      expect i.NextState(s, false).Error?;
    }
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := [Value(1)]);
      var i := Instruction(Decode(JUMPI));
      expect i.NextState(s, true).Error?;
      expect i.NextState(s, false).Error?;
    }
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := [Random(), Random()]);
      var i := Instruction(Decode(JUMPI));
      expect i.NextState(s, true).Error?;
      expect i.NextState(s, false).Error?;
    }
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := [Value(10), Random()]);
      var i := Instruction(Decode(JUMPI));
      expect i.NextState(s, true).EState?;
      expect i.NextState(s, true).pc == 10;
      expect i.NextState(s, false).EState?;
      expect i.NextState(s, false).pc == 5;
    }
  }

  method {:test} RJumps()
  {
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := []);
      var i := Instruction(Decode(RJUMPI));
      expect i.NextState(s, true).Error?;
      expect i.NextState(s, false).Error?;
    }
    {
      var s := DEFAULT_VALIDSTATE.(pc := 4, stack := []);
      var i := Instruction(Decode(RJUMPV));
      expect i.NextState(s, true).Error?;
      expect i.NextState(s, false).Error?;
    }
  }

}

