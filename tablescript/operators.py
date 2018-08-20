from pypeg2 import *

from .scope import *
from .typedefs import *


class MemberAccess:

    grammar = None

    def __init__(self, exp):
        self.exp = exp

    def evaluate(self, scope):

        if len(self.exp) == 1:
            return self.exp[0].evaluate(scope)

        else:
            v0 = self.exp[0].evaluate(scope)

            if type(v0[1]) != Scope:
                raise LookupError("There's no accessible label on the left.")

            v1 = self.exp[1].evaluate(v0[1])

            return {"type": "infix", "op": "access", "left": v0[0], "right": v1[0]}, v1[1]


MemberAccess.grammar = Label, maybe_some(".", MemberAccess)

class Index:

    grammar = TerminalExpression, \
              optional(
                  "[",
                  [
                      (Expression, re.compile(r':'), Expression),
                      (Expression, re.compile(r':')),
                      (re.compile(r':'), Expression),
                      Expression,
                  ] ,"]"
              )

    def __init__(self, exp):
        self.exp = exp

    def evaluate(self, scope):

        if len(self.exp) == 1:
            return self.exp[0].evaluate(scope)

        arr = self.exp[0].evaluate(scope)

        if type(arr[1]) != ArrayBox:
            raise Exception("Expected array as left operand.")

        if len(self.exp) == 2:

            key = self.exp[1].evaluate(scope)
            value = key[1]

            if type(value) == RollBox:
                value = value + IntegerBox(0)

            return { "type": "postfix", "op": "[]", "left": arr[0], "index": key[0] }, arr[1][value.value]

        if len(self.exp) > 2:

            if self.exp[1] == ":":

                end = self.exp[2].evaluate(scope)
                value = end[1]

                if type(value) == RollBox:
                    value = value + IntegerBox(0)

                if type(end[1]) != IntegerBox:
                    raise Exception("The specified index is not an integer.")

                return { "type": "postfix", "op": "[]", "left": arr[0], "endIndex": end[0] }, ArrayBox(arr[1].value[:value.value])

            if self.exp[2] == ":" and len(self.exp) == 3:

                start = self.exp[1].evaluate(scope)
                value = start[1]

                if type(value) == RollBox:
                    value = value + IntegerBox(0)

                if type(start[1]) != IntegerBox:
                    raise Exception("The specified index is not an integer.")

                return { "type": "postfix", "op": "[]", "left": arr[0], "startIndex": start[0] }, ArrayBox(arr[1].value[value.value:])

            start = self.exp[1].evaluate(scope)
            end = self.exp[3].evaluate(scope)
            values = start[1]
            valuee = end[1]

            if type(values) == RollBox:
                values = values + IntegerBox(0)

            if type(valuee) == RollBox:
                valuee = valuee + IntegerBox(0)

            if type(start[1]) != IntegerBox:
                raise Exception("Start index is not an integer.")

            if type(end[1]) != IntegerBox:
                raise Exception("End index is not an integer.")

            return {"type": "postfix", "op": "[]", "left": arr[0], "startIndex": start[0], "endIndex": end[0]}, ArrayBox(arr[1].value[values.value:valuee.value])


class Prefix:

    grammar = maybe_some(re.compile(r'\-|\!')), Index

    def __init__(self, exp):
        self.exp = exp

    def evaluate(self, scope):

        if len(self.exp) == 1:
            return self.exp[0].evaluate(scope)

        else:

            v0 = self.exp[1].evaluate(scope)
            op = self.exp[0]

            tree = {"type": "prefix", "op": op, "right": v0[0]}

            if op == '-':
                return tree, -v0[1]

            elif op == '!':
                return tree, v0[1].inv()


class Merge:

    grammar = Prefix, maybe_some("::", Prefix)

    def __init__(self, exp):
        self.exp = exp

    def evaluate(self, scope):

        if len(self.exp) == 1:
            return self.exp[0].evaluate(scope)

        else:
            acc = ArrayBox()

            v0 = self.exp[0].evaluate(scope)

            acc.append(v0[1])
            tree = v0[0]

            for i in range(1, len(self.exp)):
                v = self.exp[i].evaluate(scope)

                acc.append(v[1])
                tree = {"type": "infix", "op": "::", "left": tree, "right": v[0]}

            return (tree, acc)


