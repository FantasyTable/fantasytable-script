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
        return IntegerBox(value), []

    elif type(value) == float:
        return FloatingBox(value), []

    elif type(value) == bool:
        return BooleanBox(value), []

    elif type(value) == list:
        values = []
        for i in range(0, len(value)):
            values.append(convert_type(value[i], deep_scope, external_call))
        return ArrayBox(values), []

    if type(value) == str:

        if value[0] == '!':
            try:
                return external_call(value[1:]), []
            except Exception as ex:
                return None, [{'description': 'Error during external function evaluation', 'internal': ex, 'id': elem_id}]

        return StringBox(value), []

    if type(value) == dict:
        return Scope(value), []

    if isinstance(value, Boxed):
        return Scope(value.scope), []

    if callable(value) and value.__name__ == "evaluation_fun":
        try:
            value.__indexer__ = 2
            res = value(deep_scope)
        except Exception as ex:
            return None, [{'description': 'Error during function evaluation', 'internal': ex, 'id': elem_id}]
        return convert_type(res, deep_scope, external_call)

    return value
