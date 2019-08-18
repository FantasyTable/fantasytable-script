from ..datatypes.scope import Scope
from ..datatypes.boxed import Boxed
from ..datatypes import convert_type
from . import *


class Access:

    def __init__(self, exp):

        # - Set expression
        self.exp = exp

        # - Get expressions
        if type(exp) is list and len(exp) > 1:
            self.context_exp = exp[0]
            self.access_exp = exp[1]

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
        self.context_exp.generate_tree(id_manager)
        self.access_exp.generate_tree(id_manager)

        self.tree = \
        {
            "type": "infix",
            "op": ".",
            "id": self.id,
            "left": self.context_exp.tree,
            "right": self.access_exp.tree
        }

    def evaluate(self, scope, options):

        if pass_trough_calc(self, scope, options):
            return

        # - Evaluate and merge context expression
        self.context_exp.evaluate(scope, options)
        self.errors += self.context_exp.errors
        self.stack.update(self.context_exp.stack)

        scope = self.context_exp.result

        # - Invalid context ?
        if type(scope) != Scope:
            scope = convert_type(scope, options["deepScope"])

        if isinstance(scope, Boxed):
            scope = Scope(scope.scope)

        if type(scope) != Scope:
            self.errors += [{"description": "There's no accessible label on the left.", "id": self.id}]
            self.result = None

        # - Abort if errors
        if len(self.errors) > 0:
            self.result = None
            return

        # - Evaluate and merge access expression
        self.access_exp.evaluate(scope, options)
        self.errors += self.access_exp.errors
        self.stack.update(self.access_exp.stack)

        if len(self.errors) > 0:
            self.result = None
            return

        # - Get the result from the scope access
        self.result = self.access_exp.result

        # - Update the evaluation stack
        self.stack.update({self.id: self.result})
