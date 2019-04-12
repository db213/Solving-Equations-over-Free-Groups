import argparse

from solver.solver import Solver, run

parser = argparse.ArgumentParser(
    description="Solve equations over free groups.")
parser.add_argument('--equation', type=str, required=True,
                    help="The equation: constants must be in lower" +
                    " case and variables in upper case. No numbers." +
                    " Letters followed by asterisks are inverted.")
parser.add_argument('--solvability', help="Check only if the equation " +
                    "is solvable.", action='store_true')
parser.add_argument('--bound', help="What bound to place on the " +
                    "variable size. Options are: linear, orientable, " +
                    "nonorientable.", type=str)
parser.add_argument('--verbose', action='store_true',
                    help="Whether the solver should print solutions.")
parser.add_argument('--incrementbounds', action='store_false',
                    help="Whether to incrementally increase bound on " +
                    "variable value size. Can only be true for " +
                    "solvability problems.")

all_args = vars(parser.parse_args())
solved = run(all_args['equation'], all_args['solvability'],
             all_args['bound'], all_args['incrementbounds'],
             all_args['verbose'])
if solved:
    print("SOLVABLE")
else:
    print("UNSOLVABLE")
