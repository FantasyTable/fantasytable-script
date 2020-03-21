from . import *


class Sum:

    def __init__(self, exp):

        # - Set expression
        self.exp = exp

        # - Get expressions
        if type(exp) is list and len(exp) > 1:
            self.values_exp = [e for i, e in enumerate(exp) if i % 2 == 0]
            self.ops_exp = [e for i, e in enumerate(exp) if i % 2 == 1]

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

        # - Generate tree for first expression
        self.values_exp[0].generate_tree(id_manager)
        self.tree = self.values_exp[0].tree

        for i, op in enumerate(self.ops_exp):
            # - Set id for this expression
            self.id.append(id_manager.get_id())

            # - Generate tree for operand
            self.values_exp[i + 1].generate_tree(id_manager)

            self.tree = \
            {
                "type": "infix",
                "op": op,
                "id": self.id[-1],
                "left": self.tree,
                "right": self.values_exp[i + 1].tree
            }

    def evaluate(self, scope, options):

        if pass_trough_calc(self, scope, options):
            return self

        # - Evaluate first expression
        self.values_exp[0].evaluate(scope, options)

        # - Merge first expression
        self.errors += self.values_exp[0].errors
        self.stack.update(self.values_exp[0].stack)

        # - If any error stop
        if len(self.errors) > 0:
            self.result = None
            return

        # - Set base result state
        self.result = self.values_exp[0].result

        for i, op in enumerate(self.ops_exp):

            # - Evaluate operand expression
            self.values_exp[i + 1].evaluate(scope, options)

            # - Merge operand expression
            self.errors += self.values_exp[i + 1].errors
            self.stack.update(self.values_exp[i + 1].stack)

            # - If any error stop
            if len(self.errors) > 0:
                self.result = None
                return

            if op == '+':

                self.result = self.result + self.values_exp[i + 1].result

            elif op == '-':
                self.result = self.result - self.values_exp[i + 1].result

            # - Update the evaluation stack
            self.stack.update({self.id[i // 2]: self.result})
