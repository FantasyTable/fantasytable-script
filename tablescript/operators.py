from pypeg2 import *

from .scope import *
from .typedefs import *

def passTroughCalc(obj, scope, options):

    if type(obj.exp) == list and len(obj.exp) == 1:
        obj.exp = obj.exp[0]

    if type(obj.exp) != list:
        obj.exp.evaluate(scope, options)
        obj.result = obj.exp.result
        obj.errors = obj.exp.errors
        obj.stack = obj.exp.stack
        return True

    return False


def passTroughTree(obj, id_manager):

    if type(obj.exp) == list and len(obj.exp) == 1:
        obj.exp = obj.exp[0]

    if type(obj.exp) != list:
        obj.exp.generate_tree(id_manager)
        obj.tree = obj.exp.tree
        return True

    return False


class Parenthesis:

    grammar = "(", Expression, ")"

    def __init__(self, exp):
        self.exp = exp

    def generate_tree(self, id_manager):
        self.id = id_manager.get_id()
        self.exp.generate_tree(id_manager)
        self.tree = {
            "type": "parenthesis",
            "id": self.id,
            "content": self.exp.tree,
        }

    def evaluate(self, scope, options):
        self.exp.evaluate(scope, options)

        self.result = self.exp.result
        self.errors = self.exp.errors
        self.stack = {}
        self.stack.update({self.id: self.result})

        return self


class MemberAccess:

    grammar = None

    def __init__(self, exp):
        self.exp = exp

    def generate_tree(self, id_manager):

        if passTroughTree(self, id_manager):
            return

        self.id = id_manager.get_id()

        for i in range(0, len(self.exp)):
            self.exp[i].generate_tree(id_manager)

        self.tree = { "type": "infix", "op": ".", "id": self.id, "left": self.exp[0].tree, "right": self.exp[1].tree }


    def evaluate(self, scope, options):

        if passTroughCalc(self, scope, options):
            return self
        else:
            self.errors = []
            self.stack = {}

            self.exp[0].evaluate(scope, options)
            self.errors += self.exp[0].errors
            self.stack.update(self.exp[0].stack)

            if len(self.errors) > 0:
                self.result = None
                return self

            if type(self.exp[0].result) != Scope:
                self.errors += [{ "description": "There's no accessible label on the left.", "id": self.id }]
                self.result = None
                return self

            self.exp[1].evaluate(self.exp[0].result, options)
            self.errors += self.exp[1].errors
            self.stack.update(self.exp[1].stack)

            if len(self.errors) > 0:
                self.result = None
                return self

            self.result = self.exp[1].result

            self.stack.update({self.id: self.result})

            return self


MemberAccess.grammar = contiguous(Label, optional(".", [MemberAccess, Label]))


