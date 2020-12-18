from ..datatypes import *


class Call:

    def __init__(self, exp=[]):

        # - Set expression
        self.exp = exp

        # - Get expressions
        if type(exp) == list:
            self.params_exp = exp

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
        for exp in self.params_exp:
            exp.generate_tree(id_manager)

        self.tree = \
        {
            "type": "postfix",
            "op": "(.)",
            "id": self.id,
            "target": input_tree,
            "params": [exp.tree for exp in self.params_exp]
        }

    def evaluate(self, scope, options, input_scope=None):

        # - Invalid context ?
        if not callable(input_scope):
            self.errors += [{"description": "The left argument is not a function", "id": self.id}]
            self.result = None

        # - Abort if errors
        if len(self.errors) > 0:
            self.result = None
            return

        for param in self.params_exp:
            # - Evaluate and merge expressions
            param.evaluate(scope, options)
            self.errors += param.errors
            self.stack.update(param.stack)

        if len(self.errors) > 0:
            self.result = None
            return

        params = [param.result for param in self.params_exp]

        try:
            # - Get the result from the called function
            self.result = input_scope(*params)
            self.result, errors, stack, tree = convert_type(self.result, options["deepScope"], options["externalCall"], self.id)
            self.errors += errors
            self.stack.update(stack)
            self.tree["internal"] = tree
        except IndexError as error:
            self.errors += error.args
        except Exception as ex:
            self.errors += [{"description": str(ex), "id": self.id}]

        if len(self.errors) > 0:
            self.result = None
            return

        # - Update the evaluation stack
        self.stack.update({self.id: self.result})
