#!/bin/python3
#
# pythfinder.py

import sys
import json

### CLASSES ###

# Main character class
class Character:
    def __init__(self, data = {}):
        # Grab keys from imported json data
        keys = data.keys()

        # These are the simple values (those of a type like string, int, etc.). 
        # More complex values will get their own objects initialized.
        self.name = data["name"] if "name" in keys else ""
        self.race = data["race"] if "race" in keys else ""
        self.deity = data["deity"] if "deity" in keys else ""
        self.homeland = data["homeland"] if "homeland" in keys else ""
        self.CMB = data["CMB"] if "CMB" in keys else 0
        self.CMD = data["CMD"] if "CMD" in keys else 10
        self.initiativeMods = data["initiativeMods"] if "initiativeMods" in keys else []
        self.alignment = data["alignment"] if "alignment" in keys else ""
        self.description = data["description"] if "description" in keys else ""
        self.height = data["height"] if "height" in keys else ""
        self.weight = data["weight"] if "weight" in keys else 0
        self.size = data["size"] if "size" in keys else ""
        self.age = data["age"] if "age" in keys else 0
        self.hair = data["hair"] if "hair" in keys else ""
        self.eyes = data["eyes"] if "eyes" in keys else ""
        self.languages = data["languages"] if "languages" in keys else []
        self.baseAttackBonus = data["baseAttackBonus"] if "baseAttackBonus" in keys else []
        self.gold = data["gold"] if "gold" in keys else 0

        # Complex object members
        if "speed" in keys:
            self.speed = CharacterSpeed(data = data["speed"])
        else:
            self.speed = CharacterSpeed() 

        self.classes = []
        if "classes" in keys:
            for item in data["classes"]:
                self.classes += [CharacterClass(item)]

        if "abilities" in keys:
            self.abilities = CharacterAbilities(data = data["abilities"])
        else:
            self.abilities = CharacterAbilities()

        if "hp" in keys:
            self.hp = CharacterHP(data = data["hp"])
        else:
            self.hp = CharacterHP()

        self.special = []
        if "special" in keys:
            for item in data["special"]:
                self.special += [CharacterBasicItem(item)]

        self.traits = []
        if "traits" in keys:
            for item in data["traits"]:
                self.traits += [CharacterBasicItem(item)]

        self.feats = []
        if "feats" in keys:
            for item in data["feats"]:
                self.feats += [CharacterBasicItem(item)]


        self.equipment = data["equipment"] if "equipment" in keys else []

        # saving throws are unique; check class definition and template
        self.savingThrows = {}
        
        self.savingThrows = data["savingThrows"] if "savingThrows" in keys else {}
        self.skills = data["skills"] if "skills" in keys else []
        self.attacks = data["attacks"] if "attacks" in keys else []

    # Get the modifier for a given ability
    def getAbilityMod(self, ability):
        abilityRange = ["str","dex","con","int","wis","cha"]
        if ability not in abilityRange:
            raise ValueError("getAbilityMod: ability must be one of " + abilityRange)
        value = self.abilities[ability]
        if value == 1:
            return -5
        elif value in [2, 3]:
            return -4
        elif value in [4, 5]:
            return -3
        elif value in [6, 7]:
            return -2
        elif value in [8, 9]:
            return -1
        elif value in [10, 11]:
            return 0
        elif value in [12, 13]:
            return 1
        elif value in [14, 15]:
            return 2
        elif value in [16, 17]:
            return 3
        elif value in [18, 19]:
            return 4
        elif value in [20, 21]:
            return 5
        elif value in [22, 23]:
            return 6
        elif value in [24, 25]:
            return 7
        elif value in [26, 27]:
            return 8
        elif value in [28, 29]:
            return 9
        elif value in [30, 31]:
            return 10
        else:
            raise ValueError("getAbilityMod: ability must be within range of 1-31, inclusive.")

    # Returns a dict containing the character object, without long elements 
    # like skills, feats, traits, spells, and equipment.
    def getCharacterShort(self):
        output = {}
        output["name"] = self.name
        output["race"] = self.race
        output["classes"] = self.classes
        output["alignment"] = self.alignment
        output["description"] = self.description
        output["height"] = self.height
        output["weight"] = self.weight
        output["abilities"] = self.abilities
        output["hp"] = self.hp
        return output

class CharacterSpeed:
    def __init__(self,
                 base = 0,
                 armor = 0,
                 fly = 0,
                 swim = 0,
                 climb = 0,
                 burrow = 0,
                 data = {}):
        keys = data.keys()
        self.base = data["base"] if "base" in keys else base
        self.armor = data["armor"] if "armor" in keys else armor
        self.fly = data["fly"] if "fly" in keys else fly
        self.swim = data["swim"] if "swim" in keys else swim
        self.climb = data["climb"] if "climb" in keys else climb
        self.burrow = data["burrow"] if "burrow" in keys else burrow

