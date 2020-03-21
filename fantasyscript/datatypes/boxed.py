

class Boxed:

    def __init__(self):

        # - Define a table script scope for all basic types
        self.scope = {}

    def get_scope(self, name):

        if name not in self.scope:
            raise Exception("Function not found")

        return self.scope[name]

    def function(self, name, fn):

        self.scope[name] = fn