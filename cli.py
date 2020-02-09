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
                         metavar = "target",
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
                        metavar = "target",
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
                        default = "",
                        help = "name of entry",
                        type = str)
parser_add.add_argument("-d","--description",
                        dest = "description",
                        default = "",
                        help = "description of entry",
                        type = str)
parser_add.add_argument("-o","--notes",
                        dest = "notes",
                        default = "",
                        help = "entry notes",
                        type = str)
parser_add.add_argument("-k", "--pack",
                        dest = "pack",
                        action = "store_true",
                        help = "(items) pack item if true")
parser_add.add_argument("-c", "--count",
                        dest = "count",
                        default = 0,
                        help = "(items) number of items",
                        type = int)
parser_add.add_argument("-w", "--weight",
                        dest = "weight",
                        default = 0.0,
                        help = "(items) item unit weight",
                        type = float)
parser_add.add_argument("--weapon",
                        dest = "weapon",
                        default = "",
                        help = "(attack) name of weapon",
                        type = str)
parser_add.add_argument("--attackType",
                        dest = "attackType",
                        choices = ["melee","ranged"],
                        help = "(attack) type of attack (melee, ranged)",
                        type = str)
parser_add.add_argument("--damageType",
                        dest = "damageType",
                        choices = ["S", "P", "B"],
                        nargs = "*",
                        default = [""],
                        help = "(attack) type of damage dealt",
                        type = str)
parser_add.add_argument("--damage",
                        dest = "damage",
                        default = "",
                        help = "(attack) damage dealt (e.g. 1d6, 2d8)",
                        type = str)
parser_add.add_argument("--critRoll",
                        dest = "critRoll",
                        default = 20,
                        help = "(attack) the minimum roll to threaten a critical strike",
                        type = int)
parser_add.add_argument("--critMulti",
                        dest = "critMulti",
                        default = 2,
                        help = "(attack) the damage multiplier on critical strike",
                        type = int)
parser_add.add_argument("--range",
                        dest = "range",
                        default = 0,
                        help = "(attack) range increment",
                        type = int)
parser_add.add_argument("--acBonus",
                        dest = "acBonus",
                        default = 0,
                        help = "bonus to AC",
                        type = int)
parser_add.add_argument("--acPenalty",
                        dest = "acPenalty",
                        default = 0,
                        help = "armor check penalty",
                        type = int)
parser_add.add_argument("--maxDexBonus",
                        dest = "maxDexBonus",
                        default = 0,
                        help = "max dexterity bonus",
                        type = int)
parser_add.add_argument("--type",
                        dest = "type",
                        choices = ["light", "medium", "heavy"],
                        default = "",
                        help = "armor type",
                        type = str)
parser_add.add_argument("--arcaneFailureChance",
                        dest = "arcaneFailureChance",
                        default = 0,
                        help = "percentage chance that arcane spellcasting fails",
                        type = int)
parser_add.add_argument("--cast",
                        dest = "cast",
                        default = 0,
                        help = "number of times cast",
                        type = int)
parser_add.add_argument("--prepared",
                        dest = "prepared",
                        default = 0,
                        help = "number of spells prepared",
                        type = int)
parser_add.add_argument("--level",
                        dest = "level",
                        default = 0,
                        help = "spell level",
                        type = int)

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
        new_feat = character.addFeat(name = args.name,
                                     description = args.description,
                                     notes = args.notes)
        if new_feat.name == args.name and new_feat.description == args.description and new_feat.notes == args.notes:
            dataChanged = True
            print(getFeatString(character))
            print("\n    Feat added\n")
        else:
            dataChanged = False
            print("\n    Something went wrong; new feat not added properly; aborting\n")
    elif target == "trait":
        new_trait = character.addTrait(name = args.name,
                                     description = args.description,
                                     notes = args.notes)
        if new_trait.name == args.name and new_trait.description == args.description and new_trait.notes == args.notes:
            dataChanged = True
            print(getFeatString(character))
            print("\n    Trait added\n")
        else:
            dataChanged = False
            print("\n    Something went wrong; new trait not added properly; aborting\n")
    elif target == "special":
        new_name = args.name
        new_description = args.description
        new_notes = args.notes
        new_special = pf.CharacterBasicItem.CharacterBasicItem(name = new_name,
                                                               description = new_description,
                                                               notes = new_notes)
        character.special.append(new_special)
        dataChanged = True
        print("\n    Special added\n")
    elif target == "item":
        new_name = args.name
        new_weight = args.weight
        new_count = args.count
        new_pack = args.pack
        new_notes = args.notes
        new_item = pf.CharacterEquipment.CharacterEquipment(name = new_name,
                                                            weight = new_weight,
                                                            count = new_count,
                                                            pack = new_pack,
                                                            notes = new_notes)
        character.equipment.append(new_item)
        dataChanged = True
        print("\n    Item added\n")
    elif target == "attack":
        new_weapon = args.weapon
        new_attackType = args.attackType
        new_damageType = args.damageType
        new_damage = args.damage
        new_critRoll = args.critRoll
        new_critMulti = args.critMulti
        new_range = args.range
        new_notes = args.notes
        new_attack = pf.CharacterAttack.CharacterAttack(weapon = new_weapon,
                                                        attackType = new_attackType,
                                                        damageType = new_damageType,
                                                        damage = new_damage,
                                                        critRoll = new_critRoll,
                                                        critMulti = new_critMulti,
                                                        range_ = new_range,
                                                        notes = new_notes)
        character.attacks.append(new_attack)
        dataChanged = True
        print("\n    Attack added\n")
    elif target == "armor":
        new_name = args.name
        new_acBonus = args.acBonus
        new_acPenalty = args.acPenalty
        new_maxDexBonus = args.maxDexBonus
        new_arcaneFailureChance = args.arcaneFailureChance
        new_type = args.type
        new_armor = pf.CharacterArmor.CharacterArmor(name = new_name,
                                                     acBonus = new_acBonus,
                                                     acPenalty = new_acPenalty,
                                                     maxDexBonus = new_maxDexBonus,
                                                     arcaneFailureChance = new_arcaneFailureChance,
                                                     type_ = new_type)
        character.armor.append(new_armor)
        dataChanged = True
        print("\n    Armor added\n")
    elif target == "spell":
        new_name = args.name
        new_level = args.level
        new_description = args.description
        new_prepared = args.prepared
        new_cast = args.cast
        new_spell = pf.CharacterSpell.CharacterSpell(name = new_name,
                                                     level = new_level,
                                                     description = new_description,
                                                     prepared = new_prepared,
                                                     cast = new_cast)
        character.spells.append(new_spell)
        dataChanged = True
        print("\n    Spell added\n")

# Write check
if dataChanged:
    pf.writeCharacter(character, args.file)
    print("    Changes saved to " + args.file + "\n")
