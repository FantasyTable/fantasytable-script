from .stringbox import *
from .floatingbox import *
from .arraybox import *
from .integerbox import *
from .booleanbox import *
from .scope import *
from .boxed import *

import numbers

def convert_type(value, deep_scope, external_call, elem_id):

    if isinstance(value, numbers.Integral):
        return IntegerBox(value), [], {}, {}

    elif type(value) == float:
        return FloatingBox(value), [], {}, {}

    elif type(value) == bool:
        return BooleanBox(value), [], {}, {}

    elif type(value) == list:
        values = []
        errors = []
        stacks = {}
        trees = []
        for i in range(0, len(value)):
            val, error, stack, tree = convert_type(value[i], deep_scope, external_call, elem_id)
            values.append(val)
            errors = errors + error
            stacks.update(stack)
            trees.append(tree)
        return ArrayBox(values), errors, stacks, trees

    if type(value) == str:

        if value[0] == '!':
            try:
                return external_call(value[1:]), [], {}, {}
            except Exception as ex:
                return None, [{'description': 'Error during external function evaluation', 'internal': ex, 'id': elem_id}], {}, {}

        return StringBox(value), [], {}, {}

    if type(value) == dict:
        return Scope(value), [], {}, {}

    if isinstance(value, Boxed):
        return Scope(value.scope), [], {}, {}

    if callable(value) and value.__name__ == "evaluation_fun":
        try:
            value.__indexer__ = 2
            res = value(deep_scope)

            if len(res.errors) > 0:
                return None, [{'description': 'Error during external function evaluation', 'internal': res.errors, 'id': elem_id}], res.stack, res.tree

            val, err, stack, tree = convert_type(res.value, deep_scope, external_call, elem_id)

            return val, err, {**stack, **res.stack}, {**tree, **res.tree}

        except Exception as ex:
            return None, [{'description': 'Error during function evaluation', 'internal': ex, 'id': elem_id}], {}, {}

    return value, [], {}, {}
