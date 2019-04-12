from collections import defaultdict


ORIENTABLE = 'orientable'
LINEAR = 'linear'
NEGATION = '*'


class Equation:
    def __init__(self, equation, bound=None):
        self.letters = self._count_consts(equation)
        self.alphabet_size = len(self.letters)
        self.letter_to_int_mapping = self._create_letter_to_int_mapping(
            self.letters)
        self.int_to_letter_mapping = self._create_int_to_letter_mapping(
            self.letter_to_int_mapping, self.letters)
        self.constants = self._get_constants(equation)
        self.variables = self._find_var_placement(equation)
        self.max_var_size = self._compute_bound(self.constants,
                                                self.variables, bound)
        self.variable_names = self._get_variable_names(equation)

    def _compute_bound(self, consts, vars, bound):
        if bound == None:
            return self._calc_max_var_size(self.constants, self.variables)
        if bound == LINEAR:
            return self._total_const_length(self.constants)
        if bound == ORIENTABLE:
            return self._orientable_bound(self.constants, self.variables)
        return self._nonorientable_bound(self.constants, self.variables)

    def _get_variable_names(self, equation):
        variable_names = []
        for l in equation:
            if l.isupper() and l not in variable_names:
                variable_names.append(l)
        return variable_names

    def _find_var_placement(self, equation):
        var_placement = []
        seen_vars = defaultdict(list)
        no_vars_seen = 0
        for i in range(0, len(equation)):
            l = equation[i]
            if l.islower() or l == NEGATION:
                continue
            negated = False
            if i + 1 < len(equation):
                negated = equation[i + 1] == NEGATION
            if negated:
                seen_vars[l].append(-1 * no_vars_seen)
            else:
                seen_vars[l].append(no_vars_seen)
            no_vars_seen += 1
        for v in seen_vars.keys():
            var_placement.append(seen_vars[v])
        return var_placement

    def _is_orientable(self, vars):
        orientable = True
        for var in vars:
            contains_positive = False
            contains_negative = False
            for loc in var:
                if loc >= 0:
                    contains_positive = True
                else:
                    contains_negative = True
            if not contains_negative or not contains_positive:
                orientable = False
        return orientable

    def is_quadratic(self, vars):
        quadratic = True
        for var in vars:
            if len(var) != 2:
                quadratic = False
        return quadratic

    def _total_const_length(self, constants):
        total_const_length = 0
        for const in constants:
            if len(const) > 0:
                total_const_length += len(const)
        return max(1, total_const_length)

    def _orientable_bound(self, constants, vars):
        return 40 * self._total_const_length(constants) * \
            len(vars)

    def _nonorientable_bound(self, constants, vars):
        return 150 * self._total_const_length(constants) * \
            len(vars)**2

    def _calc_max_var_size(self, constants, vars):
        total_const_length = self._total_const_length(constants)
        if total_const_length == 1:
            return total_const_length
        if self.is_quadratic(vars):
            return (self._orientable_bound(constants, vars)
                    if self._is_orientable(vars)
                    else self._nonorientable_bound(constants, vars))
        return total_const_length

    def _get_constants(self, equation):
        constants_list = self._parse_constants(equation)
        constants = []
        for const in constants_list:
            int_map = self._const_to_int(const)
            constants.append(int_map)
        return constants

    def _const_to_int(self, const):
        int_mapping = []
        last_letter = ''
        do_next = False
        int_rep = 0
        for l in const:
            if l != NEGATION and do_next:
                int_mapping.append(int_rep)
                last_letter = l
            elif do_next:
                int_mapping.append(int_rep * -1)
                do_next = False
                last_letter = ''
            else:
                last_letter = l
                do_next = True
            int_rep = self.letter_to_int_mapping[last_letter]
        if last_letter != '':
            int_mapping.append(int_rep)
        return int_mapping

    def _parse_constants(self, equation):
        constants = []
        const = ''
        last_was_variable = False
        for l in equation:
            if l.isupper():
                constants.append(const)
                const = ''
                last_was_variable = True
            elif not l == NEGATION or not last_was_variable:
                const = const + l
                last_was_variable = False
        constants.append(const)
        return constants

    def _count_consts(self, equation):
        lowercase = [c for c in equation if c.islower()]
        return set(lowercase)

    def _create_letter_to_int_mapping(self, letters):
        mapping = {}
        i = 1
        for c in letters:
            mapping[c] = i
            i += 1
        mapping[''] = 0
        return mapping

    def _create_int_to_letter_mapping(self, mapping, letters):
        r_map = {}
        for l in letters:
            r_map[mapping[l]] = l
            r_map[mapping[l] * -1] = l + NEGATION
        r_map[0] = ''
        return r_map

    def _reducible(self, word):
        last_num = None
        for i in range(0, len(word)):
            if last_num == None:
                last_num = i
                continue
            if word[i] == -1 * word[last_num]:
                return i
            last_num = i
        return -1

    def solves(self, solution):
        filled_in = []
        for i in range(0, len(self.constants)):
            filled_in = filled_in + self.constants[i]
            if i < len(self.constants) - 1:
                variable_name = ''
                inverted = False
                for j in range(0, len(self.variables)):
                    if i in self.variables[j]:
                        variable_name = self.variable_names[j]
                    elif -1 * i in self.variables[j]:
                        inverted = True
                        variable_name = self.variable_names[j]
                value = self._const_to_int(solution[variable_name])
                if inverted:
                    value.reverse()
                    value = list(map(lambda x: -1 * x, value))
                filled_in = filled_in + value
        reduce_at = self._reducible(filled_in)
        while reduce_at >= 0:
            del filled_in[reduce_at]
            del filled_in[reduce_at - 1]
            reduce_at = self._reducible(filled_in)
        return len(filled_in) == 0
