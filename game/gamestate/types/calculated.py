

def parse_calculated(schema):

    if "_script_" not in schema:
        raise Exception("Missing script field")

    # - Get the script
    script = schema["_script_"]

    return script
