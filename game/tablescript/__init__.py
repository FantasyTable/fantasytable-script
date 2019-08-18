from .tablelanguage import TableLanguage
from pypeg2 import *
from .utils import *
from game.tablescript.datatypes.scope import *


class TableScript:

    def __init__(self, configs=None):

        self.configs = \
        {
            "cacheRolls": False,
            "calculateStack": True,
        }

        if configs:
            self.configs.update(configs)

        self.result = None
        self.errors = None
        self.stack = None
        self.tree = None

        # - A global id counter
        self.id_manager = IdManager()


    def eval(self, text, scope):

        try:
            # - Parse expression structure
            expression = self.parse(text)
        except SyntaxError as err:
            self.errors = [err]
            return None

        # - Get the evaluation tree
        expression.generate_tree(self.id_manager)

        self.configs["deepScope"] = scope

        # - Evaluate expression
        expression.evaluate(Scope(scope), self.configs)

        # - Dump all parsing information
        self.result = expression.result
        self.errors = expression.errors
        self.stack = expression.stack
        self.tree = expression.tree

        return expression.result

    def parse(self, text):

        if type(text) != str:
            raise Exception("Expecting a string")

        # - Parse expression structure
        return parse(text, TableLanguage)
