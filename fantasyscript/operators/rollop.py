from ..datatypes.integerbox import IntegerBox
from ..datatypes.rollbox import RollBox

from . import *


class RollOp:

    def __init__(self, exp):

        # - Set expression
        self.exp = exp

        # - Get expressions
        if type(exp) is list and len(exp) > 1:
            self.roll_count = exp[0]
            self.roll_dice = exp[1]

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

        # - Generate tree for the two expressions
        self.roll_count.generate_tree(id_manager)
        self.roll_dice.generate_tree(id_manager)

        self.tree = \
        {
            "type": "infix",
            "op": "d",
            "id": self.id,
            "left": self.roll_count,
            "right": self.roll_dice
        }

    def evaluate(self, scope, options):

        if pass_trough_calc(self, scope, options):
            return

        # - Evaluate roll count
        self.roll_count.evaluate(scope, options)
        self.errors += self.roll_count.errors
        self.stack.update(self.roll_count.stack)

        # - Abort if errors
        if len(self.errors) > 0:
            self.result = None
            return

        # - Get the result
        count = self.roll_count.result

        # TODO: Change casting method

        # - Convert to integer
        if type(count) == RollBox:
            count = count + IntegerBox(0)

        # - Check if we have the correct type
        if type(count) != IntegerBox:
            self.errors += [{"description": "Left roll operand must be an integer.", "id": self.id}]
            self.result = None
            return

        # - Evaluate dice type
        self.exp[1].evaluate(scope, options)
        self.errors += self.exp[1].errors
        self.stack.update(self.exp[1].stack)

        # - Abort if errors
        if len(self.errors) > 0:
            self.result = None
            return

        # - Get the result
        dice = self.exp[1].result

        # - Convert to integer
        if type(dice) == RollBox:
            dice = dice + IntegerBox(0)

        # - Check if we have the correct type
        if type(dice) != IntegerBox:
            self.errors += [{"description": "Right roll operand must be an integer.", "id": self.id}]
            self.result = None
            return

        # - Create the result boxed type
        self.result = RollBox(count, dice)

        # - Update the evaluation stack
        self.stack.update({self.id: self.result})
