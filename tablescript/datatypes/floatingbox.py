

class FloatingBox:

    def __init__(self, init=0):

        if type(init) == FloatingBox:
            self.value = init.value

        elif type(init) == str:
            self.value = float(init)

        else:
            self.value = float(init)

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = value

    def __neg__(self):
        return FloatingBox(-self.value)

    def __add__(self, other):
        from .integerbox import IntegerBox
        from .arraybox import ArrayBox
        from .rollbox import RollBox

        if type(other) == IntegerBox:
            return FloatingBox(self.value + other.value)

        if type(other) == RollBox:
            return FloatingBox(self.value + sum(other.value))

        if type(other) == ArrayBox:
            ret = ArrayBox(other.value)
            for i in range(0, len(ret.value)):
                ret.value[i] = ret.value[i] + self
                print(ret.value[i])
            return ret

        if type(other) == FloatingBox:
            return FloatingBox(self.value + other.value)

    def __sub__(self, other):
        from .integerbox import IntegerBox
        from .arraybox import ArrayBox
        from .rollbox import RollBox

        if type(other) == IntegerBox:
            return FloatingBox(self.value - other.value)

        if type(other) == RollBox:
            return FloatingBox(self.value - sum(other.value))

        if type(other) == ArrayBox:
            ret = ArrayBox(other.value)
            for i in range(0, len(ret.value)):
                ret.value[i] = ret.value[i] - self
                print(ret.value[i])
            return ret

        if type(other) == FloatingBox:
            return FloatingBox(self.value - other.value)

    def __mul__(self, other):
        from .integerbox import IntegerBox
        from .arraybox import ArrayBox
        from .rollbox import RollBox

        if type(other) == IntegerBox:
            return FloatingBox(self.value * other.value)

        if type(other) == RollBox:
            return FloatingBox(self.value * sum(other.value))

        if type(other) == ArrayBox:
            ret = ArrayBox(other.value)
            for i in range(0, len(ret.value)):
                ret.value[i] = ret.value[i] * self
                print(ret.value[i])
            return ret

        if type(other) == FloatingBox:
            return FloatingBox(self.value * other.value)

    def __truediv__(self, other):
        from .integerbox import IntegerBox
        from .arraybox import ArrayBox
        from .rollbox import RollBox

        if type(other) == IntegerBox:
            return FloatingBox(self.value / other.value)

        if type(other) == RollBox:
            return FloatingBox(self.value / sum(other.value))

        if type(other) == ArrayBox:
            ret = ArrayBox(other.value)
            for i in range(0, len(ret.value)):
                ret.value[i] = ret.value[i] / self
                print(ret.value[i])
            return ret

        if type(other) == FloatingBox:
            return FloatingBox(self.value / other.value)

    def __floordiv__(self, other):
        from .integerbox import IntegerBox
        from .arraybox import ArrayBox
        from .rollbox import RollBox

        if type(other) == IntegerBox:
            return FloatingBox(self.value // other.value)

        if type(other) == RollBox:
            return FloatingBox(self.value // sum(other.value))

        if type(other) == ArrayBox:
            ret = ArrayBox(other.value)
            for i in range(0, len(ret.value)):
                ret.value[i] = ret.value[i] // self
                print(ret.value[i])
            return ret

        if type(other) == FloatingBox:
            return FloatingBox(self.value // other.value)

    def __repr__(self):
        return str(self.value)