class Index:

    grammar = TerminalExpression, \
              maybe_some(
                  re.compile(r"\["),
                  [
                      (Expression, re.compile(r':'), Expression),
                      (Expression, re.compile(r':')),
                      (re.compile(r':|\?'), Expression),
                      Expression,
                  ], re.compile(r"\]")
              )

    def __init__(self, exp):
        self.exp = exp

    def generate_tree(self, id_manager):

        if passTroughTree(self, id_manager):
            return

        self.id = id_manager.get_id()

        self.exp[0].generate_tree(id_manager)
        self.tree = self.exp[0].tree

        i = 1
        self.indexes = []
        for i in range(1, len(self.exp)):
            if self.exp[i] == "[":
                self.indexes.append([])
            elif self.exp[i] == "]":
                continue
            else:
                self.indexes[-1].append(self.exp[i])

        for i in range(0, len(self.indexes)):

            curr_index = self.indexes[i]

            if len(curr_index) == 3 and curr_index[1] == ":":
                curr_index[0].generate_tree(id_manager)
                curr_index[2].generate_tree(id_manager)
                self.tree = {
                    "type": "postfix",
                    "op": "[n:n]",
                    "id": self.id,
                    "left": self.tree,
                    "start": curr_index[0].tree,
                    "end": curr_index[2].tree
                }

            elif len(curr_index) == 2 and curr_index[1] == ":":
                curr_index[0].generate_tree(id_manager)
                self.tree = {
                    "type": "postfix",
                    "op": "[n:]",
                    "id": self.id,
                    "left": self.tree,
                    "start": curr_index[0].tree,
                }

            elif len(curr_index) == 2 and curr_index[0] == ":":
                curr_index[1].generate_tree(id_manager)
                self.tree = {
                    "type": "postfix",
                    "op": "[:n]",
                    "id": self.id,
                    "left": self.tree,
                    "end": curr_index[1].tree,
                }

            elif len(curr_index) == 2 and curr_index[0] == "?":
                curr_index[1].generate_tree(id_manager)
                self.tree = {
                    "type": "postfix",
                    "op": "[?n]",
                    "id": self.id,
                    "left": self.tree,
                    "cond": curr_index[1].tree,
                }

            elif len(curr_index) == 1:
                curr_index[0].generate_tree(id_manager)
                self.tree = {
                    "type": "postfix",
                    "op": "[n]",
                    "id": self.id,
                    "left": self.tree,
                    "key": curr_index[0].tree,
                }

    def evaluate(self, scope, options):

        if passTroughCalc(self, scope, options):
            return self

        self.errors = []
        self.stack = {}

        self.exp[0].evaluate(scope, options)
        self.errors += self.exp[0].errors
        self.stack.update(self.exp[0].stack)

        if len(self.errors) > 0:
            self.result = None
            return self

        self.result = self.exp[0].result

        if type(self.result) != ArrayBox:
            self.errors += [{ "description": "Expected array as left operand.", "id": self.id }]
            self.result = None
            return self

        for i in range(0, len(self.indexes)):

            curr_index = self.indexes[i]

            if len(curr_index) == 1:

                curr_index[0].evaluate(scope, options)
                self.errors += curr_index[0].errors
                self.stack.update(curr_index[0].stack)

                if len(self.errors) > 0:
                    self.result = None
                    return self

                value = curr_index[0].result

                if type(value) == RollBox:
                    value = value + IntegerBox(0)

                if type(value) != IntegerBox:
                    self.errors += [{"description": "Expected an integer result as key.", "id": self.id}]
                    self.result = None
                    return self

                self.result = self.result[value.value]
                self.stack.update({self.id: self.result})

                continue

            if len(curr_index) == 2 and curr_index[0] == "?":

                options["cacheRolls"] = True
                res = []

                for i in range(0, len(self.result.value)):
                    arrayScope = Scope({"value": self.result.value[i], "key": i}).merge(scope)

                    curr_index[1].evaluate(arrayScope, options)
                    self.errors += curr_index[1].errors
                    self.stack.update(curr_index[1].stack)

                    if len(self.errors) > 0:
                        self.result = None
                        return self

                    value = curr_index[1].result

                    if type(value) != BooleanBox:
                        self.errors += [{"description": "Expected a boolean result as condition.", "id": self.id}]
                        self.result = None
                        return self

                    if value.value:
                        res.append(self.result[i])

                self.result = ArrayBox(res)
                self.stack.update({self.id: self.result})

                continue

            if len(curr_index) == 2 and (curr_index[0] == ":" or curr_index[1] == ":"):

                index = 1 if curr_index[0] == ":" else 0

                curr_index[index].evaluate(scope, options)
                self.errors += curr_index[index].errors
                self.stack += curr_index[index].stack

                if len(self.errors) > 0:
                    self.result = None
                    return self

                value = curr_index[index].result

                if type(value) == RollBox:
                    value = value + IntegerBox(0)

                if type(value) != IntegerBox:
                    self.errors += [{"description": "Expected an integer range.", "id": self.id}]
                    self.result = None
                    return self

                self.result = ArrayBox(self.result[:-value.value]) if curr_index[1] == ":" else ArrayBox(self.result[value.value:])
                self.stack.update({self.id: self.result})

                continue

            curr_index[0].evaluate(scope, options)
            self.errors += curr_index[0].errors
            self.stack += curr_index[0].stack

            curr_index[2].evaluate(scope, options)
            self.errors += curr_index[2].errors
            self.stack.update(curr_index[2].stack)

            if len(self.errors) > 0:
                self.result = None
                return self

            start = curr_index[0].result
            end = curr_index[2].result

            if type(start) == RollBox:
                start = start + IntegerBox(0)

            if type(end) == RollBox:
                end = end + IntegerBox(0)

            if type(start) != IntegerBox:
                raise Exception("Start index is not an integer.")

            if type(end) != IntegerBox:
                raise Exception("End index is not an integer.")

            self.result = ArrayBox(self.result[start.value:end.value])
            self.stack.update({self.id: self.result})

        return self


