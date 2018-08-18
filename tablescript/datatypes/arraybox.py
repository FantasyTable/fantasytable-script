

class ArrayBox:

    def __init__(self, init=[]):

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

    def __add__(self, other):
        from .floatingbox import FloatingBox
        from .integerbox import IntegerBox

        if type(other) == IntegerBox or type(other) == FloatingBox:
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

        if type(other) == IntegerBox or type(other) == FloatingBox:
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

        if type(other) == IntegerBox or type(other) == FloatingBox:
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

        if type(other) == IntegerBox or type(other) == FloatingBox:
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

        if type(other) == IntegerBox or type(other) == FloatingBox:
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

    def __repr__(self):

        return str(self.value)
