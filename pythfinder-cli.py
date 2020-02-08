#!/bin/python3
#
# pythfinder-cli.py

import argparse
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
        if item.pack:
            totalCamp += item.weight * item.count
        else:
            outstring += " (camp item)"
        outstring += "\n    "
    outstring += "\n    Total weight: {}\n    Total weight (with camp set up): {}".format(str(total),str(totalCamp))
    return outstring

# Formatted string of feats
def getFeatString(c):
    outstring = "\n    Feats:\n\n    "
    for feat in c.feats:
        outstring += "{}:\n        {}\n        {}\n\n    ".format(feat.name,feat.description,feat.notes)
    return outstring

# Formatted string of traits
def getTraitString(c):
    outstring = "\n    Traits:\n\n    "
    for trait in c.traits:
        outstring +=  "{}:\n        {}\n        {}\n\n    ".format(trait.name,trait.description,trait.notes)
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

# Formatted string of combat elements
def getCombatString(c):
    outstring = "    Combat:\n\n"
    outstring += "    HP: " + str(c.hp.current) + "/" + str(c.hp.max) + "\n\n"
    outstring += "    Attacks:\n"
    outstring += "    BAB: " + "/".join(map(str, c.baseAttackBonus)) + "\n"
    outstring += "    Melee mod: " + str(c.getAbilityMod("str")) + "\n"
    outstring += "    Ranged mod: " + str(c.getAbilityMod("dex")) + "\n"

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
    outstring += "\n    Armor:\n\n"

    for item in c.armor:
        outstring += "    {}: ({} armor)\n        AC Bonus: {}, Max Dex Bonus: {}, Armor Check Penalty: {}, Spell Failure Chance: {}%\n\n".format(item.name,item.type,item.acBonus,item.maxDexBonus,item.acPenalty,item.arcaneFailureChance)
    outstring += "    AC Calculation: 10 + Dex Bonus + AC Bonus\n\n"

    outstring += "    CMD: {}".format(str(sum([10, c.baseAttackBonus[0], c.getAbilityMod("str"), c.getAbilityMod("dex")]))) + "\n"
    outstring += "    CMB: {}".format(str(sum([c.baseAttackBonus[0], c.getAbilityMod("str")]))) + "\n\n"
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
    outstring = "\n    Spells:\n\n"
    spells = c.getSortedSpells()
    spellLevels = spells.keys()
    for level in spellLevels:
        outstring += "Level {}:\n\n".format(level)
        for spell in spells[level]:
            outstring += "    {}:\n        {}\n\n        Prepared: {}  - Cast: {}\n\n".format(
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

# Formatted string of saving throws
def getThrowString(c):
    outstring = "\n    Saving throws:\n\n"
    fort_total = sum([c.savingThrows["fortitude"].base, sum(c.savingThrows["fortitude"].misc), c.getAbilityMod("con")])
    ref_total = sum([c.savingThrows["reflex"].base, sum(c.savingThrows["reflex"].misc), c.getAbilityMod("dex")])
    will_total = sum([c.savingThrows["will"].base, sum(c.savingThrows["will"].misc), c.getAbilityMod("wis")])
    outstring += "    Fortitude: {}\n\n    Reflex: {}\n\n    Will: {}\n\n".format(str(fort_total), str(ref_total), str(will_total))
    return outstring

# Primary user input function
def getInput():
    arg = ""
    args = ["character",
            "abilities",
            "skills",
            "items",
            "combat",
            "spells",
            "special",
            "throws",
            "feats",
            "traits"]
    inputString = ""
    inputString += data + " (" + character.name + ") > "
    arg = input(inputString)
    while not arg in args:
        print("\n    Usage:\n\n" + "    {" + "|".join(args[:-1]) + "}\n")
        arg = input(inputString)
    return arg

# Any functions that intend to change character data will flag this as 
# True; at the end of execution, if this is true, data will be written 
# to the data argument given as input.
dataChanged = False

# Argument parsing
parser = argparse.ArgumentParser(description = "pathfinder 1E character sheet")

# Subparsers for subcommands
subparsers = parser.add_subparsers(help = "subcommand",
                                   dest = "subcommand_name")

# List: read values
parser_list = subparsers.add_parser("list",
                                    help = "list character details",
                                    aliases = ["ls"])
parser_list.add_argument("target",
                         choices = ["abilities",
                                    "character",
                                    "combat",
                                    "feats",
                                    "items",
                                    "skills",
                                    "special",
                                    "spells",
                                    "throws",
                                    "traits"],
                         help = "list target",
                         type = str
                         )

# Add: create a new entry in the character
parser_add = subparsers.add_parser("add",
                                    help = "add entry to character")
parser_add.add_argument("target",
                        choices = ["feat",
                                   "trait",
                                   "special",
                                   "item",
                                   "attack",
                                   "armor",
                                   "spell"],
                        help = "add target",
                        type = str)
parser_add.add_argument("-n","--name",
                        dest = "name",
                        help = "name of entry",
                        type = str)
parser_add.add_argument("-d","--description",
                        dest = "description",
                        help = "description of entry",
                        type = str)
parser_add.add_argument("-o","--notes",
                        dest = "notes",
                        help = "entry notes",
                        type = str)

# File path (positional)
parser.add_argument("file",
                    metavar = "filepath",
                    type = str,
                    help = "path to character sheet file")

args = parser.parse_args()

try:
    with open(args.file) as f:
        character = pf.Character(json.load(f))
except FileNotFoundError:
    print("File not found.")
    sys.exit()

# Main execution
subcommand = args.subcommand_name
target = args.target
if subcommand == "list":
    if target == "character":
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
    elif target == "abilities":
        print(getAbilityString(character))
    elif target == "skills":
        print(getSkillString(character))
    elif target == "items":
        print(getEquipmentString(character))
    elif target == "combat":
        print(getCombatString(character))
    elif target == "feats":
        print(getFeatString(character))
    elif target == "throws":
        print(getThrowString(character))
    elif target == "spells":
        print(getSpellString(character))
    elif target == "traits":
        print(getTraitString(character))
    elif target == "special":
        print(getSpecialString(character))
elif subcommand == "add":
    if target == "feat":
        new_name = args.name if args.name != None else ""
        new_description = args.description if args.description != None else ""
        new_notes = args.notes if args.notes != None else ""
        new_feat = pf.CharacterBasicItem.CharacterBasicItem(name = new_name,
                                         description = new_description,
                                         notes = new_notes)
        character.feats.append(new_feat)
        dataChanged = True
        print("\n    Feat added\n")
    elif target == "trait":
        new_name = args.name if args.name != None else ""
        new_description = args.description if args.description != None else ""
        new_notes = args.notes if args.notes != None else ""
        new_trait = pf.CharacterBasicItem.CharacterBasicItem(name = new_name,
                                         description = new_description,
                                         notes = new_notes)
        character.traits.append(new_trait)
        dataChanged = True
        print("\n    Trait added\n")
    elif target == "special":
        new_name = args.name if args.name != None else ""
        new_description = args.description if args.description != None else ""
        new_notes = args.notes if args.notes != None else ""
        new_special = pf.CharacterBasicItem.CharacterBasicItem(name = new_name,
                                         description = new_description,
                                         notes = new_notes)
        character.special.append(new_special)
        dataChanged = True
        print("\n    Special added\n")
    """
    elif target == "item":
    elif target == "attack":
    elif target == "armor":
    elif target == "spell":
    """

# Write check
if dataChanged:
    pf.writeCharacter(character, args.file)
    print("\n    Changes saved to " + args.file + "\n")
sys.exit()
