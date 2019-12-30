#!/bin/python3
#
# pythfinder.py

import sys
import json

### CLASSES ###

class Character:
    def __init__(self, data = {}):
        if data is None:
            self.name = ""
            self.race = ""
            self.classes = []
            self.alignment = ""
            self.description = ""
            self.height = ""
            self.weight = 0
            self.age = 0
            self.languages = []
            self.abilities = {}
            self.hitDie = 0
            self.hp = {}
            self.baseAttackBonus = []
            self.special = []
            self.traits = []
            self.feats = []
            self.gold = 0
            self.equipment = []
            self.skills = []
            self.attacks = []
        else:
            keys = data.keys()
            self.name = data["name"] if "name" in keys else ""
            self.race = data["race"] if "race" in keys else ""
            self.classes = data["classes"] if "classes" in keys else []
            self.alignment = data["alignment"] if "alignment" in keys else ""
            self.description = data["description"] if "description" in keys else ""
            self.height = data["height"] if "height" in keys else ""
            self.weight = data["weight"] if "weight" in keys else 0
            self.age = data["age"] if "age" in keys else 0
            self.languages = data["languages"] if "languages" in keys else []
            self.abilities = data["abilities"] if "abilities" in keys else {}
            self.hitDie = data["hitDie"] if "hitDie" in keys else 0
            self.hp = data["hp"] if "hp" in keys else {}
            self.baseAttackBonus = data["baseAttackBonus"] if "baseAttackBonus" in keys else []
            self.special = data["special"] if "special" in keys else []
            self.traits = data["traits"] if "traits" in keys else []
            self.feats = data["feats"] if "feats" in keys else []
            self.gold = data["gold"] if "gold" in keys else 0
            self.equipment = data["equipment"] if "equipment" in keys else []
            self.skills = data["skills"] if "skills" in keys else []
            self.attacks = data["attacks"] if "attacks" in keys else []

    # Get the modifier for a given ability
    def getAbilityMod(self, ability):
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
        outstring = "\n    Items:\n\n    "
        for item in sorted(c.equipment, key = lambda i: i["name"]):
            total += item["weight"] * item["count"]
            outstring += item["name"] + " - Unit Weight: " + str(item["weight"]) + " lbs, Count: " + str(item["count"])
            if item["notes"]:
                outstring += ", Notes: " + item["notes"]
            if item["pack"]:
                outstring += " (pack item)"
                totalCamp += item["weight"] * item["count"]
            outstring += "\n    "
        outstring += "\n    Total weight: " + str(total) + "\n    Total weight (with camp set up): " + str(totalCamp)
        return outstring

    # Formatted string of feats
    def getFeatString(c):
        outstring = "\n    Feats:\n\n    "
        for feat in c.feats:
            outstring += feat["name"] + ":\n        " + feat["description"] + "\n        " + feat["notes"] + "\n    "
        return outstring

    # Formatted string of traits
    def getTraitString(c):
        outstring = "\n    Traits:\n\n    "
        for trait in c.traits:
            outstring += trait["name"] + ":\n        " + trait["description"] + "\n    "
        return outstring

    # Formatted string of skills
    def getSkillString(c):
        outstring = "\n    Skills:\n\n    "
        for skill in c.skills:
            total = 0
            outstring += skill["name"] + " - " + str(skill["rank"]) + " (ranks) "
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

    # Primary user input function
    def getInput():
        arg = ""
        args = ["character",
                "abilities",
                "skills",
                "items",
                "attacks",
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
        elif arg == "q" or arg == "quit":
            break

    if dataChanged:
        writeCharacter(character, data)
    sys.exit()
