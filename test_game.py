from warrior import Warrior
from MARS import MARS


def test_game():
    warriors = [
        Warrior("Warriors/Dwarf.red"),
        Warrior("Warriors/Imp_1.red")
    ]
    core = MARS(8000, 10000, warriors)
    core.prepare_for_simulation()
    assert 1 == 1
