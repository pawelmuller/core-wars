from Redcode import Instruction


def test_Instruction_convert():
    instruction1 = Instruction("ADD.I 4, 3")
    assert instruction1._instruction == "ADD"
    assert instruction1._modifier == "I"
    assert instruction1._A == 4
    assert instruction1._B == 3

    instruction2 = Instruction("          MOV.AB 4, 3")
    assert instruction2._instruction == "MOV"
    assert instruction2._modifier == "AB"
    assert instruction2._A == 4
    assert instruction2._B == 3

    instruction3 = Instruction("      JMP   -4")
    assert instruction3._instruction == "JMP"
    assert instruction3._A == -4

    instruction4 = Instruction("      JMP.BA   @-4,  #15")
    assert instruction4._instruction == "JMP"
    assert instruction4._modifier == "BA"
    assert instruction4._A == -4
    assert instruction4._type_A == "@"
    assert instruction4._B == 15
    assert instruction4._type_B == "#"


def test_Instruction_compare():
    instruction1 = Instruction("ADD.I 4, 3")
    instruction2 = Instruction("          MOV.AB 4, 3")
    assert instruction1.compare(instruction2) is False

    instruction3 = Instruction("      JMP.A   -4")
    instruction4 = Instruction("      JMP.A   -4")
    assert instruction3.compare(instruction4)
