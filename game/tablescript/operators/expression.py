

class Expression:

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

        # - Pass trough tree generation
        self.exp.generate_tree(id_manager)
        self.tree = self.exp.tree

    def evaluate(self, scope, options):

        # - Pass trough evaluation
        self.exp.evaluate(scope, options)

        self.stack = self.exp.stack
        self.result = self.exp.result
        self.errors = self.exp.errors
