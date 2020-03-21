

class FloatingBox:

    def __init__(self, init):

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
            return ret

        if type(other) == FloatingBox:
            return FloatingBox(self.value // other.value)

    def __lt__(self, other):
        from .integerbox import IntegerBox
        from .booleanbox import BooleanBox
        from .arraybox import ArrayBox
        from .rollbox import RollBox

        if type(other) == IntegerBox or type(other) == FloatingBox:
            return BooleanBox(self.value < other.value)

        if type(other) == RollBox:
            val = sum(other.value)
            return BooleanBox(self.value < val)

        if type(other) == ArrayBox:
            ret = ArrayBox()
            for i in range(0, len(self.value)):
                ret.append(BooleanBox(self.other < self.value[i]))
            return ret

    def __eq__(self, other):
        return (self < other).inv().andOp((other < self).inv())

    def __ne__(self, other):
        return (self < other).orOp(other < self)

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        return (self < other).inv()

    def __le__(self, other):
        return (other < self).inv()

    def __repr__(self):
        return str(self.value)