class Prefix:

    grammar = maybe_some(re.compile(r'[-!]')), Index

    def __init__(self, exp):
        self.exp = exp

    def generate_tree(self, id_manager):

        if passTroughTree(self, id_manager):
            return

        self.id = []

        self.exp[-1].generate_tree(id_manager)
        self.tree = self.exp[-1].tree

        for i in range(2, len(self.exp) + 1):
            self.id.append(id_manager.get_id())
            self.tree = {
                "type": "prefix",
                "op": self.exp[-i],
                "id": self.id[-1],
                "right": self.tree
            }

    def evaluate(self, scope, options):

        if passTroughCalc(self, scope, options):
            return self

        self.exp[-1].evaluate(scope, options)
        self.stack = self.exp[-1].stack
        self.errors = self.exp[-1].errors
        self.result = self.exp[-1].result

        id = 1

        for i in range(2, len(self.exp) + 1):

            op = self.exp[-i]

            if op == '-':
                self.result = -self.result

            elif op == '!':
                self.result = self.result.inv()

            self.stack.update({self.id[-id]: self.result})
            id = id + 1

        return self


class RollOperator:

    grammar = [([Number, Parenthesis], "d", [Number, Parenthesis]), Prefix]

    def __init__(self, exp):
        self.exp = exp
        self.result = None

    def generate_tree(self, id_manager):

        if passTroughTree(self, id_manager):
            return

        self.id = id_manager.get_id()

        self.exp[0].generate_tree(id_manager)
        self.exp[1].generate_tree(id_manager)

        self.tree = {
            "type": "infix",
            "op": "d",
            "id": self.id,
            "left": self.exp[0].tree,
            "right": self.exp[1].tree
        }

    def evaluate(self, scope, options):

        if passTroughCalc(self, scope, options):
            return self

        self.errors = []
        self.stack = {}

        self.exp[0].evaluate(scope, options)
        self.errors += self.exp[0].errors
        self.stack.update(self.exp[0].stack)

        if len(self.errors) > 0:
            self.result = None
            return self

        count = self.exp[0].result

        if type(count) == RollBox:
            count = count + IntegerBox(0)

        if type(count) != IntegerBox:
            self.errors += [{"description": "Left roll operand must be an integer.", "id": self.id}]
            self.result = None
            return self

        self.exp[1].evaluate(scope, options)
        self.errors += self.exp[1].errors
        self.stack.update(self.exp[1].stack)

        if len(self.errors) > 0:
            self.result = None
            return self

        dice = self.exp[1].result

        if type(dice) == RollBox:
            dice = dice + IntegerBox(0)

        if type(dice) != IntegerBox:
            self.errors += [{"description": "Right roll operand must be an integer.", "id": self.id}]
            self.result = None
            return self

        if not (options["cacheRolls"] and type(self.result) == RollBox):
            self.result = RollBox(count, dice)

        self.stack.update({self.id: self.result})

        return self


