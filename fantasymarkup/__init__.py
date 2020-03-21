from .types.calculated import *
from .types.integer import *
from .types.boolean import *
from .types.struct import *
from .types.string import *
from .types.script import *
from .types.array import *

from .helpers.json import *

from game.tablescript import *


class FantasyMarkup:

    def __init__(self, game, store):

        self.store = store
        self.meta = game
        self.entities = {}
        self.actions = {}

    def add_entity(self, name, typename, state):

        # - Check state integrity
        errors = self.__state_integrity_check(typename, state)

        # - Raise errors

        # - Add the entity to the entity list
        self.entities[name] = { 'state': state, 'type': typename, 'name': name, 'cache': None }

        # - Make the first cached version
        self.entities[name]["cache"] = self.get_entity(name)

    def remove_entity(self, entity_name):

        # - Remove the entity from the dictionary
        self.entities.pop(entity_name)

    def invalidate_entity(self, entity_name):

        # - Invalidate the entity cache
        self.entities[entity_name]["cache"] = None

    def get_entity(self, name):

        if name not in self.entities:
            raise Exception("This entity does not exists")

        # - Get entity from the store
        entity = self.entities[name]
        state = entity["state"]
        type = entity["type"]
        cache = entity["cache"]

        # - Improve performance by caching
        if cache:
            return cache

        # - Get the type descriptor
        meta_type = self.meta[type]

        # - Calculate all dummy fields that no needs computation
        dummy_fields = self.__parse_dummy_fields(meta_type, state)

        # - Calculate all computed fields
        calculated = self.__parse_computed_fields(dummy_fields)

        # - Prepare all instance actions
        actions = self.__parse_action_fields(calculated, name)

        return actions

    def __state_integrity_check(self, typename, state):
        return None

    def __parse_dummy_fields(self, meta_type, params):

        if "_nullable_" in meta_type and meta_type["_nullable_"] and not params:
            return None

        if "_type_" not in meta_type:
            raise Exception("Type as not type identifier.")

        # - Get type name for parsing
        typename = meta_type["_type_"]

        if typename == "any":
            return params

        if typename == "integer":
            return parse_integer(params, meta_type)

        if typename == "string":
            return parse_string(params, meta_type)

        if typename == "boolean":
            return parse_boolean(params, meta_type)

        if typename == "calculated":
            # - Get the script
            script = parse_calculated(meta_type)

            def evaluation_fun(context):
                # - Instantiate the parser
                tablescript = TableScript({'externalCall': lambda x: self.actions[x]})

                # - Prepare the scope
                scope = {}
                scope.update(self.entities)
                scope.update(context)

                # - Evaluate script
                result = tablescript.eval(script, scope)

                return result

            return evaluation_fun

        if typename == "script":
            if type(params) == str:
                params = {"_scripts_": [{"_target_": "value", "_script_": params}]}

            return {**params, **meta_type}

        if typename == "reference":

            # - Get reference
            ref = meta_type["_to_"]

            if ref not in self.meta:
                raise Exception("The following type does not exists: " + ref)

            return self.__parse_dummy_fields(self.meta[ref], params)

        if typename == "array":
            res = []

            # - For each array element parse using the associated scope
            for schema, scope in parse_array(params, meta_type):
                val = self.__parse_dummy_fields(schema, scope)
                res.append(val)

            return res

        if typename == "struct":
            res = {}
            store = None

            if "_store_" in meta_type:

                # - Get the store element type
                store_name = meta_type["_store_"]

                # - Check if this element exists in the store
                if store_name not in self.store:
                    raise Exception("Store element not found")

                # - Get the store element
                store = self.store[store_name]

            # - Parse each struct's field
            for name, field in parse_struct(params, meta_type):

                scope = {}
                if store:
                    if "_select_" not in params:
                        raise Exception("Missing the selected type")

                    # - Add all the missing references
                    params.update([el for el in store if el["_id_"] == params["_select_"]][0])

                if name in params:
                    scope = params[name]

                # - Parse the current field with augmented context
                val = self.__parse_dummy_fields(field, scope)

                res[name] = val

            return res

        return meta_type

    def __parse_computed_fields(self, obj, root=None, self_obj=None):

        root = obj if not root else root
        self_obj = obj if not self_obj else self_obj

        if callable(obj):
            return obj({'self': self_obj, '$': root})

        if type(obj) == dict:
            result = {}

            if "_type_" in obj:
                return obj

            # - Enter in each field
            for key, value in obj.items():
                result[key] = self.__parse_computed_fields(value, root, obj)
            return result

        if type(obj) == list:
            result = []
            for value in obj:
                result.append(self.__parse_computed_fields(value, root, self_obj))
            return result

        return obj

    def __parse_action_fields(self, obj, entity_name, scope_path=[]):

        if type(obj) == dict:
            result = {}

            if "_type_" in obj:

                # - Get the structure type
                typename = obj["_type_"]

                if typename == "script":
                    scripts, params_meta = parse_script(obj, obj)

                    hash = entity_name + "." + '.'.join(scope_path)

                    # - Pick last scope
                    last_scope = scope_path if scope_path[-1].isdigit() else scope_path[0:-1]

                    self.actions[hash] = self.make_action_call(params_meta, scripts, entity_name, last_scope)

                    return "!" + hash

            # - Enter in each field
            for key, value in obj.items():
                result[key] = self.__parse_action_fields(value, entity_name, [*scope_path, key])
            return result

        if type(obj) == list:
            result = []
            for i, value in enumerate(obj):
                result.append(self.__parse_action_fields(value, entity_name, [*scope_path, str(i)]))
            return result

        return obj

    def make_action_call(self, meta_params, scripts, entity_name, scope_path):

        def action_call(*params):
            params_scope = {}
            results = []

            # - Check all parameters and validate them
            for i, (param_name, param_type) in enumerate(meta_params.items()):
                if i > len(params):
                    raise Exception("Missing parameter: " + param_name)
                params_scope[param_name] = self.__parse_dummy_fields(param_type, params[i])

            # - Get the local scope
            entity = self.get_entity(entity_name)
            local_entity = json_crawl(entity, scope_path)

            # - Execute all scripts
            for script in scripts:
                # - Instantiate the parser
                tablescript = TableScript({'externalCall': lambda x: self.actions[x]})

                # - Prepare the scope
                scope = {}
                scope.update(self.entities)
                scope.update(params_scope)
                scope.update({'$': entity, 'self': local_entity})

                # - Evaluate script
                result = tablescript.eval(script["script"], scope)
                result = result.value if result else None

                # - Get the script target
                target = script["target"]

                # - Get the assignment path
                path = json_path_split(script["to"]) if "to" in script else None

                if target in ["assignment", "append"]:

                    # - Check if path is available
                    if not path:
                        raise Exception("Target path not provided")

                    # - Get the entity parameters
                    entity_parameters = self.entities[entity_name]["state"]

                    # - Set the local scope
                    if path[0] == "self":
                        entity_parameters = json_crawl(entity_parameters, scope_path)

                    # - Skip the root symbol by default
                    if path[0] in ["$", "self"]:
                        path = path[1:]

                if target == "append":
                    # - Assign from entity list
                    json_array_push(entity_parameters, path, result)
                    self.invalidate_entity(entity_name)

                if target == "assignment":
                    # - Assign from entity list
                    json_assign(entity_parameters, path, result)
                    self.invalidate_entity(entity_name)

                results.append(result)

            return results[0] if len(results) == 1 else results

        return action_call

    def invoke(self, action_path, params):

        if action_path not in self.actions:
            raise Exception("This entity does not exists.")

        return self.actions[action_path](params)

    def query(self, script, additional_scope={}):

        # - Instantiate the parser
        tablescript = TableScript({'externalCall': lambda x: self.actions[x]})

        # - Prepare the scope
        scope = {}
        for entity in self.entities.values():
            scope.update({entity["name"]: self.get_entity(entity["name"])})
        scope.update(additional_scope)

        # - Evaluate script
        result = tablescript.eval(script, scope)

        return result
