#!/bin/python3
#
# carrion_crown_fighter.py

import sys
import json

# Paths to data file (for demo purposes)
dataPath = "/home/matt/pathfinder/data/qofin-parora.json"

# Any functions that intend to change character data will flag this as True; at 
# the end of the loop, if this is true, data will be written to the data 
# argument given as input.
dataChanged = False

### FUNCTIONS ###

# Read the json data from path
def readCharacter(path):
    with open(path) as f:
        character = json.load(f)
    return character

# Write the given character data to the file in path
def writeCharacter(character, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(character, f, indent=4)

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
    inputString += data + " > "
    arg = input(inputString)
    while not arg in args:
        print("\n    Usage:\n\n" + "    {" + "|".join(args[:-1]) + "}\n")
        arg = input(inputString)
    return arg

# Get the modifier for a given ability
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

# Formatted string of basic character info, including abilities
def getCharacterString():
    outstring = "\n    " + character["name"] + ", the " + character["race"] + " " + character["class"] + ". Level: " + str(character["level"])
    outstring += "\n    " + character["height"] + ", " + character["weight"] + "\n    " + character["description"] + "\n"
    outstring += getAbilityString()
    return outstring

# Formatted string of abilities
def getAbilityString():
    outstring = "\n    Abilities:\n\n    "
    for k, v in character["abilities"].items():
        outstring += k + ": " + str(v) + "\n    "
    return outstring

def getSkillString():
    outstring = "\n    Skills:\n\n    "
    for skill in character["skills"]:
        outstring += skill["name"] + " - Ranks: " + str(skill["rank"])
        if skill["isClass"]:
            outstring += " (class), "
        else:
            outstring += ", "
        outstring += "Mod: " + skill["mod"] + " (" + str(getAbilityMod(character["abilities"][skill["mod"]])) + ")\n    "
    return outstring

# Formatted string of items
def getEquipmentString():
    outstring="\n    Items:\n\n    "
    for item in character["equipment"]:
        outstring += item["name"] + " - Unit Weight: " + str(item["weight"]) + " lbs, Count: " + str(item["count"])
        if item["notes"]:
            outstring += ", Notes: " + item["notes"]
        if item["pack"]:
            outstring += " (pack item)"
        outstring += "\n    "
    return outstring


### MAIN ###

# Check for argument
if not (len(sys.argv) >= 2):
    print("Usage: " + sys.argv[0] + " <data_path>")
    sys.exit()

data = sys.argv[1]

# Will be changed to data in future
character = readCharacter(dataPath)

# Main loop
while True:
    arg = getInput()
    if arg == "character":
        print(getCharacterString())
    elif arg == "abilities":
        print(getAbilityString())
    elif arg == "skills":
        print(getSkillString())
    elif arg == "items":
        print(getEquipmentString())
    elif arg == "attacks":
        print("attacks")
    elif arg == "feats":
        print("feats")
    elif arg == "traits":
        print("traits")
    elif arg == "q" or arg == "quit":
        break

if dataChanged:
    writeCharacter(character, data)
sys.exit()
