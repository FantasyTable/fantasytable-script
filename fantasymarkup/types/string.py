

def parse_string(value, schema):

    if type(value) != str:
        raise Exception("Invalid string input")

    return value