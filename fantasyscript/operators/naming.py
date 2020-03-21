from ..datatypes.scope import Scope
from . import *


class Naming:

    def __init__(self, exp):

        # - Set expression
        self.exp = exp

        # - Get roll expressions
        if type(exp) is list and len(exp) > 1:
            self.exp_value = exp[0]
            self.exp_name = exp[1]

        # - Initialize values
        self.id = 0
        self.tree = {}
        self.errors = []
        self.stack = {}
        self.refs = []
        self.result = None

    def generate_tree(self, id_manager):

        if pass_trough_tree(self, id_manager):
            return

        # - Set id for this expression
        self.id = id_manager.get_id()

        # - Generate tree for exp value
        self.exp_value.generate_tree(id_manager)

        self.tree = \
        {
            "type": "infix",
            "op": "as",
            "id": self.id,
            "left": self.exp_value.tree,
            "right": self.exp_name
        }

    def evaluate(self, scope, options):

        if pass_trough_calc(self, scope, options):
            return

        # - Evaluate the expression value
        self.exp_value.evaluate(scope, options)

        # - Merge the result
        self.errors += self.exp_value.errors
        self.stack.update(self.exp_value.stack)

        # - Check for errors
        if len(self.errors) > 0:
            self.result = None
            return

        # - Return a new scope which have the new value
        self.result = Scope({self.exp[1]: self.exp[0].result})

        # - Update the stack
        self.stack.update({self.id: self.result})
