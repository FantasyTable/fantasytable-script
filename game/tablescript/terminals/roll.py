from ..datatypes.rollbox import *


class Roll:

    def __init__(self, exp):

        # - Set expression
        self.exp = exp

        # - Get roll expressions
        self.roll_count = exp[0]
        self.roll_dice = exp[1]
        self.roll_values = exp[2:]

        # - Initialize values
        self.id = 0
        self.tree = {}
        self.errors = []
        self.stack = {}
        self.refs = {}
        self.result = None

    def generate_tree(self, id_manager):

        # - Set id for this expression
        self.id = id_manager.get_id()

        # - Generate expression tree for all sub expressions
        for expression in self.exp:
            expression.generate_tree(id_manager)

        # - Get roll values tree
        rolls = [elem.tree for elem in self.exp[2:]]

        self.tree = \
        {
            "type": "roll",
            "id": self.id,
            "count": self.exp[0].tree,
            "dice": self.exp[1].tree,
            "rolls": rolls
        }

    def evaluate(self, scope, options):

        # - Evaluate all sub expressions
        for expression in self.exp:
            expression.evaluate(scope, options)
            self.errors += expression.errors
            self.stack += expression.errors

        # - Get evaluated values for all expressions
        rolls = [elem.result for elem in self.exp[2:]]
        dice = self.exp[1].result
        rolls = self.exp[0].result

        try:
            # - Try to box this expression
            self.result = RollBox(rolls, dice, rolls)
        except e:
            self.errors += [{"description": str(e), "id": self.id}]
            self.result = None

        # - Update the stack
        self.stack.update({self.id: self.result})
