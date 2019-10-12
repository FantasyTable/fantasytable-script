from game.gamestate import *
from game.tablescript import *

import json

# - Instantiate the parser
tablescript = TableScript()

while False:
    txt = input(">>> ")
    result = tablescript.eval(txt, {"ciao": {"giovanni": 2}})

    print(result.value)

with open("C:/Users/PizzaKun/Desktop/dnd.json", 'r') as dnd_file:
    with open("C:/Users/PizzaKun/Desktop/dnd_store.json", 'r') as dnd_store:
        with open("C:/Users/PizzaKun/Desktop/character.json", 'r') as chr_file:
            dnd = json.load(dnd_file)
            store = json.load(dnd_store)
            params = json.load(chr_file)

            manager = GameStateManager(dnd, store)

            parser = TableScript()

            manager.add_entity("astrid", "playable", params)

            result = manager.get_entity("astrid")

            result_str = json.dumps(result, indent=4, separators=(',', ': '))

            with open('C:/Users/PizzaKun/Desktop/output.json', 'w') as outfile:
                json.dump(result, outfile, indent=2, separators=(',', ': '))


            while True:
                txt = input(">>> ")

                results = manager.query(txt)

                res, err, stack, tree = results
                print("Result: " + str(res))
                print("Values: " + str(stack))
                print("Errors: " + str(err))
                print("Expression tree: " + str(tree))