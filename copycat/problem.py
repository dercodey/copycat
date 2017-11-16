from .copycat import Copycat

from pprint import pprint

class Problem:
    def __init__(self, initial, modified, target, iterations, distributions=None, formulas=None):
        self.initial  = initial
        self.modified = modified
        self.target   = target

        self.iterations    = iterations
        if distributions is None:
            self.distributions = self.solve()
        else:
            self.distributions = distributions
        self.formulas      = formulas
        if formulas is not None:
            assert hasattr(Copycat().workspace, 'temperature')

    def test(self, comparison, expected=None):
        print('-' * 120)
        print('Testing copycat problem: {} : {} :: {} : _'.format(self.initial,
                                                                  self.modified,
                                                                  self.target))
        print('expected:')
        if expected is None:
            expected = self.distributions
        pprint(expected)

        actual = self.solve()
        print('actual:')
        pprint(actual)
        comparison(actual, expected)
        print('-' * 120)

    def solve(self):
        copycat = Copycat()
        answers  = dict()
        if self.formulas == None:
            if hasattr(copycat.workspace, 'temperature'):
                formula = copycat.workspace.temperature.getAdj()
            else:
                formula = None
            answers[formula] = copycat.run(self.initial,
                                self.modified,
                                self.target,
                                self.iterations)
        else:
            for formula in self.formulas:
                copycat.temperature.useAdj(formula)
                answers[formulas] = copycat.run(self.initial,
                                        self.modified,
                                        self.target,
                                        self.iterations)
        return answers

    def generate(self):
        self.distributions = self.solve()
