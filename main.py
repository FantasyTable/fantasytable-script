from game.gamestate import *
from game.tablescript import *

import json, pprint as pp

character = \
{
    "hitPoints": 23,
    "tempHitPoints": 0,

    "baseStr": 15,
    "baseDex": 11,
    "baseCon": 12,
    "baseInt": 13,
    "baseWis": 14,
    "baseCha": 15,

    "bonusStr": 0,
    "bonusDex": 0,
    "bonusCon": 3,
    "bonusInt": 0,
    "bonusWis": -1,
    "bonusCha": 0,

    "classes":
    [
        { "level": 3, "class": { "_select_": "fighter" } }
    ],

    "race": { "_select_": "half-elf" }
}

store = \
{
    "classes":
    [
        {
            "_id_": "fighter",

            "name": "Fighter",
            "description": "A fighter.",

            "features":
            [
                { "level": 1, "feature": { "_select_": "Second Wind" } }
            ]
        }
    ],

    "races":
    [
        {
            "_id_": "half-elf",

            "name": "Half-Elf",
            "description": "An half elf.",

            "features": [ { "_select_": "Half-Elf Ability Bonus" } ]
        }
    ],

    "features":
    [
        {
            "_id_": "Second Wind",

            "name": "Second Wind",
            "description": "You have a limited well of stamina that you can draw on to protect yourself from harm. On your turn, you can use a bonus action to regain hit points equal to 1d10 + your fighter level. Once you use this feature, you must finish a short or long rest before you can use it again.",
            "bonuses": [],
            "actions":
            [
                "1d10 + self.classes[val.class.name == 'fighter'].level",
                "1d10 + self.classes[val.class.name == 'fighter'].level"
            ]
        },

        {
            "_id_": "Half-Elf Ability Bonus",

            "name": "Ability Bonus",
            "description": "You have a limited well of stamina that you can draw on to protect yourself from harm. On your turn, you can use a bonus action to regain hit points equal to 1d10 + your fighter level. Once you use this feature, you must finish a short or long rest before you can use it again.",
            "actions": [],
            "bonuses":
            [
                { "field": "charisma", "value": 2 },
                { "field": "dexterity", "value": 1 }
            ]
        }
    ]
}

output = \
{
  "hitPoints": 23,
  "tempHitPoints": 0,
  "strength": 15,
  "decterity": 11,
  "constitution": 15,
  "intelligence": 13,
  "wisdom": 13,
  "charisma": 17,
  "raceStr": 0,
  "raceDex": 0,
  "raceCon": 0,
  "raceInt": 0,
  "raceWis": 0,
  "raceCha": 2,
  "baseStr": 15,
  "baseDex": 11,
  "baseCon": 12,
  "baseInt": 13,
  "baseWis": 14,
  "baseCha": 15,
  "bonusStr": 0,
  "bonusDex": 0,
  "bonusCon": 3,
  "bonusInt": 0,
  "bonusWis": -1,
  "bonusCha": 0,
  "classes": [
    {
      "level": 3,
      "class": {
        "name": "Fighter",
        "description": "A fighter.",
        "features": [
          {
            "level": 1,
            "feature": {
              "name": "Second Wind",
              "description": "You have a limited well of stamina that you can draw on to protect yourself from harm. On your turn, you can use a bonus action to regain hit points equal to 1d10 + your fighter level. Once you use this feature, you must finish a short or long rest before you can use it again.",
              "actions": [
                {
                  "_type_": "script"
                },
                {
                  "_type_": "script"
                }
              ],
              "bonuses": []
            }
          }
        ]
      }
    }
  ],
  "race": {
    "name": "Half-Elf",
    "description": "An half elf.",
    "features": [
      {
        "name": "Ability Bonus",
        "description": "You have a limited well of stamina that you can draw on to protect yourself from harm. On your turn, you can use a bonus action to regain hit points equal to 1d10 + your fighter level. Once you use this feature, you must finish a short or long rest before you can use it again.",
        "actions": [],
        "bonuses": [
          {
            "field": "charisma",
            "value": 2
          },
          {
            "field": "dexterity",
            "value": 1
          }
        ]
      }
    ]
  }
}


#manager = GameStateManager(dnd, store)

parser = TableScript()

def test():
    while True:
        txt = input(">>> ")
        scope = {"self": output}
        res = parser.eval(txt, scope)
        if len(parser.errors) == 0:
            print("Result: " + str(parser.result.value))
        else:
            pp.pprint(vars(parser.errors[0]))
        #print("Values: " + str(parser.stack))
        #print("Expression tree: " + str(parser.tree))

test()
result = manager.add_entity("astrid", "playable", params)

result_str = json.dumps(result, indent=4, separators=(',', ': '))

with open('/home/pizzakun/Desktop/output.json', 'w') as outfile:
    json.dump(result, outfile, indent=2, separators=(',', ': '))

print(result_str)
