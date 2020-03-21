from ..datatypes.scope import *


class Struct:

    def __init__(self, exp=None):

        # - Set expression
        self.exp = exp

        if exp:
            # - Get roll expressions
            self.labels = exp[::2]
            self.values = exp[1::2]

        # - Initialize values
        self.id = 0
        self.tree = {}
        self.errors = []
        self.stack = {}
        self.refs = {}
        self.result = Scope({})

    def generate_tree(self, id_manager):

        values = []
        if self.exp:
            for i in range(0, len(self.labels)):
                label = self.labels[i]
                value = self.values[i]

                # - Generate tree for values
                value.generate_tree(id_manager)

                values.append({label: value.tree})

        # - Set id for this expression
        self.id = id_manager.get_id()

        self.tree = \
        {
            "type": "scope",
            "id": self.id,
            "values": values
        }

    def evaluate(self, scope, options):

        if not self.exp:
            return

        self.result = {}
        for i in range(0, len(self.labels)):
            label = self.labels[i]
            value = self.values[i]

            value.evaluate(scope, options)

            # - Merge all expressions result
            self.errors += value.errors
            self.stack.update(value.stack)

            if len(self.errors) != 0:
                return

            self.result[label] = value.result.value

        self.result = Scope(self.result)

        # - Update the stack
        self.stack.update({self.id: self.result})
