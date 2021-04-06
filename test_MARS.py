import pytest
from MARS import MARS
from warrior import Warrior
from Redcode import Instruction
from Validating_tools import WarriorSizeError, NoWarriorsError


def test_validate_warriors():
    test_warriors = [
        Warrior("Warriors/Dwarf.red") for _ in range(100)
    ]
    with pytest.raises(WarriorSizeError):
        MARS(100, 100, test_warriors)

    test_warriors_2 = []
    with pytest.raises(NoWarriorsError):
        MARS(100, 100, test_warriors_2)


def test_find_a_place():
    warriors = [Warrior("Warriors/Imp.red")]
    warrior = Warrior("Warriors/Imp.red")

    core = MARS(5, 1, warriors)
    for i in range(5):
        core._MARS[i] = Instruction("DAT 12")
    core._MARS[3] = Instruction(None, "DAT", None, 0, 0)
    assert core._find_a_place(warrior) == 3

    for i in range(5):
        core._MARS[i] = Instruction("DAT 12")
    core._MARS[1] = Instruction(None, "DAT", None, 0, 0)
    assert core._find_a_place(warrior) == 1

    warrior = Warrior("Warriors/Dwarf.red")
    core = MARS(100, 1, warriors)
    for i in range(100):
        core._MARS[i] = Instruction("SPL 12, $5")
    for i in range(24, 28):
        core._MARS[i] = Instruction(None, "DAT", None, 0, 0)
    assert core._find_a_place(warrior) == 24
