import sys

def parse_boolean(value, schema):

    if type(value) != bool:
        raise Exception("Invalid boolean input")

    return value
