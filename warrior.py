from Redcode import Instruction


class Warrior:
    """
    Class that maintains all warrior-oriented aspects.

    Stores all important data, keeps track of process queue
    and performs its turn.
    """
    def __init__(self, path_to_file):
        """
        Initiates Warrior object.

        Attributes:
        :param path_to_file: Path to file where instructions are held.
        :type path_to_file: str
        """
        self._path_to_file = path_to_file
        self._name = self._extract_name()
        self._instructions = self._import_from_file()
        # List of indexes of different processes
        # (last on the list - first to run):
        self._process_queue = []

    # Self representation:

    def __repr__(self):
        return f"ID: {id(self)}, {self._name}"

    def __len__(self):
        return len(self._instructions)

    def _extract_name(self):
        if "/" in self._path_to_file:
            name = self._path_to_file.split("/")[-1]
        else:
            name = self._path_to_file
        name = name.split('.')[0]
        return name

    def is_alive(self):
        return True if len(self) > 0 else False

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

    def _import_from_file(self):
        """
        Method imports warrior from file and returns
        a list of its instructions.

        Attributes:
        :param path_to_file: Path to Redcode file where warrior is located.
        :type path_to_file: str
        """
        instructions = []
        with open(self._path_to_file, "r") as file:
            for line in file:
                if self._validate_line(line):
                    new_instruction = Instruction(line, warrior=self)
                    instructions.append(new_instruction)
        return instructions

    # Game elements:

    def make_a_turn(self):
        """
        Performs a warrior turn.
        Returns True if successful.
        """
        core = self._core
        core_size = len(core)
        current_process_index = self._process_queue.pop()
        current_process_index %= core_size
        instruction = core[current_process_index]
        instruction.run()
        return True

    def add_process(self, index):
        """
        Adds new process to warrior.
        """
        core_size = len(self._core)
        index %= core_size
        self._process_queue.append(index)
        return True

    def end_process(self, index=None):
        """
        Ends current or specific process of the warrior.
        Deletes it from the _process_queue list.
        """
        if index:
            core_size = len(self._core)
            index %= core_size
            process = self._process_queue[index]
        else:
            process = self._process_queue[0]
        self._process_queue.remove(process)
        return True

    # Getters and setters:

    def get_instructions(self):
        return self._instructions

    def set_start(self, index):
        """
        Creates first process.
        """
        core_size = len(self._core)
        index %= core_size
        self._process_queue.append(index)
        return True

    def attach_core(self, core):
        """
        Updates link to MARS.
        """
        self._core = core
        return True
