from ..datatypes.stringbox import *


class String:

    def __init__(self, exp):

        # - Set expression
        self.exp = exp

        # - Get roll expressions
        self.string_value = exp[1:-1]

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
            "type": "string",
            "id": self.id
        }

    def evaluate(self, scope, options):

        try:
            # - Try parsing the string value
            self.result = StringBox(self.string_value)
        except:
            desc = "Can't convert '" + self.exp + "' to string."
            self.errors  += [{"description": desc, "id": self.id}]
            self.result = None

        # - Update the stack
        self.stack.update({self.id: self.result})
