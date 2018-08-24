from .datatypes.floatingbox import *
from .datatypes.integerbox import *
from .datatypes.booleanbox import *
from .datatypes.stringbox import *
from .datatypes.arraybox import *
from .datatypes.rollbox import *
from .scope import *


class IdManager:

    def __init__(self):
        self.current_id = 0

    def get_id(self):
        self.current_id = self.current_id + 1
        return self.current_id

    def reset(self):
        self.current_id = 0


def convertType(value):

    """ Convert a standard python type to a boxed type.

    :param value: Original value.
    :return: Boxed value.
    """

    if type(value) == int:
        return IntegerBox(value)

    elif type(value) == float:
        return FloatingBox(value)

    elif type(value) == list:
        values = []
        for i in range(0, len(value)):
            values.append(convertType(value[i]))
        return ArrayBox

    if type(value) == dict:
        return Scope(value)

    return value