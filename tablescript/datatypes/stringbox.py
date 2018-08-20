

class StringBox:

    def __init__(self, init):
        from .floatingbox import FloatingBox
        from .integerbox import IntegerBox
        from .booleanbox import BooleanBox
        from .rollbox import RollBox

        if type(init) == StringBox:
            self.value = init.value

        self.value = str(init)

    def __add__(self, other):
        return StringBox(self.value + str(other))

    def __repr__(self):
        return self.value