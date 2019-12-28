from Redcode import Instruction


class Warrior:
    def __init__(self, path_to_file):
        self._warrior_instructions = []
        self._path_to_file = path_to_file
        self.import_from_file(path_to_file)

    def validate_line(self, line):
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

    def import_from_file(self, path_to_file):
        """
        Method imports warrior from file and appends its instructions
        (as objects) into self._warrior_instructions.

        Attributes:
        :param path_to_file: Path to Redcode file where warrior is located.
        :type path_to_file: str
        """
        with open(path_to_file, "r") as file:
            for line in file:
                if self.validate_line(line) is True:
                    self._warrior_instructions.append(Instruction(line))
