

def parse_array(value, schema):

    if type(value) != list:
        raise Exception("Invalid array input")

    if "_of_" not in schema:
        raise Exception("Missing type specifier for this array")

    # - Get elem schema
    elem_schema = schema["_of_"]

    elems = []
    for elem in value:
        elems.append((elem_schema, elem))

    return elems
