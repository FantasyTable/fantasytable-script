from .datatypes.floatingbox import *
from .datatypes.integerbox import *
from .datatypes.booleanbox import *
from .datatypes.stringbox import *
from .datatypes.arraybox import *
from .datatypes.rollbox import *
from .scope import *

from pypeg2 import *

import re


validLabels = re.compile(r'(?!\btrue\b|\bTrue\b|\bfalse\b|\bFalse\b|\bin\b|\bas\b)^\b([a-zA-Z]\w*)\b')

def convertType(value):

    """ Convert a standard python type to a boxed type.

    :param value: Original value.
    :return: Boxed value.
    """

    if type(value) == int:
        return IntegerBox(value)

    elif type(value) == float:
        return FloatingBox(value)

    elif type(value) == list:
        values = []
        for i in range(0, len(value)):
            values.append(convertType(value[i]))
        return ArrayBox

    if type(value) == dict:
        return Scope(value)

    return value

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------

class Label:

    grammar = validLabels

    def __init__(self, exp):
        self.exp = exp

    def evaluate(self, scope):

        try:
            value = scope.value[self.exp]
            converted = convertType(value)

            return { "type": "label", "name": self.exp, "value": value }, converted

        except Exception:
            raise LookupError("Identifier not found for: " + self.exp)


class String:

    grammar = re.compile(r'\"(\\.|[^\\"])*\"')

    def __init__(self, exp):
        self.exp = exp

    def evaluate(self, scope):
        value = self.exp[1:-1]
        return { "type": "label", "value": value }, StringBox(value)
        


class Number:

    grammar = re.compile(r'\d+')

    def __init__(self, exp):
        self.exp = exp

    def evaluate(self, scope):
        return { "type": "number", "value": int(self.exp) }, IntegerBox(self.exp)


class Boolean:

    grammar = re.compile(r'true|false|True|False')

    def __init__(self, exp):
        self.exp = exp

    def evaluate(self, scope):
        value = False
        if self.exp == "true" or self.exp == "True":
            value = True
        else:
            value = False

        return {"type": "boolean", "value": value}, BooleanBox(value)


class Decimal:

    grammar = re.compile(r'\d+\.\d+')

    def __init__(self, exp):
        self.exp = exp

    def evaluate(self, scope):
        return { "type": "decimal", "value": float(self.exp) }, FloatingBox(self.exp)


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

        return {"type": "roll", "dice": dice, "value": rolls }, RollBox(rolls, dice, rolls)


class Array:

    grammar = [("[", csl(Expression), "]"), "[]"]

    def __init__(self, exp=None):
        if exp is None:
            exp = []
        self.exp = exp

    def evaluate(self, scope):

        values = []
        trees = []

        for i in range(0, len(self.exp)):
            data = self.exp[i].evaluate(scope)
            values.append(data[1])
            trees.append(data[0])

        return {"type": "array", "content": trees}, ArrayBox(values)
