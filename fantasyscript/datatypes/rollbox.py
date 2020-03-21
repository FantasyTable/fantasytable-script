from numpy import *


class RollBox:

    def __init__(self, *params):

        if len(params) == 1 and type(params[0]) == RollBox:
            self._value = params[0]._value
            self.dice = params[0].dice

        if len(params) >= 2:

            if params[0].value <= 0:
                raise Exception("You must throw at least 1 dice.")

            if params[1].value <= 0:
                raise Exception("A dice can't have 0 or less faces.")

            self.dice = params[1].value

            if len(params) == 3:

                if len(params[2]) != params[0].value:
                    raise Exception("Array size doesn't corresponds to the first parameter.")

                self._value = params[2]

            if len(params) == 2:
                self._value = []

                for i in range(0, params[0].value):
                    self._value.append(random.randint(1, self.dice + 1))

    def toArray(self):
        from .arraybox import ArrayBox
        from .integerbox import IntegerBox

        ret = ArrayBox()

        for i in range(0, len(self._value)):
            ret.append(RollBox(IntegerBox(1), IntegerBox(self.dice), [self._value[i]]))

        return ret

    @property
    def value(self):
        return sum(self._value)

    def __neg__(self):
        return -sum(self._value)

    def __add__(self, other):
        from .floatingbox import FloatingBox
        from .integerbox import IntegerBox
        from .arraybox import ArrayBox

        if type(other) == RollBox:
            return IntegerBox(sum(self._value) + sum(other.value))

        if type(other) == IntegerBox:
            return IntegerBox(sum(self._value) + other.value)

        if type(other) == FloatingBox:
            return FloatingBox(sum(self._value) + other.value)

        if type(other) == ArrayBox:
            return IntegerBox(sum(self._value)) + other

    def __sub__(self, other):
        from .floatingbox import FloatingBox
        from .integerbox import IntegerBox
        from .arraybox import ArrayBox

        if type(other) == RollBox:
            return IntegerBox(sum(self._value) - sum(other.value))

        if type(other) == IntegerBox:
            return IntegerBox(sum(self._value) - other.value)

        if type(other) == FloatingBox:
            return FloatingBox(sum(self._value) - other.value)

        if type(other) == ArrayBox:
            return IntegerBox(sum(self._value)) - other

    def __mul__(self, other):
        from .floatingbox import FloatingBox
        from .integerbox import IntegerBox
        from .arraybox import ArrayBox

        if type(other) == RollBox:
            return IntegerBox(sum(self._value) * sum(other.value))

        if type(other) == IntegerBox:
            return IntegerBox(sum(self._value) * other.value)

        if type(other) == FloatingBox:
            return FloatingBox(sum(self._value) * other.value)

        if type(other) == ArrayBox:
            return IntegerBox(sum(self._value)) * other

    def __truediv__(self, other):
        from .floatingbox import FloatingBox
        from .integerbox import IntegerBox
        from .arraybox import ArrayBox

        if type(other) == RollBox:
            return IntegerBox(sum(self._value) / sum(other.value))

        if type(other) == IntegerBox:
            return IntegerBox(sum(self._value) / other.value)

        if type(other) == FloatingBox:
            return FloatingBox(sum(self._value) / other.value)

        if type(other) == ArrayBox:
            return IntegerBox(sum(self._value)) / other

    def __floordiv__(self, other):
        from .floatingbox import FloatingBox
        from .integerbox import IntegerBox
        from .arraybox import ArrayBox

        if type(other) == RollBox:
            return IntegerBox(sum(self._value) // sum(other.value))

        if type(other) == IntegerBox:
            return IntegerBox(sum(self._value) // other.value)

        if type(other) == FloatingBox:
            return FloatingBox(sum(self._value) // other.value)

        if type(other) == ArrayBox:
            return IntegerBox(sum(self._value)) // other

    def __lt__(self, other):
        from .floatingbox import FloatingBox
        from .booleanbox import BooleanBox
        from .integerbox import IntegerBox
        from .arraybox import ArrayBox
        from .rollbox import RollBox

        if type(other) == RollBox:
            return BooleanBox(sum(self._value) < sum(other.value))

        if type(other) == FloatingBox or type(other) == IntegerBox:
            return BooleanBox(sum(self._value) < other.value)

        if type(other) == ArrayBox:
            ret = ArrayBox()
            for i in range(0, len(self._value)):
                ret.append(other < self._value[i])
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

        nums = str(self._value[0])
        for i in range(1, len(self._value)):
            nums = nums + ", " + str(self._value[i])

        return "<" + str(len(self._value)) + "d" + str(self.dice) + "| " + nums + ">"
