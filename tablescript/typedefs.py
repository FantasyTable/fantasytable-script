from .datatypes.floatingbox import *
from .datatypes.integerbox import *
from .datatypes.arraybox import *
from .datatypes.rollbox import *
from .scope import *

from pypeg2 import *

import re


def convertType(value):

    if type(value) == int:
        return IntegerBox(value)
    elif type(value) == float:
        return FloatingBox(value)
    elif type(value) == list:
        values = []

        for i in range(0, len(value)):
            values.append(convertType(value[i]))

        return ArrayBox

    return Scope(value)

class TerminalExpression:

    grammar = None

    def __init__(self, exp):
        self.exp = exp

    def evaluate(self, scope):
        return self.exp.evaluate(scope)


class Expression:

    grammar = None

    def __init__(self, exp):
        self.exp = exp

    def evaluate(self, scope):
        return self.exp.evaluate(scope)


class Label:

    grammar = re.compile(r'[a-ce-zA-Z]\w*')

    def __init__(self, exp):
        self.exp = exp

    def evaluate(self, scope):

        value = scope.value[self.exp]
        converted = convertType(value)

        return ({ "type": "label", "name": self.exp, "value": value }, converted)


class Number:

    grammar = re.compile(r'\d+')

    def __init__(self, exp):
        self.exp = exp

    def evaluate(self, scope):
        return ({ "type": "number", "value": int(self.exp) }, IntegerBox(self.exp))


class Decimal:

    grammar = re.compile(r'\d+\.\d+')

    def __init__(self, exp):
        self.exp = exp

    def evaluate(self, scope):
        return ({ "type": "decimal", "value": float(self.exp) }, FloatingBox(self.exp))


class Roll:

    grammar = "<", Number, "d", Number, "|", Number, maybe_some(",", Number), ">"

    def __init__(self, exp):
        self.exp = exp

    def evaluate(self, scope):

        rolls = []
        for i in range(2, len(self.exp)):
            rolls.append(self.exp[i].evaluate(scope)[1])

        dice = self.exp[1].evaluate(scope)[1]
        rolls = self.exp[0].evaluate(scope)[1]

        return ({"type": "roll", "dice": dice, "value": rolls }, RollBox(rolls, dice, rolls))


class RollOperator:

    grammar = Number, "d", Number

    def __init__(self, exp):
        self.exp = exp

    def evaluate(self, scope):

        v1 = self.exp[0].evaluate(scope)[1]
        v2 = self.exp[1].evaluate(scope)[1]
        value = RollBox(v1, v2)

        return ({"type": "roll", "dice": v2, "value": value.value }, value)


class ArrayRoll:

    grammar = Number, "[d]", Number

    def __init__(self, exp):
        self.exp = exp

    def evaluate(self, scope):
        v1 = self.exp[0].evaluate(scope)[1]
        v2 = self.exp[1].evaluate(scope)[1]

        value = RollBox(v1, v2).toArray()

        trees = []
        for i in range(0, len(value.value)):
            trees.append({"type": "roll", "dice": v2, "value": value[i].value })

        return ({"type": "array", "content": trees}, value)


class Array:

    grammar = [("[", csl(Expression, separator=","), "]"), "[]"]

    def __init__(self, exp=[]):
        self.exp = exp

    def evaluate(self, scope):

        values = []
        trees = []

        for i in range(0, len(self.exp)):
            data = self.exp[i].evaluate(scope)
            values.append(data[1])
            trees.append(data[0])

        return ({"type": "array", "content": trees}, ArrayBox(values))
