

class IntegerBox:

    def __init__(self, init=0):

        if type(init) == IntegerBox:
            self.value = init.value

        elif type(init) == str:
            self.value = int(init)

        else:
            self.value = int(init)

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = value

    def __neg__(self):
        return IntegerBox(-self.value)

    def __add__(self, other):
        from .floatingbox import FloatingBox
        from .arraybox import ArrayBox
        from .rollbox import RollBox

        if type(other) == FloatingBox:
            return FloatingBox(self.value + other.value)

        if type(other) == RollBox:
            return IntegerBox(self.value + sum(other.value))

        if type(other) == ArrayBox:
            ret = ArrayBox(other.value)
            for i in range(0, len(ret.value)):
                ret.value[i] = ret.value[i] + self
                print(ret.value[i])
            return ret

        if type(other) == IntegerBox:
            return IntegerBox(self.value + other.value)

        if not other:
            return IntegerBox(self.value)

    def __sub__(self, other):
        from .floatingbox import FloatingBox
        from .arraybox import ArrayBox
        from .rollbox import RollBox

        if type(other) == FloatingBox:
            return FloatingBox(self.value - other.value)

        if type(other) == RollBox:
            return IntegerBox(self.value - sum(other.value))

        if type(other) == ArrayBox:
            ret = ArrayBox(other.value)
            for i in range(0, len(ret.value)):
                ret.value[i] = ret.value[i] - self
                print(ret.value[i])
            return ret

        if type(other) == IntegerBox:
            return IntegerBox(self.value - other.value)

        if not other:
            return IntegerBox(self.value)

    def __mul__(self, other):
        from .floatingbox import FloatingBox
        from .arraybox import ArrayBox
        from .rollbox import RollBox

        if type(other) == FloatingBox:
            return FloatingBox(self.value * other.value)

        if type(other) == RollBox:
            return IntegerBox(self.value * sum(other.value))

        if type(other) == ArrayBox:
            ret = ArrayBox(other.value)
            for i in range(0, len(ret.value)):
                ret.value[i] = ret.value[i] * self
                print(ret.value[i])
            return ret

        if type(other) == IntegerBox:
            return IntegerBox(self.value * other.value)

        if not other:
            return IntegerBox(0)

    def __truediv__(self, other):
        from .floatingbox import FloatingBox
        from .arraybox import ArrayBox
        from .rollbox import RollBox

        if type(other) == FloatingBox:
            return FloatingBox(self.value / other.value)

        if type(other) == RollBox:
            return IntegerBox(self.value / sum(other.value))

        if type(other) == ArrayBox:
            ret = ArrayBox(other.value)
            for i in range(0, len(ret.value)):
                ret.value[i] = ret.value[i] / self
                print(ret.value[i])
            return ret

        if type(other) == IntegerBox:
            return FloatingBox(self.value / other.value)

    def __floordiv__(self, other):
        from .floatingbox import FloatingBox
        from .arraybox import ArrayBox
        from .rollbox import RollBox

        if type(other) == FloatingBox:
            return FloatingBox(self.value // other.value)

        if type(other) == RollBox:
            return IntegerBox(self.value // sum(other.value))

        if type(other) == ArrayBox:
            ret = ArrayBox(other.value)
            for i in range(0, len(ret.value)):
                ret.value[i] = ret.value[i] // self
                print(ret.value[i])
            return ret

        if type(other) == IntegerBox:
            return IntegerBox(self.value // other.value)

    def __lt__(self, other):
        from .floatingbox import FloatingBox
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

        if not other:
            return BooleanBox(self.value < 0)

    def __eq__(self, other):
        return (self < other).inv().andOp((other < self).inv())

    def __ne__(self, other):
        return (self < other).orOp(other < self)

    def __gt__(self, other):
        from .booleanbox import BooleanBox

        return BooleanBox(other < self.value)

    def __ge__(self, other):
        return (self < other).inv()

    def __le__(self, other):
        return (other < self).inv()

    def __repr__(self):
        return str(self.value)
