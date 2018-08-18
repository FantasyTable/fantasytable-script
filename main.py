from tablescript.tablescript import *

while True:
    txt = input(">>> ")
    scope = { "players": { "astrid": 2 } }
    res = eval(txt, scope)
    print(res.value)
    print(res.tree)