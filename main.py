from tablescript.tablescript import *

while True:
    txt = input(">>> ")
    scope = {"players": {"astrid": {"AC": 13, "HP": 23, "cha": 3}, "enemy": {"AC": 13, "HP": 23}}, "pane": 2}
    res = eval(txt, scope)
    print(res.value)
    print(res.tree)
