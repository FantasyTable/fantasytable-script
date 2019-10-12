

class TResult:

    def __init__(self, result, errors, stack, tree):

        self.value = result
        self.errors = errors
        self.stack = stack
        self.tree = tree