class CharacterClass:
    def __init__(self,
                 name = "",
                 archetypes = [],
                 level = 0,
                 data = {}):
        keys = data.keys()
        self.name = data["name"] if "name" in keys else name
        self.archetypes = data["archetypes"] if "archetypes" in keys else archetypes
        self.level = data["level"] if "level" in keys else level

class CharacterAbilities:
    def __init__(self,
                 str_ = 10,
                 dex = 10,
                 con = 10,
                 int_ = 10,
                 wis = 10,
                 cha = 10,
                 data = {}):
        keys = data.keys()
        self.str = data["str"] if "str" in keys else str_
        self.dex = data["dex"] if "dex" in keys else dex
        self.con = data["con"] if "con" in keys else con
        self.int = data["int"] if "int" in keys else int_
        self.wis = data["wis"] if "wis" in keys else wis
        self.cha = data["cha"] if "cha" in keys else cha

class CharacterHP:
    def __init__(self,
                 max_ = 0,
                 current = 0,
                 temporary = 0,
                 data = {}):
        keys = data.keys()
        self.max = data["max"] if "max" in keys else max_
        self.current = data["current"] if "current" in keys else current
        self.temporary = data["temporary"] if "temporary" in keys else temporary

class CharacterBasicItem:
    def __init__(self,
                 name = "",
                 description = "",
                 notes = "",
                 data = {}):
        keys = data.keys()
        self.name = data["name"] if "name" in keys else name
        self.description = data["description"] if "description" in keys else description
        self.notes = data["notes"] if "notes" in keys else notes

class CharacterSavingThrow:
    def __init__(self,
                 base = 0,
                 bonuses = [],
                 data = {}):
        keys = data.keys()
        self.base = data["base"] if "base" in keys else base
        self.bonuses = data["bonuses"] if "bonuses" in keys else bonuses

class CharacterSkill:
    def __init__(self,
                 name = "",
                 rank = 0,
                 isClass = False,
                 mod = "",
                 notes = "",
                 useUntrained = True,
                 misc = 0,
                 data = {}):
        keys = data.keys()
        self.name = data["name"] if "name" in keys else name
        self.rank = data["rank"] if "rank" in keys else rank
        self.isClass = data["isClass"] if "isClass" in keys else isClass
        self.mod = data["mod"] if "mod" in keys else mod
        self.notes = data["notes"] if "notes" in keys else notes
        self.useUntrained = data["useUntrained"] if "useUntrained" in keys else useUntrained
        self.misc = data["misc"] if "misc" in keys else misc

class CharacterAttack:
    def __init__(self,
                 weapon = "",
                 attackType = "",
                 damageType = [],
                 damage = "",
                 critRoll = 0,
                 critMulti = 0,
                 range_ = 0,
                 notes = 0,
                 data = {}):
        keys = data.keys()
        self.weapon = data["weapon"] if "weapon" in keys else weapon
        self.attackType = data["attackType"] if "attackType" in keys else attackType
        self.damageType = data["damageType"] if "damageType" in keys else damageType
        self.damage = data["damage"] if "damage" in keys else damage
        self.critRoll = data["critRoll"] if "critRoll" in keys else critRoll
        self.critMulti = data["critMulti"] if "critMulti" in keys else critMulti
        self.range = data["range"] if "range" in keys else range_
        self.notes = data["notes"] if "notes" in keys else notes

### FUNCTIONS ###

