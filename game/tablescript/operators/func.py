from ..datatypes.scope import Scope
from . import *


class Func:

    def __init__(self, exp):

        # - Set expression
        self.exp = exp

        # - Get expressions
        if type(exp) == list:
            self.params_exp = exp[1:-1]
            self.statement_exp = exp[-1]

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
        self.statement_exp.generate_tree(id_manager)

        self.tree = \
        {
            "type": "postfix",
            "op": "func",
            "id": self.id,
            "statement": self.statement_exp.tree,
            "params": [exp for exp in self.params_exp]
        }

    def evaluate(self, scope, options):

        if pass_trough_calc(self, scope, options):
            return

        def evaluate_internal(*parameters):
            errors = []

            if len(parameters) != len(self.params_exp):
                errors += {"description": "Calling arguments does not match the function parameters.", "id": self.id}

            internal_context = {}
            for i, label in enumerate(self.params_exp):
                internal_context[label] = parameters[i]

            internal_scope = Scope(internal_context).merge(scope)

            # - Abort if errors
            if len(self.errors) > 0:
                raise errors
                return None

            # - Evaluate and merge context expression
            self.statement_exp.evaluate(internal_scope, options)

            # - Abort if errors
            if len(self.statement_exp.errors) > 0:
                raise IndexError(self.statement_exp.errors)
                return None

            return self.statement_exp.result

        # - Return the function callable
        self.result = evaluate_internal

        # - Update the evaluation stack
        self.stack.update({self.id: self.result})
