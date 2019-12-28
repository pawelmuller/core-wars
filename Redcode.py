def DAT(A, B, type_A, type_B):
    '''DAT -- data (kills the process)'''
    pass


def MOV(A, B, type_A, type_B):
    '''MOV -- move (copies data from one address to another)'''
    pass


def ADD(A, B, type_A, type_B):
    '''ADD -- add (adds one number to another)'''
    pass


def SUB(A, B, type_A, type_B):
    '''SUB -- subtract (subtracts one number from another)'''
    pass


def MUL(A, B, type_A, type_B):
    '''MUL -- multiply (multiplies one number with another)'''
    pass


def DIV(A, B, type_A, type_B):
    '''DIV -- divide (divides one number with another)'''
    pass


def MOD(A, B, type_A, type_B):
    '''MOD -- modulus (divides one number with another
    and gives the remainder)'''
    pass


def JMP(A, B, type_A, type_B):
    '''JMP -- jump (continues execution from another address)'''
    pass


def JMZ(A, B, type_A, type_B):
    '''JMZ -- jump if zero (tests a number and jumps
    to an address if it's 0)'''
    pass


def JMN(A, B, type_A, type_B):
    '''JMN -- jump if not zero (tests a number and
    jumps if it isn't 0)'''
    pass


def DJN(A, B, type_A, type_B):
    '''DJN -- decrement and jump if not zero (decrements a number
    by one, and jumps unless the result is 0)'''
    pass


def SPL(A, B, type_A, type_B):
    '''SPL -- split (starts a second process at another address)'''
    pass


def CMP(A, B, type_A, type_B):
    '''CMP -- compare (same as SEQ)'''
    pass


def SEQ(A, B, type_A, type_B):
    '''SEQ -- skip if equal (compares two instructions, and skips the next
    instruction if they are equal)'''
    pass


def SNE(A, B, type_A, type_B):
    '''SNE -- skip if not equal (compares two instructions, and skips the next
    instruction if they aren't equal)'''
    pass


def SLT(A, B, type_A, type_B):
    '''SLT -- skip if lower than (compares two values, and skips the
    next instruction if the first is lower than the second)'''
    pass


def LDP(A, B, type_A, type_B):
    '''LDP -- load from p-space (loads a number from private storage space)'''
    pass


def STP(A, B, type_A, type_B):
    '''STP -- save to p-space (saves a number to private storage space)'''
    pass


def NOP(A, B, type_A, type_B):
    '''NOP -- no operation (does nothing)'''
    pass


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
    "LDP": LDP,
    "STP": STP,
    "NOP": NOP
}


class Instruction:
    def __init__(self, line, instruction=None, modifier=None,
                 A=None, B=None, type_A="$", type_B="$"):
        """
        Creates Instruction object.
        """
        if line:
            self._line = line
            self.convert(line)
        else:
            self._instruction = instruction
            self._modifier = modifier
            self._A = A
            self._B = B
            self._type_A = type_A
            self._type_B = type_B

    def convert(self, line):
        """
        Converts Redcode file line into Instruction object.
        """
        str_instruction = line.split(';', maxsplit=1)
        str_instruction = str_instruction.lstrip()
        self._instruction = str_instruction[0:3].upper()
        self._modifier = str_instruction[0:3].upper()  # to-do: wycina modifier
        self._type_A = "#"  # to-do: wycina typ adresowania A
        self._A = 0  # to-do: wycina A
        self._type_B = "#"  # to-do: wycina typ adresowania B
        self._B = 0  # to-do: wycina B

    def run(self):
        """
        Runs itself.
        """
        Instructions[self._instruction](self._A, self._B,
                                        self._type_A, self._type_B)
