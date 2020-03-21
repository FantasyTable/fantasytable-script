from ..datatypes.arraybox import ArrayBox


class Array:

    def __init__(self, exp=None):

        # - Set expression
        self.exp = exp
        if exp is None:
            self.exp = []

        # - Initialize values
        self.id = []
        self.tree = {}
        self.errors = []
        self.stack = {}
        self.refs = []
        self.result = None

    def generate_tree(self, id_manager):

        # - Set id for this expression
        self.id = id_manager.get_id()

        # - Generate tree for each element
        for exp in self.exp:
            exp.generate_tree(id_manager)

        self.tree = \
        {
            "type": "array",
            "id": self.id,
            "value": [elem.tree for elem in self.exp]
        }

    def evaluate(self, scope, options):

        for exp in self.exp:

            # - Evaluate each element
            exp.evaluate(scope, options)

            # - Merge all expressions result
            self.errors += exp.errors
            self.stack.update(exp.stack)

        # - Box all values in an array box
        self.result = ArrayBox([value.result for value in self.exp])

        # - Update the evaluation stack
        self.stack.update({self.id: self.result})

        return self
