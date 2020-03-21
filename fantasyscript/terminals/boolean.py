from ..datatypes.booleanbox import *


class Boolean:

    def __init__(self, exp):

        # - Set expression
        self.exp = exp

        # - Get roll expressions
        self.boolean_value = exp

        # - Initialize values
        self.id = 0
        self.tree = {}
        self.errors = []
        self.stack = {}
        self.refs = {}
        self.result = None

    def generate_tree(self, id_manager):

        # - Set id for this expression
        self.id = id_manager.get_id()

        self.tree = \
        {
            "type": "boolean",
            "id": self.id
        }

    def evaluate(self, scope, options):

        # - Parse de boolean expression
        is_true = self.boolean_value == "true" or self.boolean_value == "True"

        # - Box the result
        self.result = BooleanBox(is_true)

        # - Update the stack
        self.stack.update({self.id: self.result})
