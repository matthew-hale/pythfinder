#!/bin/python3
#
# carrion_crown_fighter.py

import sys
import json

# Paths to data file (for demo purposes)
dataPath = "/home/matt/pathfinder/data/qofin-parora.json"

with open(dataPath) as f:
    character = json.load(f)

### FUNCTIONS ###

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

# Formatted string of abilities
def getAbilityString():
    outstring = ""
    for k, v in character["abilities"].items():
        outstring += k + ": " + str(v) + "\n"
    # Slicing off the last newline
    return outstring[0:-1]

def getSkillString():
    outstring = ""
    for skill in character["skills"]:
        outstring += skill["name"] + " - Ranks: " + str(skill["rank"])
        if skill["isClass"]:
            outstring += " (class), "
        else:
            outstring += ", "
        outstring += "Mod: " + skill["mod"] + " (" + str(getAbilityMod(character["abilities"][skill["mod"]])) + ")\n"
    # Slicing off the last newline
    return outstring[0:-1]

# Formatted string of items
def getEquipmentString():
    outstring=""
    for item in character["equipment"]:
        outstring += item["name"] + " - Unit Weight: " + str(item["weight"]) + " lbs, Count: " + str(item["count"])
        if item["notes"]:
            outstring += ", Notes: " + item["notes"]
        if item["pack"]:
            outstring += " (pack item)"
        outstring += "\n"
    # Slicing off the last newline
    return outstring[0:-1]
### MAIN ###

# Check for argument
if not (len(sys.argv) >= 2):
    print("Usage: " + sys.argv[0] + " {character|abilities|skills|items|weapons|feats|traits}")
    sys.exit()

# Argument options
if sys.argv[1] == "character":
    print(character["name"] + ", the " + character["race"] + " " + character["class"] + ". Level: " + str(character["level"]))
    print(character["height"] + ", " + character["weight"] + "\n" + character["description"] + "\n")
    print("Abilities:\n" + getAbilityString())
elif sys.argv[1] == "abilities":
    print("Abilities:\n" + getAbilityString())
elif sys.argv[1] == "skills":
    print("Skills:\n" + getSkillString())
elif sys.argv[1] == "items":
    print("Items:\n" + getEquipmentString())
elif sys.argv[1] == "attacks":
    print("attacks")
elif sys.argv[1] == "feats":
    print("feats")
elif sys.argv[1] == "traits":
    print("traits")
else:
    print("Usage: " + sys.argv[0] + " {character|abilities|skills|items|attacks|feats|traits}")
    sys.exit()
