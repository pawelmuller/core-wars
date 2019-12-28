from Redcode import Instruction


class MARS():
    def __init__(self, size, cycle_limit, warriors):
        self._MARS = []
        self._size = size
        self._cycle_limit = cycle_limit
        self._warriors = warriors
        for cell in range(self._size):
            self._MARS.append(Instruction(None, "DAT", None, 0, 0))

    def simulate(self):
        # symulacja MARS-a
        pass

    def print_simplified_GUI(self):
        # Wyswietlanie przebiegu gry tekstowo w terminalu
        pass


if __name__ == "__main__":
    test = MARS(8000, 10000, 2)
    print(len(test._MARS))
