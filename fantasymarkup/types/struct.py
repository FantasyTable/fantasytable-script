

def parse_struct(value, schema):

    if type(value) != dict:
        raise Exception("Invalid struct input")

    keywords = ["_type_", "_store_"]

    return [(key, value) for key, value in schema.items() if key not in keywords]
