from warrior import Warrior
from Redcode import Instruction


def test_Warrior_import_from_file():
    instructions = [
        Instruction("ADD #4, 3"),
        Instruction("        MOV 2, @2"),
        Instruction("JMP -2"),
        Instruction("        DAT #0, #0")
    ]
    warrior = Warrior("Warriors/Dwarf.red")
    for correct, test in zip(instructions, warrior._instructions):
        assert correct.compare(test)
