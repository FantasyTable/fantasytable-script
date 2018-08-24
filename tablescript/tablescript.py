from collections import namedtuple

from pypeg2 import *
from .typedefs import *
from .operators import *
from .utils import *
from .scope import *


TerminalExpression.grammar = \
[
	MemberAccess,
	Roll,
	Decimal,
	Number,
	Boolean,
	String,
	Label,
	Array,
	Parenthesis
]

Expression.grammar = ScopeMerge


class TableLanguage:

	grammar = Expression

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


def eval(text, scope):

	id_manager = IdManager()

	options = {

		"cacheRolls": False,
		"calculateStack": True,

	}

	expression = parse(text, TableLanguage)
	expression.generate_tree(id_manager)
	expression.evaluate(Scope(scope), options)
	Tp = namedtuple("ParsingRes", ["result", "errors", "valueStack", "tree"])
	return Tp(expression.result, expression.errors, expression.stack, expression.tree)