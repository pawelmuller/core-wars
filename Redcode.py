class Instruction:
    def __init__(self, line, instruction=None, modifier=None,
                 A=None, B=None, type_A="$", type_B="$", warrior=None):
        """
        Creates Instruction object.
        """
        self._instruction = instruction
        self._modifier = modifier
        self._A = A
        self._B = B
        self._type_A = type_A
        self._type_B = type_B
        self._warrior = warrior

        if line:
            self.convert(line)

        # Instructions dictionary:
        self.Redcode_Instructions = {
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

        # Modifiers dictionary:
        '''self.Modifiers = {
            "A": self.mod_A,
            "B": self.mod_B,
            "AB": self.mod_AB,
            "BA": self.mod_BA,
            "F": self.mod_F,
            "X": self.mod_X,
            "I": self.mod_I
        }'''

    def __repr__(self):
        """
        Represents Instruction object.
        """
        output = f"ID: {id(self)}, "
        output += self._instruction
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
        self._instruction = in_str[0:3]

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
        if ',' in in_str:
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
        else:
            variable = in_str.strip()
            if variable.isdigit():
                if self._instruction == "DAT":
                    self._B = int(variable)
                else:
                    self._A = int(variable)
            elif variable[0] == "-":
                if self._instruction == "DAT":
                    self._B = int(variable)
                else:
                    self._A = int(variable)
            else:
                if self._instruction == "DAT":
                    self._type_B = variable[0]
                    self._B = int(variable[1:])
                else:
                    self._type_A = variable[0]
                    self._A = int(variable[1:])
        return True

    def copy(self):
        """
        Returns new object with the same parameters as self.
        """
        return Instruction(None, self._instruction, self._modifier,
                           self._A, self._B, self._type_A, self._type_B,
                           self._warrior)

    def compare(self, other):
        """
        Compares two Instruction objects.
        Returns True if equal.
        """
        if self._instruction != other._instruction:
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

    def run(self):
        """
        Runs the instruction.
        """
        self.Redcode_Instructions[self._instruction]()
        return True

    # Handling Redcode instructions:
    def DAT(self):
        '''DAT -- data (kills the process)'''
        # Modifiers[modifier](A, B) - modifiers don't affect DAT
        pass

    def MOV(self):
        '''
        MOV -- move (copies data from one address to another)
        '''
        # Modifiers[modifier](A, B)
        index = self._index
        core = self._core
        core_size = len(core)

        A_abs = (self._A + index) % core_size
        B_abs = (self._B + index) % core_size

        core[B_abs] = core[A_abs].copy()
        new_index = (index + 1) % core_size
        core[B_abs].attach_core(core)
        core[B_abs].update_index()

        warrior = self._warrior
        warrior.add_process(new_index)

    def ADD(self):
        '''ADD -- add (adds one number to another)'''
        # Modifiers[modifier](A, B)
        pass

    def SUB(self):
        '''SUB -- subtract (subtracts one number from another)'''
        # Modifiers[modifier](A, B)
        pass

    def MUL(self):
        '''MUL -- multiply (multiplies one number with another)'''
        # Modifiers[modifier](A, B)
        pass

    def DIV(self):
        '''DIV -- divide (divides one number with another)'''
        # Modifiers[modifier](A, B)
        pass

    def MOD(self):
        '''MOD -- modulus (divides one number with another
        and gives the remainder)'''
        # Modifiers[modifier](A, B)
        pass

    def JMP(self):
        '''JMP -- jump (continues execution from another address)'''
        # Modifiers[modifier](A, B)
        pass

    def JMZ(self):
        '''JMZ -- jump if zero (tests a number and jumps
        to an address if it's 0)'''
        # Modifiers[modifier](A, B)
        pass

    def JMN(self):
        '''JMN -- jump if not zero (tests a number and
        jumps if it isn't 0)'''
        # Modifiers[modifier](A, B)
        pass

    def DJN(self):
        '''DJN -- decrement and jump if not zero (decrements a number
        by one, and jumps unless the result is 0)'''
        # Modifiers[modifier](A, B)
        pass

    def SPL(self):
        '''SPL -- split (starts a second process at another address)'''
        # Modifiers[modifier](A, B)
        pass

    def CMP(self):
        '''CMP -- compare (same as SEQ)'''
        # Modifiers[modifier](A, B)
        pass

    def SEQ(self):
        '''SEQ -- skip if equal (compares two instructions, and skips the next
        instruction if they are equal)'''
        # Modifiers[modifier](A, B)
        pass

    def SNE(self):
        '''SNE -- skip if not equal (compares two instructions, and skips the next
        instruction if they aren't equal)'''
        # Modifiers[modifier](A, B)
        pass

    def SLT(self):
        '''SLT -- skip if lower than (compares two values, and skips the
        next instruction if the first is lower than the second)'''
        # Modifiers[modifier](A, B)
        pass

    def NOP(self):
        '''NOP -- no operation (does nothing)'''
        # Modifiers[modifier](A, B)
        pass

    # Modifiers:

    def mod_A(self):
        '''A -- moves the A of the source into the A of the destination'''
        pass

    def mod_B(self):
        '''B -- moves the B of the source into the B of the destination'''
        pass

    def mod_AB(self):
        '''AB -- moves the A of the source into the B of the destination'''
        pass

    def mod_BA(self):
        '''BA -- moves the B of the source into the A of the destination'''
        pass

    def mod_F(self):
        '''F -- moves AB of the source into the AB in the destination'''
        pass

    def mod_X(self):
        '''X -- moves AB of the source into the BA in the destination'''
        pass

    def mod_I(self):
        '''I -- moves the whole source instruction into the destination'''
        pass
