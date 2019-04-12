from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
from solver.equation import Equation
from ortools.sat.python import cp_model


class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, r_map, var_start_locs, variables, max_var_size,
                 variable_names, E, M, limit=None, verbose=True):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._r_map = r_map
        self._var_start_locs = var_start_locs
        self._variables = variables
        self._max_var_size = max_var_size
        self._variable_names = variable_names
        self._solution_count = 0
        self._E = E
        self._M = M
        self._found_solutions = []
        self._solution_limit = limit
        self._verbose = verbose

    def on_solution_callback(self):
        j = 0
        solution = {}
        for loc in self._var_start_locs:
            if (j < len(self._variable_names) and
                    self._variable_names[j] not in solution):
                value = ''
                for i in range(0, self._max_var_size):
                    value += self._r_map[self.Value(self._E[loc + i])]
                solution[self._variable_names[j]] = value
                j = j + 1
        if solution not in self._found_solutions:
            self._solution_count += 1
            if self._verbose:
                print(solution)
            self._found_solutions.append(solution)

        if (self._solution_limit and
                self._solution_count >= self._solution_limit):
            self.StopSearch()

    @property
    def solution_count(self):
        return self._solution_count

    @property
    def solutions(self):
        return self._found_solutions

    @property
    def verbose(self):
        return self._verbose


