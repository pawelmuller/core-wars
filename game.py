import argparse
from MARS import MARS
from warrior import Warrior

if __name__ == "__main__":
    # Parsing arguments
    parser = argparse.ArgumentParser("MARS simulator")
    parser.add_argument("-coresize", type=int,
                        help="Set the core size.", default=8000)
    parser.add_argument("-cyclelimit", type=int,
                        help="Cycles to run until tie.", default=10000)
    '''parser.add_argument("-display", type=bool,
                        help="Choose whether to use Terminal or pygame.",
                        default=False)  # False - terminal'''
    parser.add_argument("warriors", type=str, nargs="*",
                        help="Path to at least two warriors.")

    arguments = parser.parse_args()

    # Creating list of Warrior objects created from pathways given as arguments
    warriors = [Warrior(path) for path in arguments.warriors]

    # Core simulation
    core = MARS(arguments.coresize, arguments.cyclelimit, warriors)
    core.prepare_for_simulation()
    core.simulate()

    # Game results (will show the results)
    core.results()
