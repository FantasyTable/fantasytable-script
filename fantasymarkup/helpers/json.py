import re

def json_path_split(path):
    return re.split("[.\[\]]", path)


def json_crawl_operation(source, path, op):

    if type(source) == list and path[0].isdigit() and 0 <= int(path[0]) < len(source):

        # - Make the operation
        if len(path) == 1:
            op(source, int(path[0]))
            return

        # - Continue searching for the field
        json_crawl_operation(source[int(path[0])], path[1:], op)

    if type(source) == dict and type(path[0]) == str and path[0] in source:

        # - Make the operation
        if len(path) == 1:
            op(source, path[0])
            return

        # - Continue searching for the field
        json_crawl_operation(source[path[0]], path[1:], op)

    raise Exception("Invalid field path")


def json_crawl(source, path):

    if len(path) <= 0:
        return source

    if type(source) == list and path[0].isdigit() and 0 <= int(path[0]) < len(source):

        # - Make the operation
        if len(path) == 1:
            return source[int(path[0])]

        # - Continue searching for the field
        return json_crawl(source[int(path[0])], path[1:])

    if type(source) == dict and type(path[0]) == str and path[0] in source:

        # - Make the operation
        if len(path) == 1:
            return source[path[0]]

        # - Continue searching for the field
        return json_crawl(source[path[0]], path[1:])

    raise Exception("Invalid field path")


def json_assign(source, path, data):

    def assign_func(s, p):
        s[p] = data

    # - Make the assignment
    json_crawl_operation(source, path, assign_func)


def json_array_push(source, path, data):

    def assign_func(s, p):
        if type(s[p]) != list:
            raise Exception("Invalid field path")

        s[p].append(data)

    # - Make the push
    json_crawl_operation(source, path, assign_func)
