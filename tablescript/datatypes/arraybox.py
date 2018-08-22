

class ArrayBox:

    def __init__(self, init=None):

        if init is None:
            init = []
        self.value = init.copy()

    def append(self, value):

        if type(value) == ArrayBox:
            self.value = self.value + value.value
        else:
            self.value.append(value)

    def __get__(self, instance, owner):
        return self.value.copy()

    def __set__(self, instance, value):
        self.value = value.copy()

    def __getitem__(self, key):
        return self.value[key]

    def __delitem__(self, key):
        del self.value[key]

    def __setitem__(self, key, value):
        self.value[key] = value

    def inv(self):
        ret = ArrayBox(self.value)
        for i in range(0, len(ret.value)):
            ret.value[i] = ret.value[i].inv()
        return ret

    def __neg__(self):
        ret = ArrayBox(self.value)
        for i in range(0, len(ret.value)):
            ret.value[i] = -ret.value[i]
        return ret

    def __add__(self, other):
        from .floatingbox import FloatingBox
        from .integerbox import IntegerBox
        from .rollbox import RollBox

        if type(other) == IntegerBox or type(other) == FloatingBox or type(other) == RollBox:
            ret = ArrayBox(self.value)
            for i in range(0, len(ret.value)):
                ret.value[i] = ret.value[i] + other
            return ret

        if type(other) == ArrayBox:
            ret = ArrayBox(self.value)
            for i in range(0, max(len(ret.value), len(other.value))):
                if i >= len(ret.value):
                    ret.append(other[i])
                else:
                    ret[i] = ret[i] + other[i]

            return ret

    def __sub__(self, other):
        from .floatingbox import FloatingBox
        from .integerbox import IntegerBox
        from .rollbox import RollBox

        if type(other) == IntegerBox or type(other) == FloatingBox or type(other) == RollBox:
            ret = ArrayBox(self.value)
            for i in range(0, len(ret.value)):
                ret.value[i] = ret.value[i] - other
            return ret

        if type(other) == ArrayBox:
            ret = ArrayBox(self.value)
            for i in range(0, max(len(ret.value), len(other.value))):

                if i >= len(ret.value):
                    ret.append(-other[i])
                else:
                    ret[i] = ret[i] - other[i]

            return ret

    def __mul__(self, other):
        from .floatingbox import FloatingBox
        from .integerbox import IntegerBox
        from .rollbox import RollBox

        if type(other) == IntegerBox or type(other) == FloatingBox or type(other) == RollBox:
            ret = ArrayBox(self.value)
            for i in range(0, len(ret.value)):
                ret.value[i] = ret.value[i] * other
            return ret

        if type(other) == ArrayBox:
            ret = ArrayBox(self.value)
            for i in range(0, max(len(ret.value), len(other.value))):

                if i >= len(ret.value):
                    ret.append(other[i])
                else:
                    ret[i] = ret[i] * other[i]

            return ret

    def __truediv__(self, other):
        from .floatingbox import FloatingBox
        from .integerbox import IntegerBox
        from .rollbox import RollBox

        if type(other) == IntegerBox or type(other) == FloatingBox or type(other) == RollBox:
            ret = ArrayBox(self.value)
            for i in range(0, len(ret.value)):
                ret.value[i] = ret.value[i] / other
            return ret

        if type(other) == ArrayBox:
            ret = ArrayBox(self.value)
            for i in range(0, max(len(ret.value), len(other.value))):

                if i >= len(ret.value):
                    ret.append(other[i])
                else:
                    ret[i] = ret[i] / other[i]

            return ret

    def __floordiv__(self, other):
        from .floatingbox import FloatingBox
        from .integerbox import IntegerBox
        from .rollbox import RollBox

        if type(other) == IntegerBox or type(other) == FloatingBox or type(other) == RollBox:
            ret = ArrayBox(self.value)
            for i in range(0, len(ret.value)):
                ret.value[i] = ret.value[i] // other
            return ret

        if type(other) == ArrayBox:
            ret = ArrayBox(self.value)
            for i in range(0, max(len(ret.value), len(other.value))):

                if i >= len(ret.value):
                    ret.append(other[i])
                else:
                    ret[i] = ret[i] // other[i]

            return ret

    def compare(self, other, op):
        from .floatingbox import FloatingBox
        from .booleanbox import BooleanBox
        from .integerbox import IntegerBox
        from .rollbox import RollBox

        if type(other) == RollBox \
        or type(other) == FloatingBox \
        or type(other) == IntegerBox \
        or type(other) == BooleanBox:
            ret = ArrayBox()
            for i in range(0, len(self.value)):
                if op == "<":
                    ret.append(self.value[i] < other)
                elif op == ">":
                    ret.append(self.value[i] > other)
                elif op == ">=":
                    ret.append(self.value[i] >= other)
                elif op == "<=":
                    ret.append(self.value[i] <= other)
                elif op == "==":
                    ret.append(self.value[i] == other)
                elif op == "!=":
                    ret.append(self.value[i] != other)
                elif op == "or":
                    ret.append(self.value[i].orOp(other))
                elif op == "and":
                    ret.append(self.value[i].andOp(other))
            return ret

        if type(other) == ArrayBox:
            if len(self.value) != len(other.value):
                raise Exception("This vectors are of different sizes.")
            ret = ArrayBox()
            for i in range(0, len(self.value)):
                if op == "<":
                    ret.append(self.value[i] < other.value[i])
                elif op == ">":
                    ret.append(self.value[i] > other.value[i])
                elif op == ">=":
                    ret.append(self.value[i] >= other.value[i])
                elif op == "<=":
                    ret.append(self.value[i] <= other.value[i])
                elif op == "==":
                    ret.append(self.value[i] == other.value[i])
                elif op == "!=":
                    ret.append(self.value[i] != other.value[i])
                elif op == "or":
                    ret.append(self.value[i].orOp(other.value[i]))
                elif op == "and":
                    ret.append(self.value[i].andOp(other.value[i]))
            return ret

    def __lt__(self, other):
        return self.compare(other, "<")

    def __eq__(self, other):
        return self.compare(other, "==")

    def __ne__(self, other):
        return self.compare(other, "!=")

    def __gt__(self, other):
        return self.compare(other, ">")

    def __ge__(self, other):
        return self.compare(other, ">=")

    def __le__(self, other):
        return self.compare(other, "<=")

    def orOp(self, other):
        return self.compare(other, "or")

    def andOp(self, other):
        return self.compare(other, "and")

    def __repr__(self):

        return str(self.value)