class ArrayRoll:

    grammar = [([Number, Parenthesis], "[d]", [Number, Parenthesis]), RollOperator]

    def __init__(self, exp):
        self.exp = exp
        self.result = None

    def generate_tree(self, id_manager):

        if passTroughTree(self, id_manager):
            return

        self.id = id_manager.get_id()

        self.exp[0].generate_tree(id_manager)
        self.exp[1].generate_tree(id_manager)

        self.tree = {
            "type": "infix",
            "op": "[d]",
            "id": self.id,
            "left": self.exp[0].tree,
            "right": self.exp[1].tree
        }

    def evaluate(self, scope, options):

        if passTroughCalc(self, scope, options):
            return self

        self.errors = []
        self.stack = {}

        self.exp[0].evaluate(scope, options)
        self.errors += self.exp[0].errors
        self.stack.update(self.exp[0].stack)

        if len(self.errors) > 0:
            self.result = None
            return self

        count = self.exp[0].result

        if type(count) == RollBox:
            count = count + IntegerBox(0)

        if type(count) != IntegerBox:
            self.errors += [{"description": "Left roll operand must be an integer.", "id": self.id}]
            self.result = None
            return self

        self.exp[1].evaluate(scope, options)
        self.errors += self.exp[1].errors
        self.stack.update(self.exp[1].stack)

        if len(self.errors) > 0:
            self.result = None
            return self

        dice = self.exp[1].result

        if type(dice) == RollBox:
            dice = dice + IntegerBox(0)

        if type(dice) != IntegerBox:
            self.errors += [{"description": "Right roll operand must be an integer.", "id": self.id}]
            self.result = None
            return self

        self.result = RollBox(count, dice).toArray()
        self.stack.update({self.id: self.result})

        return self


class Merge:

    grammar = ArrayRoll, maybe_some("::", ArrayRoll)

    def __init__(self, exp):
        self.exp = exp

    def generate_tree(self, id_manager):

        if passTroughTree(self, id_manager):
            return

        self.id = []

        self.exp[0].generate_tree(id_manager)
        self.tree = self.exp[0].tree

        for i in range(1, len(self.exp)):
            self.id.append(id_manager.get_id())
            self.exp[i].generate_tree(id_manager)
            self.tree = {
                "type": "infix",
                "op": "::",
                "id": self.id[-1],
                "left": self.tree,
                "right": self.exp[i].tree
            }

    def evaluate(self, scope, options):

        if passTroughCalc(self, scope, options):
            return self

        self.result = ArrayBox()

        self.errors = []
        self.stack = {}

        self.exp[0].evaluate(scope, options)
        self.errors += self.exp[0].errors
        self.stack.update(self.exp[0].stack)

        if len(self.errors) > 0:
            self.result = None
            return self

        self.result.append(self.exp[0].result)

        for i in range(1, len(self.exp)):

            self.exp[i].evaluate(scope, options)
            self.errors += self.exp[i].errors
            self.stack.update(self.exp[i].stack)

            if len(self.errors) > 0:
                self.result = None
                return self

            self.result.append(self.exp[i].result)

            self.stack.update({self.id: self.result})

        return self

