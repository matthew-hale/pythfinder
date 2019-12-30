#!/bin/python3
#
# pythfinder.py

import sys
import json

### FUNCTIONS ###

# Read the json data from path
def readCharacter(path):
    with open(path) as f:
        character = json.load(f)
    return character

# Read in json data from a string
def readCharacterString(j):
    return json.loads(j)

# Write the given character data to the file in path
def writeCharacter(character, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(character, f, indent=4)

# Get the modifier for a given ability value
def getAbilityMod(ability):
    if ability == 1:
        return -5
    elif ability in [2, 3]:
        return -4
    elif ability in [4, 5]:
        return -3
    elif ability in [6, 7]:
        return -2
    elif ability in [8, 9]:
        return -1
    elif ability in [10, 11]:
        return 0
    elif ability in [12, 13]:
        return 1
    elif ability in [14, 15]:
        return 2
    elif ability in [16, 17]:
        return 3
    elif ability in [18, 19]:
        return 4
    elif ability in [20, 21]:
        return 5
    elif ability in [22, 23]:
        return 6
    elif ability in [24, 25]:
        return 7
    elif ability in [26, 27]:
        return 8
    elif ability in [28, 29]:
        return 9
    elif ability in [30, 31]:
        return 10
    else:
        raise ValueError("getAbilityMod: ability must be within range of 1-31, inclusive.")

# Returns the given character object, without long elements like skills, feats, 
# traits, spells, and equipment.
def getCharacterShort(data):
    output = {}
    output["name"] = data["name"]
    output["race"] = data["race"]
    output["classes"] = data["classes"]
    output["alignment"] = data["alignment"]
    output["description"] = data["description"]
    output["height"] = data["height"]
    output["weight"] = data["weight"]
    output["abilities"] = data["abilities"]
    output["hp"] = data["hp"]
    return output

# Returns ability valies from given character object
# If ability is specified, returns that ability's value directly
def getAbility(data, ability=None):
    if ability:
        if not ability.lower() in ["str", "dex", "con", "int", "wis", "cha"]:
            raise ValueError('getAbility: ability must be one of ["str", "dex", "con", "int", "wis", "cha"]')
        return data["abilities"][ability.lower()]
    else:
        return data["abilities"]

# Formatted string of abilities
def getAbilityString(c):
    outstring = "\n    Abilities:\n\n    "
    for k, v in c["abilities"].items():
        modValue = getAbilityMod(v)
        if modValue >= 0:
            modString = "+" + str(modValue)
        else:
            modString = str(modValue)
        outstring += k + ": " + str(v) + " (" + modString + ")\n    "
    return outstring

# Formatted string of skills
def getSkillString(c):
    outstring = "\n    Skills:\n\n    "
    for skill in c["skills"]:
        total = 0
        outstring += skill["name"] + " - " + str(skill["rank"]) + " (ranks) "
        total += skill["rank"]
        if skill["isClass"] and skill["rank"] > 0:
            outstring += "+ 3 (class) "
            total += 3
        outstring += "+ " + str(getAbilityMod(c["abilities"][skill["mod"]])) + " (mod: " + skill["mod"] + ") "
        total += getAbilityMod(c["abilities"][skill["mod"]])
        if skill["misc"] > 0:
            total += skill["misc"]
            outstring += "+ " + str(skill["misc"]) + " (misc) "
        outstring += "= " + str(total) + "\n    "
    return outstring

# Formatted string of items
def getEquipmentString(c):
    total = 0
    totalCamp = 0
    outstring = "\n    Items:\n\n    "
    for item in sorted(c["equipment"], key = lambda i: i["name"]):
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
    for feat in c["feats"]:
        outstring += feat["name"] + ":\n        " + feat["description"] + "\n        " + feat["notes"] + "\n    "
    return outstring

# Formatted string of traits
def getTraitString(c):
    outstring = "\n    Traits:\n\n    "
    for trait in c["traits"]:
        outstring += trait["name"] + ":\n        " + trait["description"] + "\n    "
    return outstring

# Formatted string of attacks
def getAttackString(c):
    outstring = "\n    Attacks:\n"
    for attack in c["attacks"]:
        outstring += "\n    " + attack["weapon"] + " (" + attack["attackType"] + ")\n        "
        outstring += "Damage: " + attack["damage"] + " " + str(attack["critRoll"])
        if attack["critRoll"] < 20:
            outstring += "-20"
        outstring += " x" + str(attack["critMulti"]) + " (" + ",".join(attack["damageType"]) + ") "
        if attack["range"] > 0:
            outstring += "\n        " + str(attack["range"]) + " ft. range increment"
        if attack["notes"]:
            outstring += "\n        " + attack["notes"]
        outstring += "\n"
    return outstring

### MAIN ###

if __name__ == "__main__":
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
        inputString += data + " (" + character["name"] + ") > "
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

    character = readCharacter(data)

    # Main loop
    while True:
        arg = getInput()
        if arg == "character":
            c = getCharacterShort(character)
            outstring = "\n    "
            outstring += c["name"] + ", " + c["alignment"] + " " + c["race"]
            for item in c["classes"]:
                outstring += "\n    " + item["class"] + " - Lvl. " + str(item["level"])
            outstring += "\n    " + c["height"] + ", " + str(c["weight"]) + " lbs."
            outstring += "\n    " + c["description"] + "\n"
            outstring += getAbilityString(character)
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
