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
    outstring = "\n    Skills:\n"
    for skill in c.skills:
        if skill.useUntrained == False:
            outstring += "\n   *"
        else:
            outstring += "\n    "
        total = skill.get_total_value(c)
        outstring += "{}: {}".format(skill.name, total)
        if skill.rank == 0:
            outstring += " - (untrained)"
    outstring += "\n"
    return outstring

# Formatted string of combat elements
def getCombatString(c):
    strength_mod = c.getAbilityMod(c.abilities.get_total_value("str"))
    dexterity_mod = c.getAbilityMod(c.abilities.get_total_value("dex"))
    outstring = "    Combat:\n\n"
    outstring += "    HP: " + str(c.hp.current) + "/" + str(c.hp.max) + "\n\n"
    outstring += "    Attacks:\n"
    outstring += "    BAB: " + "/".join(map(str, c.baseAttackBonus)) + "\n"
    outstring += "    Strength mod: {}\n".format(strength_mod)
    outstring += "    Dexterity mod: {}\n".format(dexterity_mod)

    for attack in c.attacks:
        outstring += "\n    " + attack.name + " (" + attack.attackType + ")\n        "
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

    outstring += "    CMD: {}\n".format(str(sum([10,
                                                 c.baseAttackBonus[0],
                                                 strength_mod,
                                                 dexterity_mod])))
    outstring += "    CMB: {}\n".format(str(sum([c.baseAttackBonus[0],
                                                 strength_mod])))
    return outstring

# Returns a formatted string of abilities
def getAbilityString(c):
    outstring = "\n    Abilities:"
    for ability in c.abilities.__dict__.keys():
        base_score_value = c.abilities.get_base_value(ability)
        base_mod_value = c.getAbilityMod(base_score_value)
        temp_score_value = c.abilities.get_total_value(ability)
        temp_mod_value = c.getAbilityMod(temp_score_value)
        if base_mod_value >= 0:
            base_mod_string = "+" + str(base_mod_value)
        else:
            base_mod_string = str(base_mod_value)
        if temp_mod_value >= 0:
            temp_mod_string = "+" + str(temp_mod_value)
        else:
            temp_mod_string = str(temp_mod_value)
        outstring += "\n\n    {}:  {} ({}) - temp: {} ({})".format(
            ability,
            base_score_value,
            base_mod_string,
            temp_score_value,
            temp_mod_value
        )
    outstring += "\n"
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
    fort_total = sum([c.savingThrows["fortitude"].base, sum(c.savingThrows["fortitude"].misc), c.getAbilityMod(c.abilities.get_total_value("con"))])
    ref_total = sum([c.savingThrows["reflex"].base, sum(c.savingThrows["reflex"].misc), c.getAbilityMod(c.abilities.get_total_value("dex"))])
    will_total = sum([c.savingThrows["will"].base, sum(c.savingThrows["will"].misc), c.getAbilityMod(c.abilities.get_total_value("wis"))])
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

# Edit: modify the properties of the character
parser_edit = subparsers.add_parser("edit",
                                    help = "edit character properties")
parser_edit.add_argument("target",
                         metavar = "target",
                         choices = ["ability",
                                    "skill",
                                    "item",
                                    "attack",
                                    "feat",
                                    "trait",
                                    "special",
                                    "spell"],
                         help = "edit target",
                         type = str)
parser_edit.add_argument("-n", "--name",
                         dest = "name",
                         default = "",
                         help = "name of target; primary key",
                         type = str)
parser_edit.add_argument("-d", "--description",
                         dest = "description",
                         default = "",
                         help = "new description of target",
                         type = str)
parser_edit.add_argument("--new-name",
                         dest = "new_name",
                         default = "",
                         help = "new name of target",
                         type = str)
