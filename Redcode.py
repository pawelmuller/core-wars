# Redcode instructions:
def DAT(modifier, A, B, type_A, type_B):
    '''DAT -- data (kills the process)'''
    # Modifiers[modifier](A, B) - modifiers don't affect DAT
    pass


def MOV(modifier, A, B, type_A, type_B):
    '''MOV -- move (copies data from one address to another)'''
    # Modifiers[modifier](A, B)
    pass


def ADD(modifier, A, B, type_A, type_B):
    '''ADD -- add (adds one number to another)'''
    Modifiers[modifier](A, B)
    pass


def SUB(modifier, A, B, type_A, type_B):
    '''SUB -- subtract (subtracts one number from another)'''
    Modifiers[modifier](A, B)
    pass


def MUL(modifier, A, B, type_A, type_B):
    '''MUL -- multiply (multiplies one number with another)'''
    Modifiers[modifier](A, B)
    pass


def DIV(modifier, A, B, type_A, type_B):
    '''DIV -- divide (divides one number with another)'''
    Modifiers[modifier](A, B)
    pass


def MOD(modifier, A, B, type_A, type_B):
    '''MOD -- modulus (divides one number with another
    and gives the remainder)'''
    Modifiers[modifier](A, B)
    pass


def JMP(modifier, A, B, type_A, type_B):
    '''JMP -- jump (continues execution from another address)'''
    Modifiers[modifier](A, B)
    pass


def JMZ(modifier, A, B, type_A, type_B):
    '''JMZ -- jump if zero (tests a number and jumps
    to an address if it's 0)'''
    Modifiers[modifier](A, B)
    pass


def JMN(modifier, A, B, type_A, type_B):
    '''JMN -- jump if not zero (tests a number and
    jumps if it isn't 0)'''
    Modifiers[modifier](A, B)
    pass


def DJN(modifier, A, B, type_A, type_B):
    '''DJN -- decrement and jump if not zero (decrements a number
    by one, and jumps unless the result is 0)'''
    Modifiers[modifier](A, B)
    pass


def SPL(modifier, A, B, type_A, type_B):
    '''SPL -- split (starts a second process at another address)'''
    Modifiers[modifier](A, B)
    pass


def CMP(modifier, A, B, type_A, type_B):
    '''CMP -- compare (same as SEQ)'''
    Modifiers[modifier](A, B)
    pass


def SEQ(modifier, A, B, type_A, type_B):
    '''SEQ -- skip if equal (compares two instructions, and skips the next
    instruction if they are equal)'''
    Modifiers[modifier](A, B)
    pass


def SNE(modifier, A, B, type_A, type_B):
    '''SNE -- skip if not equal (compares two instructions, and skips the next
    instruction if they aren't equal)'''
    Modifiers[modifier](A, B)
    pass


def SLT(modifier, A, B, type_A, type_B):
    '''SLT -- skip if lower than (compares two values, and skips the
    next instruction if the first is lower than the second)'''
    Modifiers[modifier](A, B)
    pass


'''
def LDP(modifier, A, B, type_A, type_B):
    ''''LDP -- load from p-space (loads a number from private storage space)''''
    Modifiers[modifier](A, B)
    pass


def STP(modifier, A, B, type_A, type_B):
    ''''STP -- save to p-space (saves a number to private storage space)''''
    Modifiers[modifier](A, B)
    pass
'''


def NOP(modifier, A, B, type_A, type_B):
    '''NOP -- no operation (does nothing)'''
    Modifiers[modifier](A, B)
    pass


# Modifiers:
def mod_A():
    '''A -- moves the A of the source into the A of the destination'''
    pass


def mod_B():
    '''B -- moves the B of the source into the B of the destination'''
    pass


def mod_AB():
    '''AB -- moves the A of the source into the B of the destination'''
    pass


def mod_BA():
    '''BA -- moves the B of the source into the A of the destination'''
    pass


def mod_F():
    '''F -- moves AB of the source into the AB in the destination'''
    pass


def mod_X():
    '''X -- moves AB of the source into the BA in the destination'''
    pass


def mod_I():
    '''I -- moves the whole source instruction into the destination'''
    pass


# Instructions dictionary:
Instructions = {
    "DAT": DAT,
    "MOV": MOV,
    "ADD": ADD,
    "SUB": SUB,
    "MUL": MUL,
    "DIV": DIV,
    "MOD": MOD,
    "JMP": JMP,
    "JMZ": JMZ,
    "JMN": JMN,
    "DJN": DJN,
    "SPL": SPL,
    "CMP": CMP,
    "SEQ": SEQ,
    "SNE": SNE,
    "SLT": SLT,
    '''
    "LDP": LDP,
    "STP": STP,
    '''
    "NOP": NOP
}

# Modifiers dictionary:
Modifiers = {
    "A": mod_A,
    "B": mod_B,
    "AB": mod_AB,
    "BA": mod_BA,
    "F": mod_F,
    "X": mod_X,
    "I": mod_I
}


class Instruction:
    def __init__(self, line, instruction=None, modifier=None,
                 A=None, B=None, type_A="$", type_B="$"):
        """
        Creates Instruction object.
        """
        self._instruction = instruction
        self._modifier = modifier
        self._A = A
        self._B = B
        self._type_A = type_A
        self._type_B = type_B

        if line:
            self._line = line
            self.convert(line)

    def __repr__(self):
        """Represents Instruction object."""
        output = self._instruction
        if self._modifier:
            output += "." + self._modifier
        output += " "
        if self._type_A:
            output += self._type_A + str(self._A)
        else:
            output += str(self._A)
        if self._B:
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
            else:
                self._type_A = A[0]
                self._A = int(A[1:])

            B = in_str[1].strip()
            if B.isdigit():
                self._B = int(B)
            else:
                self._type_B = B[0]
                self._B = int(B[1:])
        else:
            self._A = int(in_str.strip())

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

    def set_index(self, index):
        """Sets instruction index (absolute location in core)."""
        self._index = index

    def run(self):
        """
        Runs the instruction.
        """
        Instructions[self._instruction](self._modifier, self._A, self._B,
                                        self._type_A, self._type_B)
