from . import *


class Parenthesis:

    def __init__(self, exp):

        # - Set expression
        self.exp = exp

        # - Initialize values
        self.id = 0
        self.tree = {}
        self.errors = []
        self.stack = {}
        self.refs = []
        self.result = None

    def generate_tree(self, id_manager):

        # - Set id for this expression
        self.id = id_manager.get_id()

        # - Generate tree for the expression
        self.exp.generate_tree(id_manager)

        self.tree = \
        {
            "type": "parenthesis",
            "id": self.id,
            "content": self.exp.tree,
        }

    def evaluate(self, scope, options):

        # - Evaluated the target expression
        self.exp.evaluate(scope, options)

        # - Merge results
        self.result = self.exp.result
        self.errors = self.exp.errors
        self.stack = {}

        # - Update the evaluation stack
        self.stack.update({self.id: self.result})
