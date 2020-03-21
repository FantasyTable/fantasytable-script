from ..datatypes.scope import Scope as ScopeBox
from . import *


class Scope:

    def __init__(self, exp):

        # - Set expression
        self.exp = exp

        # - Get roll expressions
        if type(exp) is list and len(exp) > 1:
            self.target_exp = exp[-1]
            self.naming_exp = exp[0:-1]

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

        # - First element tree
        self.naming_exp[0].generate_tree(id_manager)
        self.tree = self.naming_exp[0].tree

        for naming in self.exp[1:]:

            # - Set id for this expression
            self.id.append(id_manager.get_id())

            # - Generate tree for all namings
            naming.generate_tree(id_manager)

            self.tree = \
            {
                "type": "infix",
                "op": "in",
                "id": self.id[-1],
                "left": self.tree,
                "right": naming.tree
            }

    def evaluate(self, scope, options):

        if pass_trough_calc(self, scope, options):
            return

        i = 0

        for exp in self.naming_exp:

            # - Evaluate each naming expression
            exp.evaluate(scope, options)

            # - Merge errors and stack
            self.errors += exp.errors
            self.stack.update(exp.stack)

            # - The result must be a scope
            if type(exp.result) != ScopeBox:
                self.errors += [{"description": "Cannot use an expression as scope", "id": self.id[i]}]

            # - If we have an error stop
            if len(self.errors) > 0:
                self.result = None
                return

            # - Merge the scope for the next expression
            scope = scope.merge(exp.result)

            # - Update the stack with this naming expression
            self.stack.update({self.id[i]: scope})

            i = i + 1

        # - Evaluate and merge context expression
        self.target_exp.evaluate(scope, options)
        self.errors += self.target_exp.errors
        self.stack.update(self.target_exp.stack)

        self.result = self.target_exp.result


