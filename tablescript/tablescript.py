from collections import namedtuple

from pypeg2 import *
from .typedefs import *
from .operators import *
from .scope import *


TerminalExpression.grammar = \
	[
		MemberAccess,
		RollOperator,
		ArrayRoll,
		Roll,
		Decimal,
		Number,
		Boolean,
		Label,
		Array,
		Parenthesis
	]

Expression.grammar = BoolLogic


class TableLanguage:

	grammar = Expression

	def __init__(self, exp):
		self.exp = exp

	def evaluate(self, scope):
		return self.exp.evaluate(scope)


def eval(text, scope):

	res = parse(text, TableLanguage).evaluate(Scope(scope))
	Tp = namedtuple("ParsingRes", ["value", "tree"])
	return Tp(res[1], res[0])
