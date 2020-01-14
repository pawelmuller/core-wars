from Redcode import Instruction


class Warrior:
    def __init__(self, path_to_file):
        self._path_to_file = path_to_file

        # Warrior name:
        if "/" in path_to_file:
            self.name = path_to_file.split("/")[-1]
        else:
            self.name = path_to_file
        self.name = self.name.split('.')[0]

        self._instructions = self._import_from_file(path_to_file)
        self._length = len(self._instructions)
        # List of indexes of different processes
        # (last on the list - first to run):
        self._process_queue = []
        self.alive = True

    def __repr__(self):
        return self.name

    # File handling:

    def _validate_line(self, line):
        """
        Method checks if line is suitable for converting to
        warrior instruction. If so returns True.
        Returns False if:
            line is a comment-only line
            line is blank

        Attributes:
        :param line: single line from file
        :type line: str
        """
        if line.lstrip().startswith(";"):
            return False
        if len(line.lstrip()) == 0:
            return False
        return True

    def _import_from_file(self, path_to_file):
        """
        Method imports warrior from file and returns
        a list of its instructions.

        Attributes:
        :param path_to_file: Path to Redcode file where warrior is located.
        :type path_to_file: str
        """
        instructions = []
        with open(path_to_file, "r") as file:
            for line in file:
                if self._validate_line(line) is True:
                    instructions.append(Instruction(line, warrior=self))
        return instructions

    # Game elements:

    def make_a_turn(self, core):
        """
        Performs a warrior turn and checks if warrior is still alive.
        Returns True if successful.

        Attributes:
        :param core: MARS
        :type core: list
        """
        current_process_index = self._process_queue.pop()
        core[current_process_index].run(self)
        if len(self._process_queue) <= 0:
            self.alive = False
        return True

    def add_new_process(self, index):
        """
        Adds new process to warrior.
        Puts it at 0 index of _process_queue list.
        """
        self._process_queue.insert(0, index)
        pass

    def end_current_process(self):
        """
        Ends current process of the warrior.
        Deletes it from the _process_queue list.
        """
        process = self._process_queue[-1]
        self._process_queue.remove(process)
        pass

    # Getters and setters:

    def get_instructions(self):
        return self._instructions

    def get_length(self):
        return self._length

    def set_absolute_start(self, absolute_value):
        """
        Creates first process.
        """
        self._current_process = absolute_value
        self._process_queue.append(absolute_value)


if __name__ == "__main__":
    test = Warrior("Warriors/imp_1.red")
    print(test._length)
