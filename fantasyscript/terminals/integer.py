from ..datatypes.integerbox import *


class Integer:

    def __init__(self, exp):

        # - Set expression
        self.exp = exp

        # - Get roll expressions
        self.integer_value = exp

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
            "type": "integer",
            "id": self.id
        }

    def evaluate(self, scope, options):

        try:
            # - Try to parse this integer
            self.result = IntegerBox(self.integer_value)
        except:
            desc = "Can't convert '" + self.exp + "' to integer."
            self.errors += [{"description": desc, "id": self.id}]
            self.result = None

        # - Update the evaluation stack
        self.stack.update({self.id: self.result})