parser_edit.add_argument("-o", "--notes",
                         dest = "notes",
                         default = "",
                         help = "new notes of target",
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
        new_feat = character.addFeat(name = args.name,
                                     description = args.description,
                                     notes = args.notes)
        if new_feat.name == args.name and \
           new_feat.description == args.description and \
           new_feat.notes == args.notes:
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
        if new_trait.name == args.name and \
           new_trait.description == args.description and \
           new_trait.notes == args.notes:
            dataChanged = True
            print(getTraitString(character))
            print("\n    Trait added\n")
        else:
            dataChanged = False
            print("\n    Something went wrong; new trait not added properly; aborting\n")
    elif target == "special":
        new_special = character.addSpecial(name = args.name,
                                     description = args.description,
                                     notes = args.notes)
        if new_special.name == args.name and \
           new_special.description == args.description and \
           new_special.notes == args.notes:
            dataChanged = True
            print(getSpecialString(character))
            print("\n    Special added\n")
        else:
            dataChanged = False
            print("\n    Something went wrong; new special ability not added properly; aborting\n")
    elif target == "item":
        new_item = character.addItem(name = args.name,
                                     weight = args.weight,
                                     count = args.count,
                                     pack = args.pack,
                                     notes = args.notes)
        if new_item.name == args.name and \
           new_item.weight == args.weight and \
           new_item.count == args.count and \
           new_item.pack == args.pack and \
           new_item.notes == args.notes:
            dataChanged = True
            print(getEquipmentString(character))
            print("\n    Item added\n")
        else:
            dataChanged = False
            print("\n    Something went wrong; new item not added properly; aborting\n")
    elif target == "attack":
        new_attack = character.addAttack(name = args.name,
                                         attackType = args.attackType,
                                         damageType = args.damageType,
                                         damage = args.damage,
                                         critRoll = args.critRoll,
                                         critMulti = args.critMulti,
                                         range_ = args.range)
        if new_attack.name == args.name and \
           new_attack.attackType == args.attackType and \
           new_attack.damageType == args.damageType and \
           new_attack.damage == args.damage and \
           new_attack.critRoll == args.critRoll and \
           new_attack.critMulti == args.critMulti and \
           new_attack.range_ == args.range:
            dataChanged = True
            print(getCombatString(character))
            print("\n    Attack added\n")
        else:
            dataChanged = False
            print("\n    Something went wrong; new attack not added properly; aborting\n")
    elif target == "armor":
        new_armor = character.addArmor(name = args.name,
                                       acBonus = args.acBonus,
                                       acPenalty = args.acPenalty,
                                       maxDexBonus = args.maxDexBonus,
                                       arcaneFailureChance = args.arcaneFailureChance,
                                       type_ = args.type)
        if new_armor.name == args.name and \
           new_armor.acBonus == args.acBonus and \
           new_armor.acPenalty == args.acPenalty and \
           new_armor.maxDexBonus == args.maxDexBonus and \
           new_armor.arcaneFailureChance == args.arcaneFailureChance:
            dataChanged = True
            print(getCombatString(character))
            print("\n    Armor added\n")
        else:
            dataChanged = False
            print("\n    Something went wrong; new armor not added properly; aborting\n")
    elif target == "spell":
        new_spell = character.addSpell(name = args.name,
                                       level = args.level,
                                       description = args.description,
                                       prepared = args.prepared,
                                       cast = args.cast)
        if new_spell.name == args.name and \
           new_spell.level == args.level and \
           new_spell.description == args.description and \
           new_spell.prepared == args.prepared and \
           new_spell.cast == args.cast:
            dataChanged = True
            print(getSpellString(character))
            print("\n    Spell added\n")
        else:
            dataChanged = False
            print("\n    Something went wrong; new spell not added properly; aborting\n")
elif subcommand == "edit":
    if target == "feat":
        if not args.description and not args.new_name and not args.notes:
            print("\n    No new fields specified; nothing to do\n")
        else:
            # Keeping track of what the user wants updated
            updates = [False, False, False]
            if args.new_name:
                updates[0] = True
            if args.description:
                updates[1] = True
            if args.notes:
                updates[2] = True
            updated_feat = character.updateFeat(name = args.name,
                                                new_name = args.new_name,
                                                description = args.description,
                                                notes = args.notes)
            # If updateFeat() returned "None," it means that there was 
            # no matching feat with the name given
            if updated_feat == None:
                print("\n    No matching feat with the name given; aborting\n")
            else:
            # Seeing if updates were applied successfully, testing only 
            # those values that were true above
                success = True
                for i in range(3):
                    if updates[i] == True:
                        # Name
                        if i == 0:
                            if updated_feat.name != args.new_name:
                                success = False
                        # Description
                        if i == 1:
                            if updated_feat.description != args.description:
                                success = False
                        # Notes
                        if i == 2:
                            if updated_feat.notes != args.notes:
                                success = False
                if success:
                    dataChanged = True
                    print(getFeatString(character))
                    print("\n    Feat updated\n")
                else:
                    print("\n    Something went wrong; feat not updated properly; aborting\n")

# Write check
if dataChanged:
    pf.writeCharacter(character, args.file)
    print("    Changes saved to " + args.file + "\n")
