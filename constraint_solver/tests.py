import unittest
from solver.equation import Equation
from solver.solver import Solver
from solver.generator import Generator


class Test(unittest.TestCase):
    def test_equation_parse(self):
        e = Equation("aXa")
        self.assertEqual(e.letters, {'a'})
        self.assertEqual(e.alphabet_size, 1)
        self.assertEqual(e.constants, [[1], [1]])
        self.assertEqual(e.variables, [[0]])
        self.assertEqual(e.variable_names, ['X'])
        self.assertEqual(e.max_var_size, 2)

    def test_automatic_bounds(self):
        e = Equation("aXbY")
        self.assertEqual(e.max_var_size, 2)
        e = Equation("aaXbbXaa")
        self.assertEqual(e.max_var_size, 900)
        e = Equation("aaXbbXaa", "linear")
        self.assertEqual(e.max_var_size, 6)
        e = Equation("aaXYbbXYaa")
        self.assertEqual(e.max_var_size, 900 * 4)
        e = Equation("aaXYbbXYaa", "linear")
        self.assertEqual(e.max_var_size, 6)
        e = Equation("aaXYbbXYaa", "orientable")
        self.assertEqual(e.max_var_size, 80 * 6)
        e = Equation("aaXYbbX*Y*aa")
        self.assertEqual(e.max_var_size, 40 * 2 * 6)
        e = Equation("aaXYbbX*Y*aa", "nonorientable")
        self.assertEqual(e.max_var_size, 900 * 4)

    def test_variable_names(self):
        e = Equation("XYZ")
        self.assertEqual(e.variable_names, ['X', 'Y', 'Z'])
        e = Equation("XYX*Y*")
        self.assertEqual(e.variable_names, ['X', 'Y'])

    def test_var_placement(self):
        e = Equation("XYZ")
        self.assertEqual(e.variables, [[0], [1], [2]])
        e = Equation("aaaX")
        self.assertEqual(e.variables, [[0]])
        e = Equation("XYXY")
        self.assertEqual(e.variables, [[0, 2], [1, 3]])
        e = Equation("XYX*Z*")
        self.assertEqual(e.variables, [[0, -2], [1], [-3]])

    def test_parse_constants(self):
        e = Equation("aaaXbbb")
        self.assertTrue([1, 1, 1] in e.constants)
        self.assertTrue([2, 2, 2] in e.constants)
        e = Equation("aXa*")
        self.assertEqual(e.constants, [[1], [-1]])
        e = Equation("X")
        self.assertEqual(e.constants, [[], []])

    def test_alphabet_size(self):
        e = Equation("abcdefg")
        self.assertEqual(e.alphabet_size, 7)
        e = Equation("X")
        self.assertEqual(e.alphabet_size, 0)
        e = Equation("aXa*")
        self.assertEqual(e.alphabet_size, 1)

    def test_solves_linear(self):
        e = Equation("aXa")
        solver = Solver(e, True, verbose=False)
        solver.solve()
        self.assertTrue(solver.solvable)
        solutions = solver.solution_printer.solutions
        self.assertEqual(len(solutions), 1)
        self.assertTrue(e.solves(solutions[0]))

        e = Equation("aaXbbYba*")
        solver = Solver(e, False, verbose=False)
        solver.solve()
        self.assertTrue(solver.solvable)
        solutions = solver.solution_printer.solutions
        self.assertTrue(len(solutions) > 1)
        for solution in solutions:
            self.assertTrue(e.solves(solution))

    def test_solves_quadratic(self):
        e = Equation("aXba*X*b*", bound='linear')
        solver = Solver(e, False, verbose=False)
        solver.solve()
        self.assertTrue(solver.solvable)
        solutions = solver.solution_printer.solutions
        for solution in solutions:
            self.assertTrue(e.solves(solution))

    def test_solve_no_constants(self):
        e = Equation("XYZ")
        solver = Solver(e, False, verbose=False)
        solver.solve()
        self.assertTrue(solver.solvable)
        solutions = solver.solution_printer.solutions
        self.assertEqual(len(solutions), 1)
        for solution in solutions:
            self.assertTrue(e.solves(solution))

    def test_unsolvable(self):
        e = Equation("abXcX", bound='linear')
        solver = Solver(e, False, verbose=False)
        solver.solve()
        self.assertFalse(solver.solvable)

    def test_random_solvable_quadratics(self):
        for i in range(0, 3):
            g = Generator(1, 2, 3, True)
            e = Equation(g.generate_quadratic(), bound='linear')
            solver = Solver(e, True, verbose=False)
            solver.solve()
            self.assertTrue(solver.solvable)


if __name__ == '__main__':
    unittest.main()