class Solver:
    def __init__(self, e, solvability, verbose=True):
        # Initialize constraint model.
        self._model = cp_model.CpModel()

        self.equation = e
        self._constant_length = sum(len(i) for i in e.constants)
        eq_length = self._constant_length + \
            (len(e.constants) - 1) * e.max_var_size

        # Initialize model variables.
        E = self._initialize_equation_variables(e.alphabet_size, eq_length)
        M = self._initialize_cancellation_assignment_variables(eq_length)

        # Set constraints.
        self._constraints(e, eq_length, E, M)

        # Initialize solution printer.
        limit = 1 if solvability else None
        self._printer = SolutionPrinter(e.int_to_letter_mapping,
                                        self.var_start_locs, e.variables,
                                        e.max_var_size, e.variable_names, E,
                                        M, limit=limit, verbose=verbose)

    def _initialize_equation_variables(self, bound, eq_length):
        return [self._model.NewIntVar(-1 * bound, bound, "E_%d" % i)
                for i in range(0, eq_length)]

    def _initialize_cancellation_assignment_variables(self, eq_length):
        return [self._model.NewIntVar(0, eq_length - 1, "M_%d" % i)
                for i in range(0, eq_length)]

    def _constraints(self, e, eq_length, E, M):
        # All the mappings must be to distinct elements.
        self._model.AddAllDifferent(M)

        # Set the elements in E that correspond to given constants.
        self.var_start_locs = self._constant_values_constraints(
            e.constants, E, e.max_var_size)

        # Ensure all letters of multiply recurring variables are the same.
        self._variable_continuity_constraints(E, self.var_start_locs,
                                              e.variables, e.max_var_size)

        # Everything between a pair or reducing letters reduces amongst
        # themselves, and every identity reduces with itself.
        self._reduce_between_constraints(eq_length, E, M)

        # All identities must be at the end of the variable.
        self._variable_ones_last_constraints(E, self.var_start_locs,
                                             e.max_var_size, e.variables)

        # No variable can have inverse elements adjacent to each other.
        self._variables_reduced_constraints(E, M, self.var_start_locs,
                                            e.max_var_size)

    def _constant_values_constraints(self, constants, E, max_var_size):
        i = 0
        var_start_locs = []
        for const in constants:
            if len(const) > 0:
                for c in const:
                    self._model.Add(E[i] == c)
                    i += 1
            if i < len(E):
                var_start_locs.append(i)
                i = i + max_var_size
        return var_start_locs

    def _variable_continuity_constraints(self, E, var_start_locs,
                                         variables, max_var_size):
        for var in variables:
            v_first = list(filter(lambda x: x >= 0, var))[0]
            for j in range(0, len(var)):
                if var[j] >= 0 and j != var.index(v_first):
                    for i in range(0, max_var_size):
                        self._model.Add(E[var_start_locs[v_first] + i]
                                        == E[var_start_locs[var[j]] + i])
                elif var[j] < 0:
                    i = 0
                    k = max_var_size - 1
                    while i < max_var_size:
                        postive_index = var_start_locs[v_first] + i
                        negative_index = var_start_locs[-1 * var[j]] + \
                            k - i
                        self._model.Add(E[postive_index] == -1 *
                                        E[negative_index])
                        i += 1

    def _reduce_between_constraints(self, eq_length, E, M):
        for i in range(0, eq_length):
            self._identity_maps_to_self_constraint(E, M, i)
            for j in range(0, eq_length):
                self._reflexive_constraints(E, M, i, j)
                if i < j:
                    self._between_reduces_constraints(E, M, i, j)

    def _variable_ones_last_constraints(self, E, var_start_locs,
                                        max_var_size, variables):
        for var in variables:
            for v in var:
                if v >= 0:
                    start_loc = var_start_locs[v]
                    for i in range(0, max_var_size - 1):
                        a = self._model.NewBoolVar('')
                        (self._model.Add(E[start_loc + i] == 0)
                         .OnlyEnforceIf(a))
                        (self._model.Add(E[start_loc + i] != 0)
                         .OnlyEnforceIf(a.Not()))
                        (self._model.Add(E[start_loc + i + 1] == 0)
                         .OnlyEnforceIf(a))
                else:
                    end_loc = var_start_locs[-1 * v] + max_var_size - 1
                    for i in range(0, max_var_size - 2):
                        a = self._model.NewBoolVar('')
                        (self._model.Add(E[end_loc - i] == 0)
                         .OnlyEnforceIf(a))
                        (self._model.Add(E[end_loc - i] != 0)
                         .OnlyEnforceIf(a.Not()))
                        (self._model.Add(E[end_loc - i - 1] == 0)
                         .OnlyEnforceIf(a))

    def _variables_reduced_constraints(self, E, M, var_start_locs, max_var_size):
        for v in var_start_locs:
            for i in range(1, max_var_size):
                a = self._model.NewBoolVar('')
                self._model.Add(E[v + i - 1] != 0).OnlyEnforceIf(a)
                self._model.Add(E[v + i - 1] == 0).OnlyEnforceIf(a.Not())
                (self._model.Add(E[v + i - 1] != -1 * E[v + i])
                 .OnlyEnforceIf(a))

    def _identity_maps_to_self_constraint(self, E, M, i):
        a = self._model.NewBoolVar("")
        self._model.Add(E[i] == 0).OnlyEnforceIf(a)
        self._model.Add(E[i] != 0).OnlyEnforceIf(a.Not())
        self._model.Add(M[i] == i).OnlyEnforceIf(a)
        self._model.Add(M[i] != i).OnlyEnforceIf(a.Not())

    def _reflexive_constraints(self, E, M, i, j):
        b = self._model.NewBoolVar("")
        self._model.Add(j == M[i]).OnlyEnforceIf(b)
        self._model.Add(j != M[i]).OnlyEnforceIf(b.Not())
        self._model.Add(M[j] == i).OnlyEnforceIf(b)
        self._model.Add(M[j] != i).OnlyEnforceIf(b.Not())
        self._model.Add(E[i] == -1 * E[j]).OnlyEnforceIf(b)

    def _between_reduces_constraints(self, E, M, i, j):
        c = self._model.NewBoolVar("")
        self._model.Add(j < M[i]).OnlyEnforceIf(c)
        self._model.Add(j >= M[i]).OnlyEnforceIf(c.Not())
        self._model.Add(i < M[j]).OnlyEnforceIf(c)
        self._model.Add(M[j] < M[i]).OnlyEnforceIf(c)

    def solve(self):
        solver = cp_model.CpSolver()
        if (self.equation.is_quadratic(self.equation.variables) and
                self._constant_length % 2 != 0):
            self.solvable = False
        else:
            status = solver.SearchForAllSolutions(self._model, self._printer)
            self.solvable = status == cp_model.FEASIBLE
            if self.solvable and self._printer.verbose:
                print("SOLUTIONS: " + str(self._printer.solution_count))

    @property
    def solution_printer(self):
        return self._printer


def run(equation, solvability, bound, incrementbound, verbose=False):
    equation = Equation(equation, bound)
    solved = False
    min_var_size = (int(equation.max_var_size /
                        2) if (solvability and incrementbound)
                    else equation.max_var_size)
    max_var_size = equation.max_var_size
    for i in range(min_var_size, max_var_size + 1, 2):
        equation.max_var_size = i
        solver = Solver(equation, solvability, verbose=verbose)
        solver.solve()
        solved = solver.solvable
        if solved:
            break
    return solved
