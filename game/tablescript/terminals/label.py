from ..datatypes import convert_type


class Label:

    def __init__(self, exp):

        # - Set expression
        self.exp = exp

        # - Get roll expressions
        self.label_name = exp

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
            "type": "label",
            "id": self.id
        }

    def evaluate(self, scope, options):

        # - Check if label is in the scope
        if self.label_name not in scope.value:
            raise Exception("There's no '" + self.label_name + "' variable in the scope.")

        # - Get the variable value
        value = scope.value[self.label_name]

        try:
            # - Try to convert to a language type the variable
            self.result = convert_type(value, options["deepScope"])
        except:
            self.errors += \
            [{
                "description": "Unable to convert the variable: " + self.label_name,
                "id": self.id
            }]
            self.result = None

        # - Update the stack
        self.stack.update({self.id: self.result})

        return self