class MulDiv:

    grammar = Merge, maybe_some(re.compile(r'\*|//|/'), Merge)

    def __init__(self, exp):
        self.exp = exp

    def generate_tree(self, id_manager):

        if passTroughTree(self, id_manager):
            return

        self.id = []

        self.exp[0].generate_tree(id_manager)
        self.tree = self.exp[0].tree

        for i in range(1, len(self.exp), 2):
            self.id.append(id_manager.get_id())
            self.exp[i + 1].generate_tree(id_manager)
            self.tree = {
                "type": "infix",
                "op": self.exp[i],
                "id": self.id[-1],
                "left": self.tree,
                "right": self.exp[i + 1].tree
            }

    def evaluate(self, scope, options):

        if passTroughCalc(self, scope, options):
            return self

        self.errors = []
        self.stack = {}

        self.exp[0].evaluate(scope, options)
        self.errors += self.exp[0].errors
        self.stack.update(self.exp[0].stack)

        if len(self.errors) > 0:
            self.result = None
            return self

        self.result = self.exp[0].result

        for i in range(1, len(self.exp), 2):

            self.exp[i + 1].evaluate(scope, options)
            self.errors += self.exp[i + 1].errors
            self.stack.update(self.exp[i + 1].stack)

            if len(self.errors) > 0:
                self.result = None
                return self

            if self.exp[i] == '*':
                self.result = self.result * self.exp[i + 1].result

            elif self.exp[i] == '/':
                self.result = self.result / self.exp[i + 1].result

            elif self.exp[i] == '//':
                self.result = self.result // self.exp[i + 1].result

            self.stack.update({self.id[i // 2]: self.result})

        return self

    def evaluate(self, scope, options):

        if passTroughCalc(self, scope, options):
            return self

        self.errors = []
        self.stack = {}

        self.exp[0].evaluate(scope, options)
        self.errors += self.exp[0].errors
        self.stack.update(self.exp[0].stack)

        if len(self.errors) > 0:
            self.result = None
            return self

        self.exp[2].evaluate(scope, options)
        self.errors += self.exp[2].errors
        self.stack += self.exp[2].stack

        if len(self.errors) > 0:
            self.result = None
            return self

        if self.exp[1] == '*':
            self.result = self.exp[0].result * self.exp[2].result

        elif self.exp[1] == '/':
            self.result = self.exp[0].result / self.exp[2].result

        elif self.exp[1] == '//':
            self.result = self.exp[0].result // self.exp[2].result

        self.stack.update({self.id: self.result})

        return self


class SumSub:

    grammar = MulDiv, maybe_some(re.compile(r'[+-]'), MulDiv)

    def __init__(self, exp):
        self.exp = exp

    def generate_tree(self, id_manager):

        if passTroughTree(self, id_manager):
            return

        self.id = []

        self.exp[0].generate_tree(id_manager)
        self.tree = self.exp[0].tree

        for i in range(1, len(self.exp), 2):
            self.id.append(id_manager.get_id())
            self.exp[i + 1].generate_tree(id_manager)
            self.tree = {
                "type": "infix",
                "op": self.exp[i],
                "id": self.id[-1],
                "left": self.tree,
                "right": self.exp[i + 1].tree
            }

    def evaluate(self, scope, options):

        if passTroughCalc(self, scope, options):
            return self

        self.errors = []
        self.stack = {}

        self.exp[0].evaluate(scope, options)
        self.errors += self.exp[0].errors
        self.stack.update(self.exp[0].stack)

        if len(self.errors) > 0:
            self.result = None
            return self

        self.result = self.exp[0].result

        for i in range(1, len(self.exp), 2):

            self.exp[i + 1].evaluate(scope, options)
            self.errors += self.exp[i + 1].errors
            self.stack.update(self.exp[i + 1].stack)

            if len(self.errors) > 0:
                self.result = None
                return self

            if self.exp[i] == '+':
                self.result = self.result + self.exp[i + 1].result

            elif self.exp[i] == '-':
                self.result = self.result - self.exp[i + 1].result

            self.stack.update({self.id[i // 2]: self.result})

        return self


class Compare:

    grammar = SumSub, maybe_some(re.compile(r'==|>=|<=|>|<|!='), SumSub)

    def __init__(self, exp):
        self.exp = exp

    def generate_tree(self, id_manager):

        if passTroughTree(self, id_manager):
            return

        self.id = []

        self.exp[0].generate_tree(id_manager)
        self.tree = self.exp[0].tree

        for i in range(1, len(self.exp), 2):
            self.id.append(id_manager.get_id())
            self.exp[i + 1].generate_tree(id_manager)
            self.tree = {
                "type": "infix",
                "op": self.exp[i],
                "id": self.id[-1],
                "left": self.tree,
                "right": self.exp[i + 1].tree
            }

    def evaluate(self, scope, options):

        if passTroughCalc(self, scope, options):
            return self

        self.errors = []
        self.stack = {}

        self.exp[0].evaluate(scope, options)
        self.errors += self.exp[0].errors
        self.stack.update(self.exp[0].stack)

        if len(self.errors) > 0:
            self.result = None
            return self

        self.result = self.exp[0].result

        for i in range(1, len(self.exp), 2):

            self.exp[i + 1].evaluate(scope, options)
            self.errors += self.exp[i + 1].errors
            self.stack.update(self.exp[i + 1].stack)

            if len(self.errors) > 0:
                self.result = None
                return self

            if self.exp[i] == '==':
                self.result = self.result == self.exp[i + 1].result
            elif self.exp[i] == '>=':
                self.result = self.result >= self.exp[i + 1].result
            elif self.exp[i] == '<=':
                self.result = self.result <= self.exp[i + 1].result
            elif self.exp[i] == '>':
                self.result = self.result > self.exp[i + 1].result
            elif self.exp[i] == '<':
                self.result = self.result < self.exp[i + 1].result
            elif self.exp[i] == '!=':
                self.result = self.result != self.exp[i + 1].result

            self.stack.update({self.id[i // 2]: self.result})

        return self


class BoolLogic:

    grammar = Compare, maybe_some(re.compile(r'\|\||&&'), Compare)

    def __init__(self, exp):
        self.exp = exp

    def generate_tree(self, id_manager):

        if passTroughTree(self, id_manager):
            return

        self.id = []

        self.exp[0].generate_tree(id_manager)
        self.tree = self.exp[0].tree

        for i in range(1, len(self.exp), 2):
            self.id.append(id_manager.get_id())
            self.exp[i + 1].generate_tree(id_manager)
            self.tree = {
                "type": "infix",
                "op": self.exp[i],
                "id": self.id[-1],
                "left": self.tree,
                "right": self.exp[i + 1].tree
            }

    def evaluate(self, scope, options):

        if passTroughCalc(self, scope, options):
            return self

        self.errors = []
        self.stack = {}

        self.exp[0].evaluate(scope, options)
        self.errors += self.exp[0].errors
        self.stack.update(self.exp[0].stack)

        if len(self.errors) > 0:
            self.result = None
            return self

        self.result = self.exp[0].result

        for i in range(1, len(self.exp), 2):

            self.exp[i + 1].evaluate(scope, options)
            self.errors += self.exp[i + 1].errors
            self.stack.update(self.exp[i + 1].stack)

            if len(self.errors) > 0:
                self.result = None
                return self

            if self.exp[i] == '||':
                self.result = self.result.orOp(self.exp[i + 1].result)
            elif self.exp[i] == '&&':
                self.result = self.result.andOp(self.exp[i + 1].result)

            self.stack.update({self.id[i // 2]: self.result})

        return self


class Naming:

    grammar = separated(BoolLogic, optional(Keyword("as"), ValidLabels))

    def __init__(self, exp):
        self.exp = exp

    def generate_tree(self, id_manager):

        if passTroughTree(self, id_manager):
            return

        self.id = id_manager.get_id()

        self.exp[0].generate_tree(id_manager)

        self.tree = {
            "type": "infix",
            "op": "as",
            "id": self.id,
            "left": self.exp[0].tree,
            "right": self.exp[1]
        }

    def evaluate(self, scope, options):

        if passTroughCalc(self, scope, options):
            return self

        self.errors = []
        self.stack = {}

        self.exp[0].evaluate(scope, options)
        self.errors += self.exp[0].errors
        self.stack.update(self.exp[0].stack)

        if len(self.errors) > 0:
            self.result = None
            return self

        self.result = Scope({self.exp[1]:self.exp[0].result})
        self.stack.update({self.id: self.result})

        return self


class ScopeMerge:

    grammar = [(maybe_some(Naming, Keyword("in")), Naming), BoolLogic]

    def __init__(self, exp):
        self.exp = exp

    def generate_tree(self, id_manager):

        if passTroughTree(self, id_manager):
            return

        self.id = []

        self.exp[0].generate_tree(id_manager)
        self.tree = self.exp[0].tree

        for i in range(1, len(self.exp) - 1):
            self.id.append(id_manager.get_id())
            self.exp[i].generate_tree(id_manager)
            self.tree = {
                "type": "infix",
                "op": "in",
                "id": self.id[-1],
                "left": self.tree,
                "right": self.exp[i].tree
            }

    def evaluate(self, scope, options):

        if passTroughCalc(self, scope, options):
            return self

        self.errors = []
        self.stack = {}

        for i in range(0, len(self.exp) - 1):

            self.exp[i].evaluate(scope, options)
            self.errors += self.exp[i].errors
            self.stack.update(self.exp[i].stack)

            if len(self.errors) > 0:
                self.result = None
                return self

            if type(self.exp[i].retult) != Scope:
                raise Exception("Cannot use an expression as scope.")

            scope = scope.merge(self.exp[i].retult)
            self.stack += [{"value": self.result, "id": self.id[i]}]

        self.exp[-1].evaluate(scope, options)
        self.errors += self.exp[-1].errors
        self.stack += self.exp[-1].stack

        if len(self.errors) > 0:
            self.result = None
            return self

        self.result = self.exp[-1].result
        self.stack.update({self.id[-1]: self.result})

        return self