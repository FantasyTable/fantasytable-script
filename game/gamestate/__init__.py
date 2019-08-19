from .types.calculated import *
from .types.integer import *
from .types.struct import *
from .types.string import *
from .types.array import *

from game.tablescript import *


class GameStateManager:

    def __init__(self, game, store):

        self.store = store
        self.meta = game
        self.entities = {}

    def add_entity(self, name, typename, state):

        # - Create a new entity based on the schema
        entity = self.new(typename, state)

        # - Add the entity to the entity list
        self.entities[name] = entity

        return entity

    def remove_entity(self, entity_name):

        # - Remove the entity from the dictionary
        self.entities.pop(entity_name)

    def new(self, typename, params):

        metatype = self.meta[typename]

        # - Start parsing
        return self.entity_state(metatype, params)

    def query(self, script, additional_scope={}):

        # - Instantiate the parser
        tablescript = TableScript({})

        # - Prepare the scope
        scope = {}
        scope.update(self.entities)
        scope.update(additional_scope)

        # - Evaluate script
        result = tablescript.eval(script, scope)

        return result.value if result else None

    def entity_state(self, metatype, params):

        dummy_fields = self.parse_field(metatype, params)

        return self.parse_scripts(dummy_fields)

    def parse_field(self, metatype, params):

        if "_type_" not in metatype:
            raise Exception("Type as not type identifier.")

        # - Get type name for parsing
        typename = metatype["_type_"]

        if typename == "any":
            return params

        if typename == "integer":
            return parse_integer(params, metatype)

        if typename == "string":
            return parse_string(params, metatype)

        if typename == "struct":
            res = {}
            store = None

            if "_store_" in metatype:

                # - Get the store element type
                store_name = metatype["_store_"]

                # - Check if this element exists in the store
                if store_name not in self.store:
                    raise Exception("Store element not found")

                # - Get the store element
                store = self.store[store_name]

            # - Parse each struct's field
            for name, field in parse_struct(params, metatype):

                scope = {}
                if store:
                    if "_select_" not in params:
                        raise Exception("Missing the selected type")

                    # - Add all the missing references
                    params.update([el for el in store if el["_id_"] == params["_select_"]][0])

                if name in params:
                    scope = params[name]

                # - Parse the current field with augmented context
                val = self.parse_field(field, scope)

                res[name] = val

            return res

        if typename == "array":
            res = []

            # - For each array element parse using the associated scope
            for schema, scope in parse_array(params, metatype):

                val = self.parse_field(schema, scope)

                res.append(val)

            return res

        if typename == "reference":

            # - Get reference
            ref = metatype["_to_"]

            if ref not in self.meta:
                raise Exception("The following type does not exists: " + ref)

            return self.parse_field(self.meta[ref], params)

        if typename == "calculated":
            # - Get the script
            script = parse_calculated(metatype)

            def evaluation_fun(ctx):
                return self.query(script, ctx)

            # - Calculate the script result
            return evaluation_fun

        return metatype

    def parse_scripts(self, params, global_params=None):

        if not global_params:
            global_params = params

        if callable(params):
            return params({"self": global_params})

        if type(params) == dict:
            result = {}
            for key, value in params.items():
                result[key] = self.parse_scripts(value, global_params)
            return result

        if type(params) == list:
            result = []
            for value in params:
                result.append(self.parse_scripts(value, global_params))
            return result

        return params
