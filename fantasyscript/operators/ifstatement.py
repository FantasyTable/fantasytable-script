from ..datatypes.scope import Scope
from . import *


class IfStatement:

    def __init__(self, exp=[]):

        # - Set expression
        self.exp = exp

        if len(exp) > 1:
            self.cond = exp[0]
            self.true = exp[1]
            self.false = exp[2]

        # - Initialize values
        self.id = 0
        self.tree = {}
        self.errors = []
        self.stack = {}
        self.refs = {}
        self.result = None

    def generate_tree(self, id_manager):

        if pass_trough_tree(self, id_manager):
            return

        # - Set id for this expression
        self.id = id_manager.get_id()

        # - Generate tree for all expressions
        self.cond.generate_tree(id_manager)
        self.true.generate_tree(id_manager)
        self.false.generate_tree(id_manager)

        self.tree = \
        {
            "type": "three",
            "op": "if",
            "id": self.id,
            "condition": self.cond.tree,
            "true": self.true.tree,
            "false": self.false.tree
        }

    def evaluate(self, scope, options):

        if pass_trough_calc(self, scope, options):
            return

        # - Evaluate condition expression
        self.cond.evaluate(scope, options)

        # - Merge all expressions result
        self.errors += self.cond.errors
        self.stack.update(self.cond.stack)

        if len(self.errors) != 0:
            return

        cond_result = self.cond.result.value

        if cond_result:
            # - Evaluate condition expression
            self.true.evaluate(scope, options)

            # - Merge all expressions result
            self.errors += self.true.errors
            self.stack.update(self.true.stack)

            if len(self.errors) != 0:
                return

            self.result = self.true.result

        else:
            # - Evaluate condition expression
            self.false.evaluate(scope, options)

            # - Merge all expressions result
            self.errors += self.false.errors
            self.stack.update(self.false.stack)

            if len(self.errors) != 0:
                return

            self.result = self.false.result

        # - Update the evaluation stack
        self.stack.update({self.id: self.result})
