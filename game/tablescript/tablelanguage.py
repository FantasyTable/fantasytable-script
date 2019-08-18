import re

# - Import parser library
from pypeg2 import *

# - Import all basic type references
from .terminals.roll import Roll
from .terminals.label import Label
from .terminals.string import String
from .terminals.integer import Integer
from .terminals.boolean import Boolean
from .terminals.decimal import Decimal
from .terminals.terminal import Terminal

# - Import all operator references
from .operators.sum import Sum
from .operators.mul import Mul
from .operators.call import Call
from .operators.func import Func
from .operators.merge import Merge
from .operators.scope import Scope
from .operators.logic import Logic
from .operators.array import Array
from .operators.index import Index
from .operators.rollop import RollOp
from .operators.access import Access
from .operators.prefix import Prefix
from .operators.naming import Naming
from .operators.compare import Compare
from .operators.accesses import Accesses
from .operators.arrayroll import ArrayRoll
from .operators.expression import Expression
from .operators.parenthesis import Parenthesis


# - Label system - All letter combination except boolean and keywords ---------------------------------
ValidLabels = re.compile(r'(?!\btrue\b|\?|\bTrue\b|\bfalse\b|\bFalse\b|\bin\b|\bas\b|\bfunc\b)^\b([a-zA-Z]\w*)\b')
# -----------------------------------------------------------------------------------------------------

# - Terminal values -----------------------------------------------------------------------------------
Label.grammar = ValidLabels
Integer.grammar = re.compile(r'\d+')
Decimal.grammar = re.compile(r'\d+\.\d+')
String.grammar = re.compile(r'[\"\'](\\.|[^\\"])*[\"\']')
Array.grammar = [("[", csl(Expression), "]"), "[]"]
Boolean.grammar = re.compile(r'true|false|True|False')
Roll.grammar = "<", Integer, "d", Integer, "|", Integer, maybe_some(",", Integer), ">"
# -----------------------------------------------------------------------------------------------------

# - Terminal expression statement ---------------------------------------------------------------------
Terminal.grammar = [Roll, Decimal, Integer, Boolean, String, Array, Parenthesis, Label]
# -----------------------------------------------------------------------------------------------------

# - Access types --------------------------------------------------------------------------------------
AccessTypes = \
[
    (Expression, re.compile(r':'), Expression),
    (Expression, re.compile(r':')),
    (re.compile(r':'), Expression),
    Expression
]
# -----------------------------------------------------------------------------------------------------

# - Operators syntax ----------------------------------------------------------------------------------
Parenthesis.grammar = "(", Expression, ")"
Index.grammar = re.compile(r"\["), AccessTypes, re.compile(r"\]")
Call.grammar = re.compile(r'\('), optional((csl(Expression))), ")"
Access.grammar = contiguous(".", Label)

Accesses.grammar = contiguous(Terminal, maybe_some([Access, Call, Index]))

Prefix.grammar = maybe_some(re.compile(r'[-!]')), Accesses

RollOp.grammar = [([Integer, Parenthesis], "d", [Integer, Parenthesis]), Prefix]
ArrayRoll.grammar = [([Integer, Parenthesis], "[d]", [Integer, Parenthesis]), RollOp]

Merge.grammar = ArrayRoll, maybe_some("::", ArrayRoll)
Mul.grammar = Merge, maybe_some(re.compile(r'\*|//|/'), Merge)
Sum.grammar = Mul, maybe_some(re.compile(r'[+-]'), Mul)
Compare.grammar = Sum, maybe_some(re.compile(r'==|>=|<=|>|<|!='), Sum)
Logic.grammar = Compare, maybe_some(re.compile(r'\|\||&&'), Compare)

Func.grammar = optional(re.compile(r"\bfunc\b"), optional(csl(ValidLabels)), ":"), [Logic, Func]
Naming.grammar = separated(Func, optional(Keyword("as"), ValidLabels))
Scope.grammar = maybe_some(Naming, Keyword("in")), Func

Expression.grammar = Scope
# -----------------------------------------------------------------------------------------------------


class TableLanguage:

    grammar = Scope

    def __init__(self, exp):

        # - Set expression
        self.exp = exp

        # - Initialize values
        self.id = 0
        self.tree = {}
        self.errors = []
        self.stack = {}
        self.refs = []
        self.result = None

    def generate_tree(self, id_manager):

        # - Generate tree for main expression
        self.exp.generate_tree(id_manager)

        # - Merge the generated tree
        self.tree = self.exp.tree

    def evaluate(self, scope, options):

        # - Evaluate the whole expression
        self.exp.evaluate(scope, options)

        # - Merge the evaluation result
        self.stack = self.exp.stack
        self.result = self.exp.result
        self.errors = self.exp.errors
