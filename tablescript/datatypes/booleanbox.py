

class BooleanBox:

    def __init__(self, init):

        if type(init) == BooleanBox:
            self.value = init.value

        elif type(init) == bool:
            self.value = init

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = value

    def inv(self):
        return BooleanBox(not self.value)

    def orOp(self, other):
        return BooleanBox(self.value or other.value)

    def andOp(self, other):
        return BooleanBox(self.value and other.value)

    def __repr__(self):
        return str(self.value)
