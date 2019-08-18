from .types import *


def instance(template, metatype, parameters):

    output = {}

    for field, fieldtype in metatype.items():

        # - Try to parse this type with base type
        parsed, value = parse_type(fieldtype, field, parameters)

        if parsed:
            output[field] = value
            continue

        # - Try to check if is a nested type
        parsed, value, template = parse_nested(fieldtype, field, parameters)

        if parsed:
            output[field] = instance(template, template, value)
            continue

        # - Try to check if is an array
        parsed, values, template = parse_nested(fieldtype, field, parameters)

        if parsed:
            output[field] = instance(template, template, value)
            continue

        # - Try to check if is an array
        parsed, values = parse_list(fieldtype, field, parameters)

        if parsed:
            output[field] = []

            for pair in values:
                value, template = pair
                output[field].append(instance(template, template, value))
            continue

    return output