from warrior import Warrior
from MARS import MARS


def test_game():
    warriors = [
        Warrior("Warriors/Dwarf.red"),
        Warrior("Warriors/Imp_1.red")
    ]
    core = MARS(50, 100, warriors)
    core.prepare_for_simulation()
    core.simulate_core()
    core.results()
    assert 1 == 1