class MulDiv:

    grammar = Merge, maybe_some(re.compile(r'\*|\/\/|\/'), Merge)

    def __init__(self, exp):
        self.exp = exp

    def evaluate(self, scope):

        if len(self.exp) == 1:
            return self.exp[0].evaluate(scope)

        else:

            v0 = self.exp[0].evaluate(scope)

            acc = v0[1]
            tree = v0[0]

            for i in range(1, len(self.exp), 2):

                nv = self.exp[i + 1].evaluate(scope)

                if self.exp[i] == '*':
                    acc = acc * nv[1]
                    tree = { "type": "infix", "op": "*", "left": tree, "right": nv[0] }


                elif self.exp[i] == '/':
                    acc = acc / nv[1]
                    tree = {"type": "infix", "op": "/", "left": tree, "right": nv[0]}

                elif self.exp[i] == '//':
                    acc = acc // nv[1]
                    tree = {"type": "infix", "op": "//", "left": tree, "right": nv[0] }

            return (tree, acc)


class SumSub:

    grammar = MulDiv, maybe_some(re.compile(r'[+-]'), MulDiv)

    def __init__(self, exp):
        self.exp = exp

    def evaluate(self, scope):

        if len(self.exp) == 1:
            return self.exp[0].evaluate(scope)

        else:

            v0 = self.exp[0].evaluate(scope)

            acc = v0[1]
            tree = v0[0]

            for i in range(1, len(self.exp), 2):

                nv = self.exp[i + 1].evaluate(scope)

                if self.exp[i] == '+':
                    acc = acc + nv[1]
                    tree = {"type": "infix", "op": "+", "left": tree, "right": nv[0]}

                elif self.exp[i] == '-':
                    acc = acc - nv[1]
                    tree = {"type": "infix", "op": "-", "left": tree, "right": nv[0]}

            return (tree, acc)


class Compare:

    grammar = SumSub, maybe_some(re.compile(r'==|>=|<=|>|<|!='), SumSub)

    def __init__(self, exp):
        self.exp = exp

    def evaluate(self, scope):

        if len(self.exp) == 1:
            return self.exp[0].evaluate(scope)

        else:

            v0 = self.exp[0].evaluate(scope)

            acc = v0[1]
            tree = v0[0]

            for i in range(1, len(self.exp), 2):

                nv = self.exp[i + 1].evaluate(scope)

                tree = {"type": "infix", "op": self.exp[i], "left": tree, "right": nv[0]}

                if self.exp[i] == '==':
                    acc = acc == nv[1]
                elif self.exp[i] == '>=':
                    acc = acc >= nv[1]
                elif self.exp[i] == '<=':
                    acc = acc <= nv[1]
                elif self.exp[i] == '>':
                    acc = acc > nv[1]
                elif self.exp[i] == '<':
                    acc = acc < nv[1]
                elif self.exp[i] == '!=':
                    acc = acc != nv[1]

            return tree, acc


class BoolLogic:

    grammar = Compare, maybe_some(re.compile(r'\|\||&&'), Compare)

    def __init__(self, exp):
        self.exp = exp

    def evaluate(self, scope):

        if len(self.exp) == 1:
            return self.exp[0].evaluate(scope)

        else:

            v0 = self.exp[0].evaluate(scope)

            acc = v0[1]
            tree = v0[0]

            for i in range(1, len(self.exp), 2):

                nv = self.exp[i + 1].evaluate(scope)

                tree = {"type": "infix", "op": self.exp[i], "left": tree, "right": nv[0]}

                if self.exp[i] == '||':
                    acc = acc.orOp(nv[1])
                elif self.exp[i] == '&&':
                    acc = acc.andOp(nv[1])

            return tree, acc


class Parenthesis:

    grammar = "(", BoolLogic, ")"

    def __init__(self, exp):
        self.exp = exp

    def evaluate(self, scope):
        return self.exp.evaluate(scope)



