from Redcode import Instruction
from MARS import MARS
from warrior import Warrior
from Validating_tools import WrongOpcodeError, WrongModifierError
from Validating_tools import WrongAddressingModeError
import pytest


def test_Instruction_convert():
    instruction1 = Instruction("ADD.I 4, 3")
    assert instruction1._opcode == "ADD"
    assert instruction1._modifier == "I"
    assert instruction1._A == 4
    assert instruction1._B == 3

    instruction2 = Instruction("          MOV.AB 4, 3")
    assert instruction2._opcode == "MOV"
    assert instruction2._modifier == "AB"
    assert instruction2._A == 4
    assert instruction2._B == 3

    instruction3 = Instruction("      JMP   -4")
    assert instruction3._opcode == "JMP"
    assert instruction3._A == -4

    instruction4 = Instruction("      JMP.BA   -4,  #15")
    assert instruction4._opcode == "JMP"
    assert instruction4._modifier == "BA"
    assert instruction4._A == -4
    assert instruction4._type_A == "$"
    assert instruction4._B == 15
    assert instruction4._type_B == "#"

    instruction5 = Instruction("   DAT @17777")
    assert instruction5._opcode == "DAT"
    assert instruction5._modifier == "F"
    assert instruction5._A == 0
    assert instruction5._type_A == "$"
    assert instruction5._B == 17777
    assert instruction5._type_B == "@"


def test_instruction_set_default_modifier():
    instruction1 = Instruction("ADD 4, #3")
    assert instruction1._opcode == "ADD"
    assert instruction1._modifier == "B"
    assert instruction1._A == 4
    assert instruction1._B == 3

    instruction2 = Instruction("          MOV #4, 3")
    assert instruction2._opcode == "MOV"
    assert instruction2._modifier == "AB"
    assert instruction2._A == 4
    assert instruction2._B == 3

    instruction3 = Instruction("      JMP   -4")
    assert instruction3._opcode == "JMP"
    assert instruction3._A == -4
    assert instruction3._modifier == "B"

    instruction4 = Instruction("      SEQ   *-5,  @15")
    assert instruction4._opcode == "SEQ"
    assert instruction4._modifier == "I"
    assert instruction4._A == -5
    assert instruction4._type_A == "*"
    assert instruction4._B == 15
    assert instruction4._type_B == "@"

    instruction5 = Instruction("DAT -10")
    assert instruction5._opcode == "DAT"
    assert instruction5._modifier == "F"
    assert instruction5._A == 0
    assert instruction5._type_A == "$"
    assert instruction5._B == -10
    assert instruction5._type_B == "$"

    instruction5 = Instruction("NOP #-14")
    assert instruction5._opcode == "NOP"
    assert instruction5._modifier == "F"
    assert instruction5._A == -14
    assert instruction5._type_A == "#"
    assert instruction5._B == 0
    assert instruction5._type_B == "$"


def test_Instruction_validate():
    with pytest.raises(WrongOpcodeError):
        Instruction("BLA.I 4, 3")
    with pytest.raises(WrongModifierError):
        Instruction("MOV.CCC 4, 3")
    with pytest.raises(ValueError):
        Instruction("MOV $, 3")
    with pytest.raises(WrongAddressingModeError):
        Instruction("MOV %5, 3")
    with pytest.raises(WrongAddressingModeError):
        Instruction("MOV (5, 3")
    with pytest.raises(WrongAddressingModeError):
        Instruction("MOV 5, )3")


def test_Instruction_compare():
    instruction1 = Instruction("ADD.I 4, 3")
    instruction2 = Instruction("          MOV.AB 4, 3")
    assert instruction1.compare(instruction2) is False

    instruction3 = Instruction("      JMP.A   -4")
    instruction4 = Instruction("      JMP.A   -4")
    assert instruction3.compare(instruction4)


def test_Instruction_copy():
    instruction1 = Instruction("ADD.I 4, 3")
    instruction2 = instruction1.copy()
    assert instruction1.compare(instruction2)


# Addressing modes:
test_warriors = [Warrior("Warriors/Neutral_warrior.red")]
test_core = MARS(20, 100, test_warriors)
test_core.prepare_for_simulation()
test_core._update_instruction_indexes()


def test_immediate():
    instruction = Instruction("MOV #2, #2")
    instruction._index = 5
    assert instruction.immediate(2) == 5


def test_direct():
    instruction = Instruction("MOV $-70, $2")
    instruction.attach_core(test_core)
    instruction._index = 5
    assert instruction.direct(-70) == 15


def test_A_indirect():
    instruction = Instruction("MOV *-50, $2")
    instruction.attach_core(test_core)
    instruction._index = 5
    assert instruction.A_indirect(-50) == 15


def test_B_indirect():
    instruction = Instruction("MOV @-50, $2")
    instruction.attach_core(test_core)
    instruction._index = 5
    assert instruction.B_indirect(-40) == 5


def test_A_predecrement():
    test_core[5] = Instruction("MOV {-40, $2")
    instruction = test_core[5]
    instruction.attach_core(test_core)
    instruction._index = 5
    assert instruction.A_predecrement(-40) == 4
    assert instruction._A == -41


def test_B_predecrement():
    test_core[5] = Instruction("MOV -40, <20")
    instruction = test_core[5]
    instruction.attach_core(test_core)
    instruction._index = 5
    assert instruction.B_predecrement(20) == 4
    assert instruction._B == 19


def test_A_postincrement():
    test_core[5] = Instruction("MOV }-40, $2")
    instruction = test_core[5]
    instruction.attach_core(test_core)
    instruction._index = 5
    assert instruction.A_postincrement(-40) == 5
    assert instruction._A == -39


def test_B_postincrement():
    test_core[5] = Instruction("MOV -40, >20")
    instruction = test_core[5]
    instruction.attach_core(test_core)
    instruction._index = 5
    assert instruction.B_postincrement(-40) == 5
    assert instruction._B == 21