# Write the given character data to the file in path
def writeCharacter(character, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(character.__dict__, f, indent=4)

### MAIN ###

if __name__ == "__main__":
    # These inner functions are just for the CLI; the API will utilize its own 
    # functions to format the elements of the object.

    # Formatted string of items
    def getEquipmentString(c):
        total = 0
        totalCamp = 0
        outstring = "\n    Items:\n\n    Gold: {}\n\n    ".format(str(c.gold))
        for item in sorted(c.equipment, key = lambda i: i["name"]):
            total += item["weight"] * item["count"]
            outstring += "{} - Unit Weight: {} lbs, Count: {}".format(item["name"],str(item["weight"]),str(item["count"]))
            if item["notes"]:
                outstring += ", Notes: {}".format(item["notes"])
            if item["pack"]:
                outstring += " (pack item)"
                totalCamp += item["weight"] * item["count"]
            outstring += "\n    "
        outstring += "\n    Total weight: {}\n    Total weight (with camp set up): {}".format(str(total),str(totalCamp))
        return outstring

    # Formatted string of feats
    def getFeatString(c):
        outstring = "\n    Feats:\n\n    "
        for feat in c.feats:
            outstring += "{}:\n        {}\n        {}\n    ".format(feat["name"],feat["description"],feat["notes"])
        return outstring

    # Formatted string of traits
    def getTraitString(c):
        outstring = "\n    Traits:\n\n    "
        for trait in c.traits:
            outstring +=  "{}:\n        {}\n    ".format(trait["name"],trait["description"])
        return outstring

    # Formatted string of skills
    def getSkillString(c):
        outstring = "\n    Skills:\n\n    "
        for skill in c.skills:
            total = 0
            if not skill["useUntrained"]:
                outstring += "*"
            outstring += skill["name"] 
            outstring += " - " + str(skill["rank"]) + " (ranks) "
            total += skill["rank"]
            if skill["isClass"] and skill["rank"] > 0:
                outstring += "+ 3 (class) "
                total += 3
            outstring += "+ " + str(c.getAbilityMod(skill["mod"])) + " (mod: " + skill["mod"] + ") "
            total += c.getAbilityMod(skill["mod"])
            if skill["misc"] > 0:
                total += skill["misc"]
                outstring += "+ " + str(skill["misc"]) + " (misc) "
            outstring += "= " + str(total) + "\n    "
        return outstring

    # Formatted string of attacks
    def getAttackString(c):
        outstring = "\n    Attacks:\n    "
        for attack in c.attacks:
            outstring += "\n    " + attack["weapon"] + " (" + attack["attackType"] + ")\n        "
            outstring += "Damage: " + attack["damage"] + " " + str(attack["critRoll"])
            if attack["critRoll"] < 20:
                outstring += "-20"
            outstring += " x" + str(attack["critMulti"]) + " (" + ",".join(attack["damageType"]) + ") "
            if attack["range"] > 0:
                outstring += "\n        " + str(attack["range"]) + " ft. range increment"
            if attack["notes"]:
                outstring += "\n        " + attack["notes"]
            outstring += "\n    "
        return outstring

    # Returns a formatted string of abilities
    def getAbilityString(c):
        outstring = "\n    Abilities:\n\n    "
        for k, v in c.abilities.items():
            modValue = c.getAbilityMod(k)
            if modValue >= 0:
                modString = "+" + str(modValue)
            else:
                modString = str(modValue)
            outstring += k + ": " + str(v) + " (" + modString + ")\n    "
        return outstring

    # Formatted string of special abilities
    def getSpecialString(c):
        outstring = "\n    Special:\n\n"
        for item in c.special:
            outstring += "    {}:\n    {}\n    {}\n\n".format(item["name"],item["description"],item["notes"])
        return outstring

    # Primary user input function
    def getInput():
        arg = ""
        args = ["character",
                "abilities",
                "skills",
                "items",
                "attacks",
                "special",
                "feats",
                "traits",
                "quit",
                "q"]
        inputString = ""
        inputString += data + " (" + character.name + ") > "
        arg = input(inputString)
        while not arg in args:
            print("\n    Usage:\n\n" + "    {" + "|".join(args[:-1]) + "}\n")
            arg = input(inputString)
        return arg

    # Any functions that intend to change character data will flag this as True; at 
    # the end of the loop, if this is true, data will be written to the data 
    # argument given as input.
    dataChanged = False

    # Check for argument
    if not (len(sys.argv) >= 2):
        print("Usage: " + sys.argv[0] + " <data_path>")
        sys.exit()

    data = sys.argv[1]

    try:
        with open(data) as f:
            character = Character(json.load(f))
    except FileNotFoundError:
        print("File not found.")
        sys.exit()

    # Main loop
    while True:
        arg = getInput()
        if arg == "character":
            c = character.getCharacterShort()
            outstring = "\n    "
            outstring += c["name"] + ", " + c["alignment"] + " " + c["race"]
            for item in c["classes"]:
                outstring += "\n    " + item["name"]
                if item["archetypes"]:
                    outstring += " (" + ", ".join(item["archetypes"]) + ")"
                outstring += " - Lvl. " + str(item["level"])
            outstring += "\n    " + c["height"] + ", " + str(c["weight"]) + " lbs."
            outstring += "\n    " + c["description"] + "\n" + getAbilityString(character)
            print(outstring)
        elif arg == "abilities":
            print(getAbilityString(character))
        elif arg == "skills":
            print(getSkillString(character))
        elif arg == "items":
            print(getEquipmentString(character))
        elif arg == "attacks":
            print(getAttackString(character))
        elif arg == "feats":
            print(getFeatString(character))
        elif arg == "traits":
            print(getTraitString(character))
        elif arg == "special":
            print(getSpecialString(character))
        elif arg == "q" or arg == "quit":
            break

    if dataChanged:
        writeCharacter(character, data)
    sys.exit()
