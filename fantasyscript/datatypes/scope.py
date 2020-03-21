

class Scope:

    def __init__(self, namedValues):
        self.value = namedValues

    def merge(self, other):
        nd = self.value.copy()
        nd.update(other.value)
        return Scope(nd)
