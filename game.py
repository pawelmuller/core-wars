import argparse
from MARS import MARS
from warrior import Warrior

if __name__ == "__main__":
    # Parsing arguments
    parser = argparse.ArgumentParser("MARS simulator")
    parser.add_argument("-coresize", type=int,
                        help="Set the core size.", default=4000)
    parser.add_argument("-cycleslimit", type=int,
                        help="Cycles to run until tie.", default=8000)
    parser.add_argument("warriors", type=str, nargs="*",
                        help="Path to two warriors.")

    arguments = parser.parse_args()

    # Creating list of Warrior objects created from pathways given as arguments
    warriors = [Warrior(path) for path in arguments.warriors]

    # Core initiation
    core = MARS(arguments.coresize, arguments.cycleslimit, warriors)
    core.prepare_for_simulation()

    # Core simulation
    core.simulate_core()

    # Game results
    core.results()
