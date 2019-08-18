from .stringbox import *
from .floatingbox import *
from .arraybox import *
from .integerbox import *
from .scope import *
from .boxed import *


def convert_type(value, deep_scope):

    if type(value) == int:
        return IntegerBox(value)

    elif type(value) == float:
        return FloatingBox(value)

    elif type(value) == list:
        values = []
        for i in range(0, len(value)):
            values.append(convert_type(value[i], deep_scope))
        return ArrayBox(values)

    if type(value) == str:
        return StringBox(value)

    if type(value) == dict:
        return Scope(value)

    if isinstance(value, Boxed):
        return Scope(value.scope)

    if callable(value) and value.__name__ == "evaluation_fun":
        try:
            res = value(deep_scope)
        except Exception as e:
            print(e)
        return convert_type(res, deep_scope)

    return value
