from warrior import Warrior
from MARS import MARS


def test_game_1():
    warriors = [
        # Warrior("Warriors/Dwarf.red"),
        Warrior("Warriors/Imp.red"),
        # Warrior("Warriors/Blur_scanner.red"),
        # Warrior("Warriors/PolyDwarf.red"),
        Warrior("Warriors/Looping_paper.red"),
        # Warrior("Warriors/Transposition_stone.red"),
    ]
    core = MARS(50, 100, warriors)
    core.prepare_for_simulation()
    core.simulate_core()
    core.results()
    assert 1 == 1
