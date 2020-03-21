import sys


def parse_script_string(script):

    script = script.lstrip(' ')

    if script[0] != '=':
        raise Exception("Invalid script.")

    return script[1:]


def parse_script(value, schema):

    scripts = []
    params = {}

    if type(value) == str:
        # - Parse the script string
        script = parse_script_string(value)

        # - Pull the script with the default target value
        scripts.append({"script": script, "target": "value"})

        return scripts, params

    value = value.copy()
    value.update(schema)

    if type(value) == dict:
        # - Check if we have at least the scripts
        if "_scripts_" not in value or type(value["_scripts_"]) != list:
            raise Exception("No scripts specified for this action.")

        # - Get the script list
        script_list = value["_scripts_"]

        for script_struct in script_list:
            if type(script_struct) == str:
                # - Parse the script string
                script = parse_script_string(script_struct)

                # - Pull the script with the default target value
                scripts.append({"script": script, "target": "value"})

                continue

            if "_script_" not in script_struct or "_target_" not in script_struct:
                raise Exception("Invalid script field.")

            # - Get the script target
            target = script_struct["_target_"]

            if target in ["assignment", "append"] and "_to_" not in script_struct:
                raise Exception("Script target field not specified.")

            # - Parse the script string
            script = parse_script_string(script_struct["_script_"])

            if target not in ["assignment", "append"]:
                scripts.append({"script": script, "target": target})
            else:
                # - Get the target field
                to = script_struct["_to_"]

                scripts.append({"script": script, "target": target, "to": to})

        if "_params_" in value:
            params = value["_params_"]

    return scripts, params
