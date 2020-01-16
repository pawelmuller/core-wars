# PIASKOWNICA - TU SIĘ WSZYSTKO TESTUJE

# from Redcode import Instructions as Ins
# from sys import argv
# from Redcode import Instruction


def blablabla():
    print("aloha")


def test12():
    print("Atrybut!")


if __name__ == "__main__":
    '''
    test1 = {
        "aloha": blablabla,
        "atrybut": test12
    }
    aha = test1["aloha"]
    aha()
    test1["atrybut"]()
    print(Ins)
    print(argv)
    line = "  ;Brokuly i grzyby"
    print(line[1])

    lines = line.rsplit(";")
    print(lines)
    line = line.lstrip()
    if line.lstrip().startswith(";"):
        print("TAK")

    line = "         \n"
    print(line.lstrip())
    print(len(line.lstrip()))

    line = "   spl.b	#2,	}0	;alimentador de processos e incrementa pont."
    str_instruction = line.split(';', maxsplit=1)[0]
    str_instruction = str_instruction.lstrip()
    instruction = str_instruction[0:3].upper()
    print(str_instruction)
    print(instruction)

    default = Instruction(None)
    test = Instruction(None)
    if test == default:
        print("True")
    else:
        print("False")

    line = "ADD.TY 4, 3"
    print(line[1:])

    lista = [0, 1, 2, 3, 4, 5, 6, 7]
    x = 4
    x = lista.index(x) + 1
    lista.insert(x % len(lista), "X")
    print(lista)
    print(lista[-1])

    line = "Warriors/Imp_1.red"
    line2 = "Imp_2.red"
    print(line.split("/")[1])
    print(line2.split("/")[1])

    test = []
    print(test.pop())

    x = 15
    # del x
    print(x)'''

    Redcode_Instructions = {
        "DAT": 123,
        "MOV": 123,
        "ADD": 432,
        "SUB": 65,
        "MUL": 7,
        "DIV": 3,
        "MOD": 6,
    }
    if "MOD" in Redcode_Instructions:
        print("No tak")
