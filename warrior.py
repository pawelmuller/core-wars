from Redcode import Instruction


class Warrior:
    def __init__(self, path_to_file):
        self._path_to_file = path_to_file
        self._instructions = self._import_from_file(path_to_file)
        self._length = len(self._instructions)
        self._process_queue = []  # List of absolute indexes of instructions

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
                    instructions.append(Instruction(line))
        return instructions

    def make_a_turn(self):
        pass

    def change_process(self):
        pass

    def add_process(self, index):
        """
        Adds new process to warrior.
        Puts it right after current one.
        """
        current_process_id = self._process_queue.index(self._current_process)
        self._process_queue.insert(current_process_id, index)  # TESTOWAC
        pass

    def end_process(self):
        pass

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
