import sys

def parse_integer(value, schema):

    if type(value) != int:
        raise Exception("Invalid integer input")

    vmax =  sys.maxsize
    vmin = -sys.maxsize - 1

    if "_max_" in schema: vmax = schema["_max_"]
    if "_min_" in schema: vmin = schema["_min_"]

    if value > vmax or value < vmin:
        raise Exception("Integer value out of bound")

    return value
