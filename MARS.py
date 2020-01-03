from Redcode import Instruction
from random import randint
from warrior import Warrior


class MARS():
    def __init__(self, size, cycle_limit, warriors):
        self._MARS = []
        self._size = size
        self._cycle_limit = cycle_limit
        self._warriors = warriors
        self._validate_warriors()

        # Filling MARS with default instructions:
        for cell in range(self._size):
            self._MARS.append(Instruction(None, "DAT", None, 0, 0))

        # Putting warriors in MARS:
        self._place_warriors(self._warriors)

    def _validate_warriors(self):
        """
        Method makes sure if warriors were given properly.
        Raises Exception if not.
        """
        if len(self._warriors) == 0:
            raise Exception("No warriors given.")
            return
        warriors_length = 0
        for warrior in self._warriors:
            warriors_length += warrior.get_length()
        if warriors_length > self._size:
            error_msg = "Summed length of warriors is "
            error_msg += "greater than size of the core."
            raise Exception(error_msg)
            return
        if warriors_length == 0:
            raise Exception("Warriors are empty.")
            return

    def _find_a_place(self, warrior):
        """
        Finds a place for the warrior in the core.
        Returns an absolute index, where to place 1st instruction.
        """
        default = Instruction(None, "DAT", None, 0, 0)
        while True:
            count = 0
            random_no = randint(0, self._size-1)
            for i in range(warrior.get_length()):
                if self._MARS[random_no + i].compare(default):
                    count += 1
                else:
                    break
                if count == warrior.get_length():
                    return random_no

    def _place_warriors(self, warriors):
        """
        Method places warriors in random places in the core.
        """
        for warrior in warriors:
            index = self._find_a_place(warrior)
            # Placing if there is a place for the warrior:
            iterators = range(warrior.get_length())
            instructions = warrior.get_instructions()
            for i, instruction in zip(iterators, instructions):
                self._MARS[index + i] = instruction
                instruction.set_index(index + i)
            warrior.set_absolute_start(index)

    def simulate(self, display):
        pass

    def results(self, display):
        # Results
        pass

    def print_simplified_GUI(self):
        # Wyswietlanie przebiegu gry tekstowo w terminalu
        pass


if __name__ == "__main__":
    warr = [Warrior("Warriors/Imp_1.red"), Warrior("Warriors/Dwarf.red")]
    test = MARS(8000, 10000, warr)
