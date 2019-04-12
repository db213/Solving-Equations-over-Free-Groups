import random


START_LETTER = 65


class Generator:
    def __init__(self, const_size, no_vars, alph_size, solvable=False):
        self.c_size = const_size
        self.n_vars = no_vars
        self.solvable = solvable
        self.alph_size = alph_size

    def _invert_constant(self, constant):
        inverted = ''
        negated = False
        for i in range(len(constant) - 1, -1, -1):
            letter = constant[i]
            if letter == '*':
                negated = True
                continue
            inverted += letter
            if not negated:
                inverted += '*'
            negated = False
        return inverted

    def _generate_constant(self, const_size):
        const = ''
        for j in range(0, const_size):
            letter = chr(random.randint(1, self.alph_size) + 96)
            inverse = random.randint(0, 1)
            final_letter = str(letter)
            if inverse == 0:
                final_letter += "*"
            const += final_letter
        return const

    def _unsolvable_quadratic(self):
        equation = ''
        used_vars = {}
        j = 0
        for i in range(0, 2 * self.n_vars + 1):
            equation += self._generate_constant(self.c_size)
            if j < 2 * self.n_vars:
                var_instance = random.randint(0, self.n_vars - 1)
                while (var_instance in used_vars and
                       used_vars[var_instance] == 2):
                    var_instance = random.randint(0, self.n_vars - 1)
                if var_instance not in used_vars:
                    used_vars[var_instance] = 1
                else:
                    used_vars[var_instance] = 2
                equation += chr(START_LETTER + var_instance)
                if used_vars[var_instance] != 1:
                    inverse = random.randint(0, 1)
                    if inverse == 0:
                        equation += '*'
                j += 1
        return equation

    def _solvable_quadratic(self):
        equation = ''
        var_map = {}
        occurred = {}
        for i in range(0, self.n_vars):
            left = self._generate_constant(int(self.c_size / 2))
            right = self._generate_constant(int(self.c_size / 2))
            var_map[i] = (left, right)
        for i in range(0, 2 * self.n_vars):
            r = random.randint(0, self.n_vars - 1)
            while r in occurred and occurred[r] == 2:
                r = random.randint(0, self.n_vars - 1)
            if r in occurred:
                occurred[r] = 2
            else:
                occurred[r] = 1
            invert = 1
            if occurred[r] == 2:
                invert = random.randint(0, 1)
            neighbours = var_map[r]
            if invert == 0:
                equation += self._invert_constant(neighbours[1])
                equation += chr(START_LETTER + r)
                equation += '*'
                equation += self._invert_constant(neighbours[0])
            else:
                equation += neighbours[0]
                equation += chr(START_LETTER + r)
                equation += neighbours[1]
        return equation

    def generate_quadratic(self):
        if self.solvable:
            return self._solvable_quadratic()
        else:
            return self._unsolvable_quadratic()

    def generate_linear(self):
        equation = ''
        for i in range(0, self.n_vars + 1):
            equation += self._generate_constant(self.c_size)
            if i < self.n_vars:
                equation += chr(START_LETTER + i)
        return equation
