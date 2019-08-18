from ..datatypes.integerbox import IntegerBox
from ..datatypes.booleanbox import BooleanBox
from ..datatypes.arraybox import ArrayBox
from ..datatypes.rollbox import RollBox
from ..datatypes.scope import Scope
from . import *


class Index:

    def __init__(self, exp):

        # - Set expression
        self.exp = exp

        # - Scatter indices
        self.indexes = []
        if type(exp) is list and len(exp) > 1:
            for exp in self.exp[1:]:
                if exp == "[":
                    self.indexes.append([])
                elif exp == "]":
                    continue
                else:
                    self.indexes[-1].append(exp)

            # - Parse types
            for i, index in enumerate(self.indexes):

                if len(index) == 3 and index[1] == ":":
                    self.indexes[i] = {"op": "[n:n]", "start": index[0], "end": index[2]}
                if len(index) == 2 and index[1] == ":":
                    self.indexes[i] = {"op": "[n:]", "start": index[0]}
                if len(index) == 2 and index[0] == ":":
                    self.indexes[i] = {"op": "[:n]", "end": index[1]}
                if len(index) == 1:
                    self.indexes[i] = {"op": "[n]", "key": index[0]}

        # - Left value
        self.target_exp = self.exp[0]

        # - Initialize values
        self.id = 0
        self.tree = {}
        self.errors = []
        self.stack = {}
        self.refs = []
        self.result = None

    def generate_tree(self, id_manager):

        if pass_trough_tree(self, id_manager):
            return

        # - Set id for this expression
        self.id = id_manager.get_id()

        # - Generate tree for the source array and merge
        self.target_exp.generate_tree(id_manager)
        self.tree = self.target_exp.tree

        for index in self.indexes:

            self.tree = \
            {
                "type": "postfix",
                "op": index["op"],
                "id": self.id,
                "left": self.tree,
            }

            if index["op"] == "[n:n]":
                index["start"].generate_tree(id_manager)
                index["end"].generate_tree(id_manager)
                self.tree["start"] = index["start"].tree
                self.tree["end"] = index["end"].tree

            elif index["op"] == "[n:]":
                index["start"].generate_tree(id_manager)
                self.tree["start"] = index["start"].tree

            elif index["op"] == "[:n]":
                index["end"].generate_tree(id_manager)
                self.tree["end"] = index["end"].tree

            elif index["op"] == "[n]":
                index["key"].generate_tree(id_manager)
                self.tree["key"] = index["key"].tree

    def evaluate(self, scope, options):

        if pass_trough_calc(self, scope, options):
            return

        # - Evaluate array base and merge
        self.target_exp.evaluate(scope, options)
        self.errors += self.target_exp.errors
        self.stack.update(self.target_exp.stack)

        # - Set first result value
        self.result = self.target_exp.result

        # - Check the array type
        if type(self.result) != ArrayBox:
            self.errors += [{"description": "Expected array as left operand.", "id": self.id}]
            self.result = None

        # - Check if errors and abort eventually
        if len(self.errors) > 0:
            self.result = None
            return

        for index in self.indexes:

            if index["op"] == "[n:n]":

                index["start"].evaluate(scope, options)
                self.errors += index["start"].errors
                self.stack.update(index["start"].stack)

                index["end"].evaluate(scope, options)
                self.errors += index["end"].errors
                self.stack.update(index["end"].stack)

                # - Index value
                start = index["start"].result
                end = index["end"].result

                # - Try to convert to integer
                if type(start) == RollBox:
                    start = start + IntegerBox(0)
                if type(end) == RollBox:
                    end = end + IntegerBox(0)

                # - Check if valid type
                if type(start) != IntegerBox:
                    self.errors += [{"description": "Expected an integer result as key.", "id": self.id}]
                    self.result = None
                if type(end) != IntegerBox:
                    self.errors += [{"description": "Expected an integer result as key.", "id": self.id}]
                    self.result = None

                # - Check if errors and abort eventually
                if len(self.errors) > 0:
                    self.result = None
                    return

                # - Get the value from the array
                self.result = self.result[start.value:end.value]

            elif index["op"] == "[n:]":

                index["start"].evaluate(scope, options)
                self.errors += index["start"].errors
                self.stack.update(index["start"].stack)

                # - Index value
                value = index["start"].result

                # - Try to convert to integer
                if type(value) == RollBox:
                    value = value + IntegerBox(0)

                # - Check if valid type
                if type(value) != IntegerBox:
                    self.errors += [{"description": "Expected an integer result as key.", "id": self.id}]
                    self.result = None

                # - Check if errors and abort eventually
                if len(self.errors) > 0:
                    self.result = None
                    return

                # - Get the value from the array
                self.result = self.result[value.value:]

            elif index["op"] == "[:n]":

                index["end"].evaluate(scope, options)
                self.errors += index["end"].errors
                self.stack.update(index["end"].stack)

                # - Index value
                value = index["end"].result

                # - Try to convert to integer
                if type(value) == RollBox:
                    value = value + IntegerBox(0)

                # - Check if valid type
                if type(value) != IntegerBox:
                    self.errors += [{"description": "Expected an integer result as key.", "id": self.id}]
                    self.result = None

                # - Check if errors and abort eventually
                if len(self.errors) > 0:
                    self.result = None
                    return

                # - Get the value from the array
                self.result = self.result[:value.value]

            elif index["op"] == "[n]":

                index["key"].evaluate(scope, options)
                self.errors += index["key"].errors
                self.stack.update(index["key"].stack)

                # - Index value
                value = index["key"].result

                if callable(value):
                    res = []
                    for index, item in enumerate(self.result):
                        filter = value(item, index)

                        if type(filter) is BooleanBox and filter.value:
                            res.append(item)

                    self.result = res
                    return

                # - Try to convert to integer
                if type(value) == RollBox:
                    value = value + IntegerBox(0)

                # - Check if valid type
                if type(value) != IntegerBox:
                    self.errors += [{"description": "Expected an integer result as key.", "id": self.id}]

                try:
                    # - Get the value from the array
                    self.result = self.result[value.value]
                except:
                    self.errors += [{"description": "Index out of range.", "id": self.id}]

                # - Check if errors and abort eventually
                if len(self.errors) > 0:
                    self.result = None
                    return

            # - Update the evaluation stack
            self.stack.update({self.id: self.result})
