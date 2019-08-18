from . import *


class Prefix:

    def __init__(self, exp):

        # - Set expression
        self.exp = exp

        # - Get expressions
        if type(exp) is list and len(exp) > 1:
            self.operators = exp[0:-1].reverse()
            self.value_exp = exp[-1]

        # - Initialize values
        self.id = []
        self.tree = {}
        self.errors = []
        self.stack = {}
        self.refs = []
        self.result = None

    def generate_tree(self, id_manager):

        if pass_trough_tree(self, id_manager):
            return

        # - Generate tree for the expression value
        self.value_exp.generate_tree(id_manager)
        self.tree = self.value_exp.tree

        for op in self.operators:
            # - Set id for this expression
            self.id.append(id_manager.get_id())

            self.tree = \
            {
                "type": "prefix",
                "op": op,
                "id": self.id[-1],
                "right": self.tree
            }

    def evaluate(self, scope, options):

        if pass_trough_calc(self, scope, options):
            return

        # - Calculate expression value and merge
        self.value_exp.evaluate(scope, options)
        self.stack = self.value_exp.stack
        self.errors = self.value_exp.errors
        self.result = self.value_exp.result

        id = 1

        for op in self.operators:

            if op == '-':
                self.result = -self.result
            elif op == '!':
                self.result = self.result.inv()

            # - Update the evaluation stack
            self.stack.update({self.id[-id]: self.result})

            id = id + 1
