from ..datatypes.arraybox import ArrayBox
from . import *


class Merge:

    def __init__(self, exp):

        # - Set expression
        self.exp = exp

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
        self.exp[0].generate_tree(id_manager)
        self.tree = self.exp[0].tree

        for exp in self.exp[1:]:

            # - Set id for this expression
            self.id.append(id_manager.get_id())

            # - Generate tree for operand
            exp.generate_tree(id_manager)

            self.tree = \
            {
                "type": "infix",
                "op": "::",
                "id": self.id[-1],
                "left": self.tree,
                "right": exp.tree
            }

    def evaluate(self, scope, options):

        if pass_trough_calc(self, scope, options):
            return self

        # - Initialize the result
        self.result = ArrayBox()

        for exp in self.exp:

            # - Evaluate expression
            exp.evaluate(scope, options)

            # - Merge expression
            self.errors += exp.errors
            self.stack.update(exp.stack)

            if len(self.errors) > 0:
                self.result = None
                return

            # - Merge the result array with the calculated expression
            self.result.append(exp.result)

            # - Update the evaluation stack
            self.stack.update({self.id[-1]: self.result})
