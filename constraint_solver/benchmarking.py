import argparse
import csv
import random
import time
import statistics

from solver.solver import Solver, run
from solver.equation import Equation
from solver.generator import Generator


ALPHABET_SIZE = 3

parser = argparse.ArgumentParser("Profile constraint solver.")
parser.add_argument('--equation', type=str, required=True,
                    help="What type of equation generate. The " +
                    "options are: linear, quadratic.")
parser.add_argument('--variable', type=str, required=True,
                    help="The variable to vary: noVars, constSize.")
parser.add_argument('--min', type=int, required=True,
                    help="The minimum variable value")
parser.add_argument('--max', type=int, required=True,
                    help="The maximum variable value")
parser.add_argument('--intervaltype', type=str, required=True,
                    help="Logarithmically or linearly scale from min " +
                    "to max: linear, logarithmic.")
parser.add_argument('--interval', type=int, required=True,
                    help="Interval size.")
parser.add_argument('--invariant', type=int, required=True,
                    help="Invariant value.")
parser.add_argument('--solvability', action='store_true',
                    help="Run until only one solution is found.")
parser.add_argument('--solvable', action='store_true',
                    help="Whether the equation must be solvable.")
parser.add_argument('--bound', type=str, required=True,
                    help="What bound to put on variable size.")
parser.add_argument('--savefile', type=str, required=False,
                    default='./', help="Where to save output.")
parser.add_argument('--verbose', action='store_true',
                    help="Whether the solver should print output.")
parser.add_argument('--repetitions', type=int, default=1,
                    help="Number of times to run same experiment.")
parser.add_argument('--incrementbounds', action='store_true',
                    help="Whether to incrementally increase bound on " +
                    "variable value size. Can only be true for " +
                    "solvability problems.")


def construct_file_name(savefile, equationtype, variable, min, max):
    return savefile + equationtype + "_" + variable + "_" + \
        str(min) + "_" + str(max) + ".csv"


def main():
    all_args = vars(parser.parse_args())
    file_name = construct_file_name(all_args['savefile'],
                                    all_args['equation'],
                                    all_args['variable'],
                                    all_args['min'],
                                    all_args['max'])
    with open(file_name, 'w+') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([all_args['variable'], 'time'])
        var_val = all_args['min']
        while var_val <= all_args['max']:
            results = []
            for i in range(0, all_args['repetitions']):
                if all_args['variable'] == 'constSize':
                    g = Generator(var_val, all_args['invariant'],
                                  ALPHABET_SIZE, all_args['solvable'])
                else:
                    g = Generator(all_args['invariant'], var_val,
                                  ALPHABET_SIZE, all_args['solvable'])
                if all_args['equation'] == 'linear':
                    equation = g.generate_linear()
                else:
                    equation = g.generate_quadratic()
                print(equation)
                start = int(round(time.time() * 1000))
                run(equation, all_args['solvability'], all_args['bound'],
                    all_args['incrementbounds'], verbose=all_args['verbose'])
                end = int(round(time.time() * 1000))
                diff = end - start
                results.append(diff)
            writer.writerow([var_val, statistics.mean(results)])
            if all_args['intervaltype'] == "logarithmic":
                var_val *= all_args['interval']
            else:
                var_val += all_args['interval']


if __name__ == '__main__':
    main()
