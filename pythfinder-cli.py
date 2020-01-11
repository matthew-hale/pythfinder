#!/bin/python3
#
# pythfinder-cli.py

import pythfinder as pf
import json
import sys

# Formatted string of items
def getEquipmentString(c):
    total = 0
    totalCamp = 0
    outstring = "\n    Items:\n\n    Gold: {}\n\n    ".format(str(c.gold))
    for item in sorted(c.equipment, key = lambda i: i.name):
        total += item.weight * item.count
        outstring += "{} - Unit Weight: {} lbs, Count: {}".format(item.name,str(item.weight),str(item.count))
        if item.notes:
            outstring += ", Notes: {}".format(item.notes)
        if not item.pack:
            outstring += " (camp item)"
            totalCamp += item.weight * item.count
        outstring += "\n    "
    outstring += "\n    Total weight: {}\n    Total weight (with camp set up): {}".format(str(total),str(totalCamp))
    return outstring

# Formatted string of feats
def getFeatString(c):
    outstring = "\n    Feats:\n\n    "
    for feat in c.feats:
        outstring += "{}:\n        {}\n        {}\n    ".format(feat.name,feat.description,feat.notes)
    return outstring

# Formatted string of traits
def getTraitString(c):
    outstring = "\n    Traits:\n\n    "
    for trait in c.traits:
        outstring +=  "{}:\n        {}\n        {}\n    ".format(trait.name,trait.description,trait.notes)
    return outstring

# Formatted string of skills
def getSkillString(c):
    outstring = "\n    Skills:\n\n    "
    for skill in c.skills:
        total = 0
        if not skill.useUntrained:
            outstring += "*"
        outstring += skill.name 
        outstring += " - " + str(skill.rank) + " (ranks) "
        total += skill.rank
        if skill.isClass and skill.rank > 0:
            outstring += "+ 3 (class) "
            total += 3
        outstring += "+ " + str(c.getAbilityMod(skill.mod)) + " (mod: " + skill.mod + ") "
        total += c.getAbilityMod(skill.mod)
        if skill.misc > 0:
            total += skill.misc
            outstring += "+ " + str(skill.misc) + " (misc) "
        outstring += "= " + str(total) + "\n    "
    return outstring

# Formatted string of attacks
def getAttackString(c):
    outstring = "\n    Attacks:\n    "
    for attack in c.attacks:
        outstring += "\n    " + attack.weapon + " (" + attack.attackType + ")\n        "
        outstring += "Damage: " + attack.damage + " " + str(attack.critRoll)
        if attack.critRoll < 20:
            outstring += "-20"
        outstring += " x" + str(attack.critMulti) + " (" + ",".join(attack.damageType) + ") "
        if attack.range > 0:
            outstring += "\n        " + str(attack.range) + " ft. range increment"
        if attack.notes:
            outstring += "\n        " + attack.notes
        outstring += "\n    "
    return outstring

# Returns a formatted string of abilities
def getAbilityString(c):
    outstring = "\n    Abilities:\n\n    "
    for k, v in c.abilities.__dict__.items():
        modValue = c.getAbilityMod(k)
        if modValue >= 0:
            modString = "+" + str(modValue)
        else:
            modString = str(modValue)
        outstring += k + ": " + str(v) + " (" + modString + ")\n    "
    return outstring

# Formatted string of spells
def getSpellString(c):
    outstring = "\n    Spells:\n\n    "
    spells = c.getSortedSpells()
    spellLevels = spells.keys()
    for level in spellLevels:
        outstring += "Level {}:\n\n    ".format(level)
        for spell in spells[level]:
            outstring += "{}:\n        {}\n\n        Prepared: {}  - Cast: {}\n\n    ".format(
                spell.name,
                spell.description,
                spell.prepared,
                spell.cast
            )
    return outstring

# Formatted string of special abilities
def getSpecialString(c):
    outstring = "\n    Special:\n\n"
    for item in c.special:
        outstring += "    {}:\n    {}\n    {}\n\n".format(item.name,item.description,item.notes)
    return outstring

# Primary user input function
def getInput():
    arg = ""
    args = ["character",
            "abilities",
            "skills",
            "items",
            "attacks",
            "spells",
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
        character = pf.Character(json.load(f))
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
        for item in character.classes:
            cClass = item.getClassDict()
            outstring += "\n    " + cClass["name"]
            if cClass["archetypes"]:
                outstring += " (" + ", ".join(cClass["archetypes"]) + ")"
            outstring += " - Lvl. " + str(cClass["level"])
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
    elif arg == "spells":
        print(getSpellString(character))
    elif arg == "traits":
        print(getTraitString(character))
    elif arg == "special":
        print(getSpecialString(character))
    elif arg == "q" or arg == "quit":
        break

if dataChanged:
    pf.writeCharacter(character, data)
sys.exit()
