import pytest
from MARS import MARS
from warrior import Warrior


def test_validate_warriors():
    test_warriors = [
        Warrior("Warriors/Imp_1.red"),
        Warrior("Warriors/Dwarf.red")
    ]
    test_core = MARS(100, 100, test_warriors)
    with pytest.raises(Exception):
        test_core.test_validate_warriors()
