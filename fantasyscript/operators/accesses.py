

class Accesses:

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
        self.exp[0].generate_tree(id_manager)
        self.tree = self.exp[0].tree

        for exp in self.exp[1:]:

            # - Pass trough tree generation
            exp.generate_tree(id_manager, self.tree)
            self.tree = exp.tree

    def evaluate(self, scope, options):

        # - Pass trough evaluation
        self.exp[0].evaluate(scope, options)

        self.stack.update(self.exp[0].stack)
        self.result = self.exp[0].result
        self.errors += self.exp[0].errors

        for exp in self.exp[1:]:

            # - Pass trough evaluation
            exp.evaluate(scope, options, self.result)

            self.stack.update(exp.stack)
            self.result = exp.result
            self.errors += exp.errors
