from tablescript.tablescript import *

while True:
    txt = input(">>> ")
    scope = { "players": { "astrid": { "AC": 13, "HP": 23 } } }
    res = eval(txt, scope)
    print(res.value)
    print(res.tree)