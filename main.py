from game.gamestate import *
from game.tablescript import *

import json

with open("C:/Users/PizzaKun/Desktop/dnd.json", 'r') as dnd_file:
    with open("C:/Users/PizzaKun/Desktop/dnd_store.json", 'r') as dnd_store:
        with open("C:/Users/PizzaKun/Desktop/character.json", 'r') as chr_file:
            dnd = json.load(dnd_file)
            store = json.load(dnd_store)
            params = json.load(chr_file)

            manager = GameStateManager(dnd, store)

            parser = TableScript()

            def test():
                with open("C:/Users/PizzaKun/Desktop/output.json", 'r') as ch_f:
                    ch = json.load(ch_f)
                    while True:
                        txt = input(">>> ")
                        scope = {"self": ch}
                        res = parser.eval(txt, scope)
                        print("Result: " + str(parser.result))
                        print("Values: " + str(parser.stack))
                        print("Errors: " + str(parser.errors))
                        print("Expression tree: " + str(parser.tree))

            test()
            result = manager.add_entity("astrid", "playable", params)

            result_str = json.dumps(result, indent=4, separators=(',', ': '))

            with open('C:/Users/PizzaKun/Desktop/output.json', 'w') as outfile:
                json.dump(result, outfile, indent=2, separators=(',', ': '))

            print(result_str)

