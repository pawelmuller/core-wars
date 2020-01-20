from Validating_tools import WrongOpcode, WrongModifier
from Validating_tools import WrongAddressingMode


class Instruction:
    def __init__(self, line, opcode=None, modifier=None,
                 A=None, B=None, type_A="$", type_B="$", warrior=None):
        """
        Creates Instruction object.
        """
        self._opcode = opcode
        self._modifier = modifier
        self._A = A
        self._B = B
        self._type_A = type_A
        self._type_B = type_B
        self._warrior = warrior

        if line:
            self.convert(line)

        if not self._modifier:
            self._set_default_modifier()

        # Opcodes dictionary:
        self.Redcode_Opcodes = {
            "DAT": self.DAT,
            "MOV": self.MOV,
            "ADD": self.ADD,
            "SUB": self.SUB,
            "MUL": self.MUL,
            "DIV": self.DIV,
            "MOD": self.MOD,
            "JMP": self.JMP,
            "JMZ": self.JMZ,
            "JMN": self.JMN,
            "DJN": self.DJN,
            "SPL": self.SPL,
            "CMP": self.CMP,
            "SEQ": self.SEQ,
            "SNE": self.SNE,
            "SLT": self.SLT,
            "NOP": self.NOP
        }

        # Modifiers list:
        self.Redcode_Modifiers = [
            "A",
            "B",
            "AB",
            "BA",
            "F",
            "X",
            "I",
        ]

        # Addressing modes dictionary:
        self.Redcode_Addressing_Modes = {
            "#": self.immediate,
            "$":  self.direct,
            "*":  self.A_indirect,
            "@":  self.B_indirect,
            "{":  self.A_predecrement,
            "<":  self.B_predecrement,
            "}":  self.A_postincrement,
            ">":  self.B_postincrement
        }

        self._validate_instruction()

    def __repr__(self):
        """
        Represents Instruction object.
        """
        output = f"ID: {id(self)}, "
        output += self._opcode
        if self._modifier:
            output += "." + self._modifier
        output += " "
        if self._type_A:
            output += self._type_A + str(self._A)
        else:
            output += str(self._A)
        if self._B is not None:
            output += " "
            if self._type_B:
                output += self._type_B + str(self._B)
            else:
                output += str(self._B)
        return output

    def __set__(self, instance, value):
        core = self._core
        core[self._index] = value.copy()

    def _validate_instruction(self):
        if self._opcode not in self.Redcode_Opcodes:
            error_msg = f"{self._opcode} instruction doesn't exist."
            raise WrongOpcode(error_msg)
        if self._modifier is not None:
            if self._modifier not in self.Redcode_Modifiers:
                error_msg = f"{self._modifier} modifier doesn't exist."
                raise WrongModifier(error_msg)
        if self._A is not None:
            try:
                int(self._A)
            except ValueError:
                error_msg = "A variable should be an integer."
                raise ValueError(error_msg)
        if self._B is not None:
            try:
                int(self._B)
            except ValueError:
                error_msg = "B variable should be an integer."
                raise ValueError(error_msg)
        if self._type_A not in self.Redcode_Addressing_Modes:
            error_msg = f"{self._type_A} addressing mode doesn't exist."
            raise WrongAddressingMode(error_msg)
        if self._type_B not in self.Redcode_Addressing_Modes:
            error_msg = f"{self._type_B} addressing mode doesn't exist."
            raise WrongAddressingMode(error_msg)
        if self._type_A == "@":
            error_msg = f"A-type mustn't be '@'. It's reserved for B-one only."
            raise WrongAddressingMode(error_msg)
        if self._type_B == "*":
            error_msg = f"B-type mustn't be '*'. It's reserved for A-one only."
            raise WrongAddressingMode(error_msg)
        return

    def _set_default_modifier(self):
        """
        If instruction modifier doesn't exist, the method adds default one.
        """
        opcode = self._opcode
        if opcode in ["DAT", "NOP"]:
            self._modifier = "F"
        elif opcode in ["MOV", "SEQ", "SNE", "CMP"]:
            if self._type_A == "#":
                self._modifier = "AB"
            elif self._type_B == "#":
                self._modifier = "B"
            else:
                self._modifier = "I"
        elif opcode in ["ADD", "SUB", "MUL", "DIV", "MOD"]:
            if self._type_A == "#":
                self._modifier = "AB"
            elif self._type_B == "#":
                self._modifier = "B"
            else:
                self._modifier = "F"
        elif opcode in ["SLT", "LDP", "STP"]:
            if self._type_A == "#":
                self._modifier = "AB"
            else:
                self._modifier = "B"
        elif opcode in ["JMP", "JMZ", "JMN", "DJN", "SPL"]:
            self._modifier = "B"
        return True

    def convert(self, line):
        """
        Converts Redcode file line into Instruction object.
        """
        line = line.upper()
        line = line.strip()

        # in_str - instruction string

        # Looking for instruction:
        in_str = line.split(';', maxsplit=1)
        in_str = in_str[0]
        self._opcode = in_str[0:3]

        # Looking for modifier:
        if '.' in in_str:
            in_str = in_str.split('.')
            in_str = in_str[1]
            in_str = in_str.split(' ', maxsplit=1)
            self._modifier = in_str[0]
            in_str = in_str[1]
        else:
            in_str = in_str.split(' ', maxsplit=1)
            in_str = in_str[1]

        # Looking for variables:
        if ',' in in_str:  # If true: two variables found
            in_str = in_str.split(',')

            # Addressing modes:
            A = in_str[0].strip()
            if A.isdigit():
                self._A = int(A)
            elif A[0] == "-":
                self._A = int(A)
            else:
                self._type_A = A[0]
                self._A = int(A[1:])

            B = in_str[1].strip()
            if B.isdigit():
                self._B = int(B)
            elif B[0] == "-":
                self._B = int(B)
            else:
                self._type_B = B[0]
                self._B = int(B[1:])
        else:  # One variable found
            variable = in_str.strip()
            if self._opcode in ["JMP", "SPL", "NOP"]:
                try:
                    int(variable)
                except ValueError:
                    self._type_A = variable[0]
                    self._A = int(variable[1:])
                else:
                    self._A = int(variable)
                self._B = 0
            elif self._opcode == "DAT":
                try:
                    int(variable)
                except ValueError:
                    self._type_B = variable[0]
                    self._B = int(variable[1:])
                else:
                    self._B = int(variable)
                self._A = 0
        return True

    def copy(self):
        """
        Returns new object with the same parameters as self.
        """
        return Instruction(None, self._opcode, self._modifier,
                           self._A, self._B, self._type_A, self._type_B,
                           self._warrior)

    def compare(self, other):
        """
        Compares two Instruction objects.
        Returns True if equal.
        """
        if self._opcode != other._opcode:
            return False
        elif self._modifier != other._modifier:
            return False
        elif self._type_A != other._type_A:
            return False
        elif self._A != other._A:
            return False
        elif self._type_B != other._type_B:
            return False
        elif self._B != other._B:
            return False
        else:
            return True

    def update_index(self):
        """
        Updates instruction index (absolute location in core).
        """
        core = self._core
        self._index = core.get_index(self)
        return True

    def attach_core(self, core):
        """
        Updates link to MARS.
        """
        self._core = core
        return True

    def attach_warrior(self, warrior):
        """
        Updates link to its parent warrior.
        """
        self._warrior = warrior
        return True

    def get_opcode(self):
        """
        Returns its opcode.
        """
        return self._opcode

    def run(self):
        """
        Runs the instruction.
        """
        A = self._A
        B = self._B
        source_index = self.Redcode_Addressing_Modes[self._type_A](A)
        destination_index = self.Redcode_Addressing_Modes[self._type_B](B)
        self.Redcode_Opcodes[self._opcode](source_index, destination_index)
        return True

    # Addressing modes:

    def immediate(self, variable):
        """#"""
        return self._index

    def direct(self, variable):
        """$"""
        core = self._core
        core_size = len(core)
        index = self._index + variable + core_size
        index %= core_size
        return index

    def A_indirect(self, variable):
        """*"""
        core = self._core
        core_size = len(core)
        pointer = self._index + variable + core_size
        pointer %= core_size
        index = core[pointer]._A + core[pointer]._index + core_size
        index %= core_size
        return index

    def B_indirect(self, variable):
        """@"""
        core = self._core
        core_size = len(core)
        pointer = self._index + variable + core_size
        pointer %= core_size
        index = core[pointer]._B + core[pointer]._index + core_size
        index %= core_size
        return index

    def A_predecrement(self, variable):
        """{"""
        core = self._core
        core_size = len(core)
        pointer = self._index + variable + core_size
        pointer %= core_size
        core[pointer]._A -= 1
        index = core[pointer]._A + core[pointer]._index + core_size
        index %= core_size
        return index

    def B_predecrement(self, variable):
        """}"""
        core = self._core
        core_size = len(core)
        pointer = self._index + variable + core_size
        pointer %= core_size
        core[pointer]._B -= 1
        index = core[pointer]._B + core[pointer]._index + core_size
        index %= core_size
        return index

    def A_postincrement(self, variable):
        """<"""
        core = self._core
        core_size = len(core)
        pointer = self._index + variable + core_size
        pointer %= core_size
        index = core[pointer]._A + core[pointer]._index + core_size
        index %= core_size
        core[pointer]._A += 1
        return index

    def B_postincrement(self, variable):
        """>"""
        core = self._core
        core_size = len(core)
        pointer = self._index + variable + core_size
        pointer %= core_size
        index = core[pointer]._B + core[pointer]._index + core_size
        index %= core_size
        core[pointer]._B += 1
        return index

    # Handling Redcode opcodes:
    def DAT(self, source_index, destination_index):
        '''DAT -- data (kills the process)'''
        return None

    def MOV(self, source_index, destination_index):
        '''MOV -- move (copies data from one address to another)'''
        index = self._index
        core = self._core
        core_size = len(core)

        if self._modifier == "A":
            core[destination_index]._A = core[source_index]._A
        elif self._modifier == "B":
            core[destination_index]._B = core[source_index]._B
        elif self._modifier == "AB":
            core[destination_index]._B = core[source_index]._A
        elif self._modifier == "BA":
            core[destination_index]._A = core[source_index]._B
        elif self._modifier == "F":
            core[destination_index]._A = core[source_index]._A
            core[destination_index]._B = core[source_index]._B
        elif self._modifier == "X":
            core[destination_index]._A = core[source_index]._B
            core[destination_index]._B = core[source_index]._A
        elif self._modifier == "I":
            core[destination_index] = core[source_index].copy()
            core[destination_index].attach_core(core)
            core[destination_index].update_index()

        new_index = (index + 1) % core_size
        return new_index

    def ADD(self, source_index, destination_index):
        '''ADD -- add (adds one number to another)'''
        index = self._index
        core = self._core
        core_size = len(core)

        if self._modifier == "A":
            core[destination_index]._A += core[source_index]._A
        elif self._modifier == "B":
            core[destination_index]._B += core[source_index]._B
        elif self._modifier == "AB":
            core[destination_index]._B += core[source_index]._A
        elif self._modifier == "BA":
            core[destination_index]._A += core[source_index]._B
        elif self._modifier == "F" or self._modifier == "I":
            core[destination_index]._A += core[source_index]._A
            core[destination_index]._B += core[source_index]._B
        elif self._modifier == "X":
            core[destination_index]._A += core[source_index]._B
            core[destination_index]._B += core[source_index]._A

        core[destination_index]._A %= core_size
        core[destination_index]._B %= core_size
        new_index = (index + 1) % core_size
        return new_index

    def SUB(self, source_index, destination_index):
        '''SUB -- subtract (subtracts one number from another)'''
        index = self._index
        core = self._core
        core_size = len(core)

        if self._modifier == "A":
            core[destination_index]._A -= core[source_index]._A
        elif self._modifier == "B":
            core[destination_index]._B -= core[source_index]._B
        elif self._modifier == "AB":
            core[destination_index]._B -= core[source_index]._A
        elif self._modifier == "BA":
            core[destination_index]._A -= core[source_index]._B
        elif self._modifier == "F" or self._modifier == "I":
            core[destination_index]._A -= core[source_index]._A
            core[destination_index]._B -= core[source_index]._B
        elif self._modifier == "X":
            core[destination_index]._A -= core[source_index]._B
            core[destination_index]._B -= core[source_index]._A

        core[destination_index]._A %= core_size
        core[destination_index]._B %= core_size
        new_index = (index + 1) % core_size
        return new_index

    def MUL(self, source_index, destination_index):
        '''MUL -- multiply (multiplies one number with another)'''
        index = self._index
        core = self._core
        core_size = len(core)

        if self._modifier == "A":
            core[destination_index]._A *= core[source_index]._A
        elif self._modifier == "B":
            core[destination_index]._B *= core[source_index]._B
        elif self._modifier == "AB":
            core[destination_index]._B *= core[source_index]._A
        elif self._modifier == "BA":
            core[destination_index]._A *= core[source_index]._B
        elif self._modifier == "F" or self._modifier == "I":
            core[destination_index]._A *= core[source_index]._A
            core[destination_index]._B *= core[source_index]._B
        elif self._modifier == "X":
            core[destination_index]._A *= core[source_index]._B
            core[destination_index]._B *= core[source_index]._A

        core[destination_index]._A %= core_size
        core[destination_index]._B %= core_size
        new_index = (index + 1) % core_size
        return new_index

    def DIV(self, source_index, destination_index):
        '''DIV -- divide (divides one number with another)'''
        index = self._index
        core = self._core
        core_size = len(core)

        if self._modifier == "A":
            if core[source_index]._A == 0:
                return None
            core[destination_index]._A //= core[source_index]._A
        elif self._modifier == "B":
            if core[source_index]._B == 0:
                return None
                core[destination_index]._B //= core[source_index]._B
        elif self._modifier == "AB":
            if core[source_index]._A == 0:
                return None
            core[destination_index]._B //= core[source_index]._A
        elif self._modifier == "BA":
            if core[source_index]._B == 0:
                return None
            core[destination_index]._A //= core[source_index]._B
        elif self._modifier == "F" or self._modifier == "I":
            if core[source_index]._A == 0 or core[source_index]._B == 0:
                return None
            core[destination_index]._A //= core[source_index]._A
            core[destination_index]._B //= core[source_index]._B
        elif self._modifier == "X":
            if core[source_index]._A == 0 or core[source_index]._B == 0:
                return None
            core[destination_index]._A //= core[source_index]._B
            core[destination_index]._B //= core[source_index]._A

        core[destination_index]._A %= core_size
        core[destination_index]._B %= core_size
        new_index = (index + 1) % core_size
        return new_index

    def MOD(self, source_index, destination_index):
        '''MOD -- modulus (divides one number with another
        and gives the remainder)'''
        index = self._index
        core = self._core
        core_size = len(core)

        if self._modifier == "A":
            if core[source_index]._A == 0:
                return None
            core[destination_index]._A %= core[source_index]._A
        elif self._modifier == "B":
            if core[source_index]._B == 0:
                return None
            core[destination_index]._B %= core[source_index]._B
        elif self._modifier == "AB":
            if core[source_index]._A == 0:
                return None
            core[destination_index]._B %= core[source_index]._A
        elif self._modifier == "BA":
            if core[source_index]._B == 0:
                return None
            core[destination_index]._A %= core[source_index]._B
        elif self._modifier == "F" or self._modifier == "I":
            if core[source_index]._A == 0 or core[source_index]._B == 0:
                return None
            core[destination_index]._A %= core[source_index]._A
            core[destination_index]._B %= core[source_index]._B
        elif self._modifier == "X":
            if core[source_index]._A == 0 or core[source_index]._B == 0:
                return None
            core[destination_index]._A %= core[source_index]._B
            core[destination_index]._B %= core[source_index]._A

        core[destination_index]._A %= core_size
        core[destination_index]._B %= core_size
        new_index = (index + 1) % core_size
        return new_index

    def JMP(self, source_index, destination_index):
        '''JMP -- jump (continues execution from another address)'''
        return source_index

    def JMZ(self, source_index, destination_index):
        '''JMZ -- jump if zero (tests a number and jumps
        to an address if it's 0)'''
        index = self._index
        core = self._core
        core_size = len(core)
        index_if_not_zero = (index + 1) % core_size

        if self._modifier in ["A", "BA"]:
            if core[destination_index]._A == 0:
                return destination_index
            else:
                return index_if_not_zero
        elif self._modifier in ["B", "AB"]:
            if core[destination_index]._B == 0:
                return destination_index
            else:
                return index_if_not_zero
        elif self._modifier in ["F", "X", "I"]:
            if core[destination_index]._A == core[destination_index]._B == 0:
                return destination_index
            else:
                return index_if_not_zero

    def JMN(self, source_index, destination_index):
        '''JMN -- jump if not zero (tests a number and
        jumps if it isn't 0)'''
        index = self._index
        core = self._core
        core_size = len(core)
        index_if_zero = (index + 1) % core_size

        if self._modifier in ["A", "BA"]:
            if core[destination_index]._A != 0:
                return destination_index
            else:
                return index_if_zero
        elif self._modifier in ["B", "AB"]:
            if core[destination_index]._B != 0:
                return destination_index
            else:
                return index_if_zero
        elif self._modifier in ["F", "X", "I"]:
            if core[destination_index]._A != 0:
                if core[destination_index]._B != 0:
                    return destination_index
                else:
                    return index_if_zero
            else:
                return index_if_zero

    def DJN(self, source_index, destination_index):
        '''DJN -- decrement and jump if not zero (decrements a number
        by one, and jumps unless the result is 0)'''
        index = self._index
        core = self._core
        core_size = len(core)
        index_if_zero = (index + 1) % core_size

        if self._modifier in ["A", "BA"]:
            core[destination_index]._A += (core_size - 1)
            core[destination_index]._A %= core_size
            if core[destination_index]._A != 0:
                return destination_index
            else:
                return index_if_zero
        elif self._modifier in ["B", "AB"]:
            core[destination_index]._B += (core_size - 1)
            core[destination_index]._B %= core_size
            if core[destination_index]._B != 0:
                return destination_index
            else:
                return index_if_zero
        elif self._modifier in ["F", "X", "I"]:
            core[destination_index]._A += (core_size - 1)
            core[destination_index]._A %= core_size
            core[destination_index]._B += (core_size - 1)
            core[destination_index]._B %= core_size
            if core[destination_index]._A != 0:
                if core[destination_index]._B != 0:
                    return destination_index
                else:
                    return index_if_zero
            else:
                return index_if_zero

    def SPL(self, source_index, destination_index):
        '''SPL -- split (starts a second process at another address)'''
        # Modifiers[modifier](A, B)
        pass

    def CMP(self, source_index, destination_index):
        '''CMP -- compare (same as SEQ)'''
        return self.SEQ(source_index, destination_index)

    def SEQ(self, source_index, destination_index):
        '''SEQ -- skip if equal (compares two instructions, and skips the next
        instruction if they are equal)'''
        # Modifiers[modifier](A, B)
        pass

    def SNE(self, source_index, destination_index):
        '''SNE -- skip if not equal (compares two instructions, and skips the next
        instruction if they aren't equal)'''
        # Modifiers[modifier](A, B)
        pass

    def SLT(self, source_index, destination_index):
        '''SLT -- skip if lower than (compares two values, and skips the
        next instruction if the first is lower than the second)'''
        # Modifiers[modifier](A, B)
        pass

    def NOP(self, source_index, destination_index):
        '''NOP -- no operation (does nothing)'''
        # Modifiers[modifier](A, B)
        pass
