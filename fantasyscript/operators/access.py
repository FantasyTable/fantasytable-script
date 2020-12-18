from ..datatypes.scope import Scope
from ..datatypes.boxed import Boxed
from ..datatypes import convert_type
from . import *


class Access:

    def __init__(self, exp):

        # - Set expression
        self.exp = exp

        # - Get expressions
        self.access_exp = exp

        # - Initialize values
        self.id = 0
        self.tree = {}
        self.errors = []
        self.stack = {}
        self.refs = {}
        self.result = None

    def generate_tree(self, id_manager, input_tree):

        # - Set id for this expression
        self.id = id_manager.get_id()

        # - Generate tree for all expressions
        self.access_exp.generate_tree(id_manager)

        self.tree = \
        {
            "type": "infix",
            "op": ".",
            "id": self.id,
            "left": input_tree,
            "right": self.access_exp.tree
        }

    def evaluate(self, scope, options, input_scope=None):

        # - Invalid context ?
        if type(input_scope) != Scope:
            scope, errors, stack, tree = convert_type(scope, options["deepScope"], options["externalCall"], self.id)
            self.errors += errors

            # - Abort if errors
            if len(self.errors) > 0:
                self.result = None
                return

        if isinstance(input_scope, Boxed):
            input_scope = Scope(input_scope.scope)

        if type(input_scope) != Scope:
            self.errors += [{"description": "There's no accessible label on the left.", "id": self.id}]
            self.result = None

        # - Abort if errors
        if len(self.errors) > 0:
            self.result = None
            return

        # - Evaluate and merge access expression
        self.access_exp.evaluate(input_scope, options)
        self.errors += self.access_exp.errors
        self.stack.update(self.access_exp.stack)

        if len(self.errors) > 0:
            self.result = None
            return

        # - Get the result from the scope access
        self.result = self.access_exp.result

        # - Update the evaluation stack
        self.stack.update({self.id: self.result})
