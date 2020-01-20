class InstructionNotValid(Exception):
    pass


class WrongOpcode(InstructionNotValid):
    """
    Raised when opcode doesn't exist.
    """
    pass


class WrongModifier(InstructionNotValid):
    """
    Raised when modifier doesn't exist.
    """
    pass


class WrongAddressingMode(InstructionNotValid):
    """
    Raised when addressing mode doesn't exist.
    """
    pass


class WarriorNotValid(Exception):
    pass


class NoWarriors(WarriorNotValid):
    """
    Raised when there are no warriors given.
    """
    pass


class WarriorSize(WarriorNotValid):
    """
    Raised when there are no warriors given.
    """
    pass
