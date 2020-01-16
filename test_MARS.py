import pytest
from MARS import MARS
from warrior import Warrior
from Redcode import Instruction


def test_validate_warriors():
    test_warriors = [
        Warrior("Warriors/Dwarf.red") for i in range(100)
    ]
    with pytest.raises(Exception):
        MARS(100, 100, test_warriors)


def test_find_a_place():
    warriors = [Warrior("Warriors/Imp_1.red")]
    warrior = Warrior("Warriors/Imp_1.red")

    core = MARS(5, 1, warriors)
    for i in range(5):
        core._MARS[i] = Instruction("BLA.BLA 12")
    core._MARS[3] = Instruction(None, "DAT", None, 0, 0)
    assert core._find_a_place(warrior) == 3

    for i in range(5):
        core._MARS[i] = Instruction("BLA.BLA 12")
    core._MARS[1] = Instruction(None, "DAT", None, 0, 0)
    assert core._find_a_place(warrior) == 1

    warrior = Warrior("Warriors/Dwarf.red")
    core = MARS(100, 1, warriors)
    for i in range(100):
        core._MARS[i] = Instruction("BLA.BLA 12")
    for i in range(24, 28):
        core._MARS[i] = Instruction(None, "DAT", None, 0, 0)
    assert core._find_a_place(warrior) == 24
