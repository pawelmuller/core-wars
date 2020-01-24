from Redcode import Instruction
from random import randint
from Validating_tools import NoWarriorsError, WarriorSizeError
from os import system
from termcolor import colored


class MARS():
    def __init__(self, size, cycles_limit, warriors):
        self._MARS = []
        self._clear(size)
        self._cycles_limit = cycles_limit
        self._warriors = warriors
        self._validate_warriors()
        self._playing_warriors = warriors

    def __repr__(self):
        return f"ID: {id(self)}"

    def __len__(self):
        return len(self._MARS)

    def __getitem__(self, key):
        return self._MARS[key]

    def __setitem__(self, key, value):
        self._MARS[key] = value

    def get_index(self, item):
        """
        Returns instruction index in MARS
        """
        core = self._MARS
        return core.index(item)

    def _clear(self, size):
        """
        Fills MARS with default instructions (DAT 0, 0).
        """
        for cell in range(size):
            self._MARS.append(Instruction(None, "DAT", None, 0, 0))

    def _validate_warriors(self):
        """
        Method makes sure if warriors were given properly.
        Raises Exception if not.
        """
        if len(self._warriors) == 0:
            raise NoWarriorsError("No warriors given.")
            return
        warriors_length = 0
        for warrior in self._warriors:
            warriors_length += len(warrior)
        if warriors_length > len(self):
            error_msg = "Summed length of warriors is "
            error_msg += "greater than size of the core."
            raise WarriorSizeError(error_msg)
            return
        if warriors_length == 0:
            raise WarriorSizeError("Warriors are empty.")
            return

    def _find_a_place(self, warrior):
        """
        Finds a place for the warrior in the core.
        Returns an absolute index, where to place 1st instruction.
        """
        warrior_size = len(warrior)
        core_size = len(self)
        default = Instruction(None, "DAT", None, 0, 0)
        while True:
            count = 0
            random_no = randint(0, core_size-1)
            for i in range(warrior_size):
                index = (random_no + i) % core_size
                if self._MARS[index].compare(default):
                    count += 1
                else:
                    break
                if count == warrior_size:
                    return random_no

    def _place_warriors(self):
        """
        Method places warriors in random places in the core.
        """
        core_size = len(self)
        for warrior in self._warriors:
            warrior.attach_core(self)
            # Searching for a place in core:
            start_index = self._find_a_place(warrior)
            # Placing warrior in core:
            iterators = range(len(warrior))
            instructions = warrior.get_instructions()
            for i, instruction in zip(iterators, instructions):
                index = (start_index + i) % core_size
                self._MARS[index] = instruction
                instruction.attach_core(self)
                instruction.attach_warrior(warrior)
                instruction.update_index()
            warrior.set_start(start_index)

    def prepare_for_simulation(self):
        """
        Prepares MARS for simulation.
        """
        colors = ['red', 'yellow', 'green', 'blue', 'orange',
                  'cyan', 'magenta', 'white']
        for warrior, color in zip(self._warriors, colors):
            warrior.attach_core(self)
            warrior.set_color(color)
        self._place_warriors()

    def _update_instruction_indexes(self):
        """
        Updates index for each instruction in core.

        Returns True if successful.
        """
        core = self._MARS
        for instruction in core:
            instruction.attach_core(self)
            instruction.update_index()
        return True

    def _perform_cycle(self):
        """
        Performs one cycle of game:
        each warrior executes its current process and runs instruction.

        If cycle was successful: return True
        If warrior lost all of its processes: returns False
        """
        for warrior in self._playing_warriors:
            warrior.attach_core(self)
            if warrior.make_a_turn():
                continue
            elif len(self._playing_warriors) > 2:
                self._playing_warriors.remove(warrior)
            else:
                return False

        return True

    def simulate_core(self):
        """
        Simulates MARS.
        """
        cycles_count = 0
        for cycle in range(self._cycles_limit):
            self._update_instruction_indexes()
            cycles_count += 1
            if self._perform_cycle():
                self._print_simulation(cycles_count)
                continue
            else:
                break
        self._cycles_count = cycles_count

    def results(self):
        """
        Prepare game results.
        """
        winners = []
        losers = []
        for warrior in self._warriors:
            if warrior.is_alive():
                winners.append(warrior)
            else:
                losers.append(warrior)
        self._print_results(winners, losers)

    def _print_simulation(self, cycle):
        """
        Prints character-based core representation.
        """
        system("clear")
        default = Instruction(None, "DAT", None, 0, 0)
        print(''.join([" " if instruction.compare(default)
                       else colored("X", instruction.get_color())
                       if instruction.get_warrior() is None
                       else colored("█", instruction.get_color())
                       for instruction in self._MARS]))
        print(f"\nCycle: {cycle} / {self._cycles_limit}\nWarriors:")
        warriors_txt = ""
        for warrior in self._warriors:
            warriors_txt += colored(warrior.get_name(), warrior.get_color())
            warriors_txt += "\t"
        print(warriors_txt)

    def _print_results(self, winners, losers):
        """
        Prints game results.
        """
        output = "="*20 + "\n"
        output += "Round results:\n"
        if self._cycles_count == self._cycles_limit:
            output += "There was a draw.\nNone of warriors won.\n"
        else:
            output += "\nWinners:" + "\n"
            for winner in winners:
                output += colored(winner.get_name(), winner.get_color()) + "\n"
            output += "\nLosers:" + "\n"
            for loser in losers:
                output += colored(loser.get_name(), loser.get_color()) + "\n"
        print(output)
