from Redcode import Instruction
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
        Instruction("MOV @5, 3")
    with pytest.raises(WrongAddressingModeError):
        Instruction("MOV 5, *3")


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
