from .datatypes.floatingbox import *
from .datatypes.integerbox import *
from .datatypes.booleanbox import *
from .datatypes.stringbox import *
from .datatypes.arraybox import *
from .datatypes.rollbox import *
from .scope import *
from .utils import *

from pypeg2 import *

import re


ValidLabels = re.compile(r'(?!\btrue\b|\bTrue\b|\bfalse\b|\bFalse\b|\bin\b|\bas\b)^\b([a-zA-Z]\w*)\b')


# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------

class TerminalExpression:

    grammar = None

    def __init__(self, exp):
        self.exp = exp

    def generate_tree(self, id_manager):
        self.exp.generate_tree(id_manager)
        self.tree = self.exp.tree

    def evaluate(self, scope, options):
        self.exp.evaluate(scope, options)

        self.stack = self.exp.stack
        self.result = self.exp.result
        self.errors = self.exp.errors

        return self


class Expression:

    grammar = None

    def __init__(self, exp):
        self.exp = exp

    def generate_tree(self, id_manager):
        self.exp.generate_tree(id_manager)
        self.tree = self.exp.tree

    def evaluate(self, scope, options):
        self.exp.evaluate(scope, options)

        self.stack = self.exp.stack
        self.result = self.exp.result
        self.errors = self.exp.errors

        return self

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------

class Label:

    grammar = ValidLabels

    def __init__(self, exp):
        self.exp = exp

    def generate_tree(self, id_manager):
        self.id = id_manager.get_id()
        self.tree = { "type": "label", "id": self.id }

    def evaluate(self, scope, options):

        self.errors = []

        try:
            value = scope.value[self.exp]
            self.result = convertType(value)
        except KeyError:
            desc = "There's no '" + self.exp + "' variable in the scope."
            self.errors  += [{"description": desc, "id": self.id}]
            self.result = None

        self.stack = {}
        self.stack.update({self.id: self.result})

        return self


class String:

    grammar = re.compile(r'\"(\\.|[^\\"])*\"')

    def __init__(self, exp):
        self.exp = exp

    def generate_tree(self, id_manager):
        self.id = id_manager.get_id()
        self.tree = { "type": "string", "id": self.id }

    def evaluate(self, scope, options):

        self.errors = []

        value = self.exp[1:-1]

        try:
            self.result = StringBox(value)

        except Exception:
            desc = "Can't convert '" + self.exp + "' to string."
            self.errors  += [{"description": desc, "id": self.id}]
            self.result = None

        self.stack = {}
        self.stack.update({self.id: self.result})

        return self
        


class Number:

    grammar = re.compile(r'\d+')

    def __init__(self, exp):
        self.exp = exp

    def generate_tree(self, id_manager):
        self.id = id_manager.get_id()
        self.tree = { "type": "integer", "id": self.id }

    def evaluate(self, scope, options):

        self.errors = []

        try:
            self.result = IntegerBox(self.exp)

        except Exception:
            desc = "Can't convert '" + self.exp + "' to integer."
            self.errors += [{"description": desc, "id": self.id }]
            self.result = None

        self.stack = {}
        self.stack.update({self.id: self.result})

        return self


class Boolean:

    grammar = re.compile(r'true|false|True|False')

    def __init__(self, exp):
        self.exp = exp

    def generate_tree(self, id_manager):
        self.id = id_manager.get_id()
        self.tree = { "type": "boolean", "id": self.id }

    def evaluate(self, scope, options):

        self.errors = []

        self.result = BooleanBox(False)
        if self.exp == "true" or self.exp == "True":
            self.result = BooleanBox(True)
        else:
            self.result = BooleanBox(False)

        self.stack = {}
        self.stack.update({self.id: self.result})

        return self


class Decimal:

    grammar = re.compile(r'\d+\.\d+')

    def __init__(self, exp):
        self.exp = exp

    def generate_tree(self, id_manager):
        self.id = id_manager.get_id()
        self.tree = { "type": "decimal", "id": self.id }

    def evaluate(self, scope, options):

        self.errors = []

        try:
            self.result = FloatingBox(self.exp)

        except Exception:
            desc = "Can't convert '" + self.exp + "' to decimal."
            self.errors += [{"description": desc, "id": self.id }]
            self.result = None

        self.stack = {}
        self.stack.update({self.id: self.result})

        return self


class Roll:

    grammar = "<", Number, "d", Number, "|", Number, maybe_some(",", Number), ">"

    def __init__(self, exp):
        self.exp = exp

    def generate_tree(self, id_manager):
        self.id = id_manager.get_id()

        for i in range(0, len(self.exp)):
            self.exp[i].generate_tree(id_manager)

        self.tree = {
            "type": "roll",
            "id": self.id,
            "count": self.exp[0].tree,
            "dice": self.exp[1].tree,
            "rolls": list(elem.tree for elem in self.exp[2:])
        }

    def evaluate(self, scope, options):

        self.errors = []
        self.stack = {}

        for i in range(0, len(self.exp)):
            self.exp[i].evaluate(scope, options)
            self.errors += self.exp[i].errors
            self.stack += self.exp[i].errors

        rolls = list(elem.result for elem in self.exp[2:])
        dice = self.exp[1].result
        rolls = self.exp[0].result

        try:
            self.result = RollBox(rolls, dice, rolls)
        except e:
            self.errors += [{"description": str(e), "id": self.id}]
            self.result = None

        self.stack.update({self.id: self.result})

        return self


class Array:

    grammar = [("[", csl(Expression), "]"), "[]"]

    def __init__(self, exp=None):
        if exp is None:
            exp = []
        self.exp = exp

    def generate_tree(self, id_manager):
        self.id = id_manager.get_id()

        for i in range(0, len(self.exp)):
            self.exp[i].generate_tree(id_manager)

        self.tree = {
            "type": "array",
            "id": self.id,
            "value": list(elem.tree for elem in self.exp)
        }

    def evaluate(self, scope, options):

        self.errors = []
        self.stack = {}

        for i in range(0, len(self.exp)):
            self.exp[i].evaluate(scope, options)
            self.errors += self.exp[i].errors
            self.stack.update(self.exp[i].stack)

        self.result = ArrayBox(list(value.result for value in self.exp))

        self.stack.update({self.id: self.result})

        return self