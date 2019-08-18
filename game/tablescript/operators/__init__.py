

def pass_trough_calc(obj, scope, options):

    if type(obj.exp) == list and len(obj.exp) == 1:
        obj.exp = obj.exp[0]

    if type(obj.exp) != list:
        obj.exp.evaluate(scope, options)
        obj.result = obj.exp.result
        obj.errors = obj.exp.errors
        obj.stack = obj.exp.stack
        return True

    return False


def pass_trough_tree(obj, id_manager):

    if type(obj.exp) == list and len(obj.exp) == 1:
        obj.exp = obj.exp[0]

    if type(obj.exp) != list:
        obj.exp.generate_tree(id_manager)
        obj.tree = obj.exp.tree
        return True

    return False