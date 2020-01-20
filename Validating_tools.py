class InstructionNotValidError(Exception):
    pass


class WrongOpcodeError(InstructionNotValidError):
    """
    Raised when opcode doesn't exist.
    """
    pass


class WrongModifierError(InstructionNotValidError):
    """
    Raised when modifier doesn't exist.
    """
    pass


class WrongAddressingModeError(InstructionNotValidError):
    """
    Raised when addressing mode doesn't exist.
    """
    pass


class WarriorNotValidError(Exception):
    pass


class NoWarriorsError(WarriorNotValidError):
    """
    Raised when there are no warriors given.
    """
    pass


class WarriorSizeError(WarriorNotValidError):
    """
    Raised when there are no warriors given.
    """
    pass
