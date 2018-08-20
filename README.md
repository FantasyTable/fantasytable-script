# Table script
Tablescript is a simple scripting language that allows to makes mathematical operations with some extra features like: dice throws, structures, arrays, conditions, loops, function calls and definitions.

## Installation
This project is made using pipenv with pycharm (see [here](https://www.jetbrains.com/help/pycharm/pipenv.html) how to configure pipenv), you needs only to install the dependencies and run the tests or the main file to try a demo.

- `git clone https://github.com/virtual-table/tablescript.git`
- Open folder with pycharm
- Configure pipenv (if needed), see [this](https://www.jetbrains.com/help/pycharm/pipenv.html)

## Usage
To run a tablescript code you can simply use the `eval(str, scope)` function in the tablescript module.

```Python

from tablescript.tablescript import *

while True:
    txt = input(">>> ")
    scope = { "players": { "astrid": 2 } }
    res = eval(txt, scope)
    print(res.value)
    print(res.tree)
```

This function returns a tuple containing the evaluation result and a json in the tree field that represent the expression tree.

## Syntax
To see the full syntax guide see the wiki for this repo.

### Types
| Type          | Syntax            | Python type  |
| ------------- |:------------------| ------------:|
| integer       | 1 (just a digit)  | IntegerBox   |
| float         | 1.0 (use dot)     | FloatingBox  |
| diceroll      | <2d20\| 4, 17>    | RollBox      |
| array         | [expression, ...] | ArrayBox     |
| boolean       | true or false     | BooleanBox   |

### Operators
| Name          | Syntax                            | Description                                                       |
| ------------- |:----------------------------------|:----------------------------------------------------------------- |
| sum           | type + type                       | Sum two values                                                    |
| sub           | type - type                       | Subtract two values                                               |
| mul           | type * type                       | Multiply two values                                               |
| div           | type / type                       | Divide two values                                                 |
| int div       | type // type                      | Integer part of the division                                      |
| append        | type :: type                      | Makes an array merging two values                                 |
| not           | !boolean or ![boolean,...]        | Boolean invert operator                                           |
| and           | boolean && boolean or []&&[]      | And boolean operator                                              |
| or            | boolean \|\| boolean or []\|\|[]  | Or boolean operator                                               |
| compare       | type >, <, >=, <=, ==, != type    | Less than, Greater than, LessEqual, GreaterEqual, Equal, NotEqual |
| dice roll     | \<v0\>d\<v1\> (Es. 2d20)          | Throws v0 number of dices with v1 faces                           | 
| dice roll arr | \<v0\>[d]\<v1\> (Es 2[d]20)       | Same as previous but each dice is an array field                  |
| label         | a label can't start with numbers  | Check in the scope if there's a variable with this name getting the value |
| access        | label.label                       | Access to a struct field by label name                            |
| index         | [2] or [1:3] or [2:] or [:2]      | Get a value or a slice of array                                   |

## TODO list

- [ ] A good exceptions handling
