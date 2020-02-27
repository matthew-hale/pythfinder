#!/bin/python3
#
# pythfinder-cli.py

import argparse
import pythfinder as pf
import json
import sys

# Special function for argparse and boolean arguments
def t_or_f(arg):
    ua = str(arg).upper()
    print("function: " + ua)
    value = None
    if "FALSE".startswith(ua):
        value = False
    elif "TRUE".startswith(ua):
        value = True
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
    return value

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
            totalCamp += item["weight"] * item["count"]
        else:
            outstring += " (camp item)"
        outstring += "\n    "
    outstring += "\n    Total weight: {}\n    Total weight (with camp set up): {}".format(str(total),str(totalCamp))
    return outstring

# Formatted string of feats
def getFeatString(c):
    outstring = "\n    Feats:\n\n    "
    for feat in c.feats:
        outstring += "{}:\n        {}\n        {}\n\n    ".format(feat["name"],feat["description"],feat["notes"])
    return outstring

# Formatted string of traits
def getTraitString(c):
    outstring = "\n    Traits:\n\n    "
    for trait in c.traits:
        outstring +=  "{}:\n        {}\n        {}\n\n    ".format(trait["name"],trait["description"],trait["notes"])
    return outstring

# Formatted string of skills
def getSkillString(c):
    outstring = "\n    Skills:\n"
    for skill in c.skills.keys():
        if c.skills[skill]["isClass"]:
            outstring += "\nc"
        else:
            outstring += "\n "
        if c.skills[skill]["useUntrained"] == False:
            outstring += "  *"
        else:
            outstring += "   "
        total = c.get_skill_value(skill)
        outstring += "{}: {}".format(skill, total)
        if c.skills[skill]["rank"] == 0:
            outstring += " - (untrained)"
    outstring += "\n"
    return outstring

# Formatted string of combat elements
def getCombatString(c):
    strength_mod = c.getAbilityMod(c.get_total_ability_value("str"))
    dexterity_mod = c.getAbilityMod(c.get_total_ability_value("dex"))
    outstring = "    Combat:\n\n"
    outstring += "    HP: " + str(c.hp["current"]) + "/" + str(c.hp["max"]) + "\n\n"
    outstring += "    Attacks:\n"
    outstring += "    BAB: " + "/".join(map(str, c.baseAttackBonus)) + "\n"
    outstring += "    Strength mod: {}\n".format(strength_mod)
    outstring += "    Dexterity mod: {}\n".format(dexterity_mod)

    for attack in c.attacks:
        outstring += "\n    " + attack.name + " (" + attack.attackType + ")\n        "
        outstring += "Damage: " + attack.damage + " " + str(attack.critRoll)
        if attack.critRoll < 20:
            outstring += "-20"
        outstring += " x" + str(attack.critMulti) + " (" + attack.damageType + ") "
        if attack.range > 0:
            outstring += "\n        " + str(attack.range) + " ft. range increment"
        if attack.notes:
            outstring += "\n        " + attack.notes
        outstring += "\n    "
    outstring += "\n    Armor:\n\n"

    for item in c.armor:
        outstring += "    {}: ({} armor)\n        AC Bonus: {}, Max Dex Bonus: {}, Armor Check Penalty: {}, Spell Failure Chance: {}%\n\n".format(item["name"],item["type"],item["acBonus"],item["maxDexBonus"],item["acPenalty"],item["arcaneFailureChance"])
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
    for ability in c.abilities.keys():
        base_score_value = c.get_base_ability_value(ability)
        base_mod_value = c.getAbilityMod(base_score_value)
        temp_score_value = c.get_total_ability_value(ability)
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
            temp_mod_string
        )
    outstring += "\n"
    return outstring

# Formatted string of spells
def getSpellString(c):
    outstring = "\n    Spells:\n\n"
    spells = c.get_sorted_spells()
    spellLevels = spells.keys()
    for level in spellLevels:
        outstring += "Level {}:\n\n".format(level)
        for spell in spells[level]:
            outstring += "    {}:\n        {}\n\n        Prepared: {}  - Cast: {}\n\n".format(
                spell["name"],
                spell["description"],
                spell["prepared"],
                spell["cast"]
            )
    return outstring

# Formatted string of special abilities
def getSpecialString(c):
    outstring = "\n    Special:\n\n"
    for item in c.special:
        outstring += "    {}:\n    {}\n    {}\n\n".format(item["name"],item["description"],item["notes"])
    return outstring

# Formatted string of saving throws
def getThrowString(c):
    outstring = "\n    Saving throws:\n\n"
    fort_total = sum([c.saving_throws["fortitude"]["base"], sum(c.saving_throws["fortitude"]["misc"]), c.getAbilityMod(c.get_total_ability_value("con"))])
    ref_total = sum([c.saving_throws["reflex"]["base"], sum(c.saving_throws["reflex"]["misc"]), c.getAbilityMod(c.get_total_ability_value("dex"))])
    will_total = sum([c.saving_throws["will"]["base"], sum(c.saving_throws["will"]["misc"]), c.getAbilityMod(c.get_total_ability_value("wis"))])
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
                                    help = "list character details")
list_target_choices = ["abilities",
                       "character",
                       "combat",
                       "feats",
                       "items",
                       "skills",
                       "special",
                       "spells",
                       "throws",
                       "traits"]
parser_list.add_argument("target",
                         metavar = "target",
                         choices = list_target_choices,
                         help = "list target; choose from " + str(list_target_choices),
                         type = str
                         )

# Add: create a new entry in the character
parser_add = subparsers.add_parser("add",
                                    help = "add entry to character")
add_target_choices = ["feat",
                      "trait",
                      "special",
                      "item",
                      "attack",
                      "armor",
                      "spell"]
parser_add.add_argument("target",
                        metavar = "target",
                        choices = add_target_choices,
                        help = "add target; choose from " + str(add_target_choices),
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
edit_target_choices = ["ability",
                       "skill",
                       "item",
                       "attack",
                       "feat",
                       "trait",
                       "special",
                       "spell"]
parser_edit.add_argument("target",
                         metavar = "target",
                         choices = edit_target_choices,
                         help = "edit target; choose from " + str(edit_target_choices),
                         type = str)
parser_edit.add_argument("-n", "--name",
                         dest = "name",
                         required = True,
                         help = "name of target; primary key",
                         type = str)
parser_edit.add_argument("-d", "--description",
                         dest = "description",
                         help = "new description of target",
                         type = str)
parser_edit.add_argument("--new-name",
                         dest = "new_name",
                         help = "new name of target",
                         type = str)
parser_edit.add_argument("-o", "--notes",
                         dest = "notes",
                         help = "new notes of target",
                         type = str)
parser_edit.add_argument("-w", "--weight",
                         dest = "weight",
                         help = "new weight of target",
                         type = float)
parser_edit.add_argument("-c", "--count",
                         dest = "count",
                         default = None,
                         help = "new count of target",
                         type = int)
parser_edit.add_argument("-k", "--pack",
                         dest = "pack",
                         help = "whether or not target is a pack item",
                         type = t_or_f)
parser_edit.add_argument("--isClass",
                         dest = "isClass",
                         help = "whether or not skill is treated as a class skill",
                         type = t_or_f)
parser_edit.add_argument("--rank",
                         dest = "rank",
                         help = "number of skill ranks",
                         type = int)
parser_edit.add_argument("--cast",
                         dest = "cast",
                         help = "number of times cast",
                         type = int)
parser_edit.add_argument("--prepared",
                         dest = "prepared",
                         help = "number of casts prepared",
                         type = int)
parser_edit.add_argument("--level",
                         dest = "level",
                         help = "level of spell",
                         type = int)
parser_edit.add_argument("--attackType",
                         dest = "attackType",
                         choices = ["melee", "ranged"],
                         help = "type of attack (melee, ranged)",
                         type = str)
parser_edit.add_argument("--damageType",
                         dest = "damageType",
                         help = "type of damage dealt",
                         type = str)
parser_edit.add_argument("--damage",
                         dest = "damage",
                         help = "amount of damage dealt",
                         type = str)
parser_edit.add_argument("--critRoll",
                         dest = "critRoll",
                         help = "the minimum roll to threaten a critical strike",
                         type = int)
parser_edit.add_argument("--critMulti",
                         dest = "critMulti",
                         help = "the damage multiplier upon critical strike",
                         type = int)
parser_edit.add_argument("--range",
                         dest = "range",
                         help = "the range of the attack, in feet",
                         type = int)
parser_edit.add_argument("--base",
                         dest = "base",
                         help = "the base value of the ability",
                         type = int)

# New: create new character sheet
parser_new = subparsers.add_parser("new",
                                   help = "create new blank character sheet")
# File path (positional)
parser.add_argument("file",
                    metavar = "filepath",
                    type = str,
                    help = "path to character sheet file")

args = parser.parse_args()

# Main execution
subcommand = args.subcommand_name
try:
    target = args.target
except AttributeError:
    target = None

if subcommand == "new":
    character = pf.Character()
    pf.writeCharacter(character, args.file)
    print("    Blank character sheet saved to " + args.file + "\n")
    sys.exit()
else:
    try:
        with open(args.file) as f:
            character = pf.Character(json.load(f))
    except FileNotFoundError:
        print("File not found.")
        sys.exit()

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
        new_feat = character.add_feat(name = args.name,
                                      description = args.description,
                                      notes = args.notes)
        if new_feat["name"] == args.name and \
           new_feat["description"] == args.description and \
           new_feat["notes"] == args.notes:
            dataChanged = True
            print(getFeatString(character))
            print("\n    Feat added\n")
        else:
            print("\n    Something went wrong; new feat not added properly; aborting\n")
    elif target == "trait":
        new_trait = character.add_trait(name = args.name,
                                        description = args.description,
                                        notes = args.notes)
        if new_trait["name"] == args.name and \
           new_trait["description"] == args.description and \
           new_trait["notes"] == args.notes:
            dataChanged = True
            print(getTraitString(character))
            print("\n    Trait added\n")
        else:
            print("\n    Something went wrong; new trait not added properly; aborting\n")
    elif target == "special":
        new_special = character.add_special(name = args.name,
                                            description = args.description,
                                            notes = args.notes)
        if new_special["name"] == args.name and \
           new_special["description"] == args.description and \
           new_special["notes"] == args.notes:
            dataChanged = True
            print(getSpecialString(character))
            print("\n    Special added\n")
        else:
            print("\n    Something went wrong; new special ability not added properly; aborting\n")
    elif target == "item":
        new_item = character.add_item(name = args.name,
                                      weight = args.weight,
                                      count = args.count,
                                      pack = args.pack,
                                      notes = args.notes)
        if new_item["name"] == args.name and \
           new_item["weight"] == args.weight and \
           new_item["count"] == args.count and \
           new_item["pack"] == args.pack and \
           new_item["notes"] == args.notes:
            dataChanged = True
            print(getEquipmentString(character))
            print("\n    Item added\n")
        else:
            print("\n    Something went wrong; new item not added properly; aborting\n")
    elif target == "attack":
        new_attack = character.addAttack(name = args.name,
                                         attackType = args.attackType,
                                         damageType = args.damageType,
                                         damage = args.damage,
                                         critRoll = args.critRoll,
                                         critMulti = args.critMulti,
                                         notes = args.notes,
                                         range_ = args.range)
        if new_attack.name == args.name and \
           new_attack.attackType == args.attackType and \
           new_attack.damageType == args.damageType and \
           new_attack.damage == args.damage and \
           new_attack.critRoll == args.critRoll and \
           new_attack.critMulti == args.critMulti and \
           new_attack.range == args.range and \
           new_attack.notes == args.notes:
            dataChanged = True
            print(getCombatString(character))
            print("\n    Attack added\n")
        else:
            print("\n    Something went wrong; new attack not added properly; aborting\n")
    elif target == "armor":
        new_armor = character.add_armor(name = args.name,
                                        acBonus = args.acBonus,
                                        acPenalty = args.acPenalty,
                                        maxDexBonus = args.maxDexBonus,
                                        arcaneFailureChance = args.arcaneFailureChance,
                                        type_ = args.type)
        if new_armor["name"] == args.name and \
           new_armor["acBonus"] == args.acBonus and \
           new_armor["acPenalty"] == args.acPenalty and \
           new_armor["maxDexBonus"] == args.maxDexBonus and \
           new_armor["arcaneFailureChance"] == args.arcaneFailureChance:
            dataChanged = True
            print(getCombatString(character))
            print("\n    Armor added\n")
        else:
            print("\n    Something went wrong; new armor not added properly; aborting\n")
    elif target == "spell":
        new_spell = character.add_spell(name = args.name,
                                        level = args.level,
                                        description = args.description,
                                        prepared = args.prepared,
                                        cast = args.cast)
        if new_spell["name"] == args.name and \
           new_spell["level"] == args.level and \
           new_spell["description"] == args.description and \
           new_spell["prepared"] == args.prepared and \
           new_spell["cast"] == args.cast:
            dataChanged = True
            print(getSpellString(character))
            print("\n    Spell added\n")
        else:
            print("\n    Something went wrong; new spell not added properly; aborting\n")
elif subcommand == "edit":
    if target == "feat":
        updates = {}
        if args.new_name:
            updates["new_name"] = args.new_name
        if args.description:
            updates["description"] = args.description
        if args.notes:
            updates["notes"] = args.notes
        updated_feat = character.update_feat(name = args.name,
                                            data = updates)
        # If update_feat() returned "None," it means that there was 
        # no matching feat with the name given
        if updated_feat == None:
            print("\n    No matching feat with the name given; aborting\n")
        else:
        # Seeing if updates were applied successfully, testing all args 
        # provided
            success = True
            for item in updates.keys():
                # New_name is a special case:
                if item == "new_name":
                    if updates["new_name"] != updated_feat["name"]:
                        success = False
                else:
                    if updates[item] != updated_feat[item]:
                        success = False
            if success:
                dataChanged = True
                print(getFeatString(character))
                print("\n    Feat updated\n")
            else:
                print("\n    Something went wrong; feat not updated properly; aborting\n")
    elif target == "trait":
        updates = {}
        if args.new_name:
            updates["new_name"] = args.new_name
        if args.description:
            updates["description"] = args.description
        if args.notes:
            updates["notes"] = args.notes
        updated_trait = character.update_trait(name = args.name,
                                              data = updates)
        # If update_trait() returned "None," it means that there was no 
        # matching trait with the name given
        if updated_trait == None:
            print("\n    No matching trait with the name given; aborting\n")
        else:
        # Seeing if updates were applied successfully, testing all args 
        # provided
            success = True
            for item in updates.keys():
                # New_name is a special case:
                if item == "new_name":
                    if updates["new_name"] != updated_trait["name"]:
                        success = False
                else:
                    if updates[item] != updated_trait[item]:
                        success = False
            if success:
                dataChanged = True
                print(getTraitString(character))
                print("\n    Trait updated\n")
            else:
                print("\n    Something went wrong; trait not updated properly; aborting\n")
    elif target == "special":
        updates = {}
        if args.new_name:
            updates["new_name"] = args.new_name
        if args.description:
            updates["description"] = args.description
        if args.notes:
            updates["notes"] = args.notes
        updated_special = character.update_special(name = args.name,
                                              data = updates)
        # If update_special() returned "None," it means that there was 
        # no matching special ability with the name given
        if updated_special == None:
            print("\n    No matching special ability with the name given; aborting\n")
        else:
        # Seeing if updates were applied successfully, testing all args 
        # provided
            success = True
            for item in updates.keys():
                # New_name is a special case:
                if item == "new_name":
                    if updates["new_name"] != updated_special["name"]:
                        success = False
                else:
                    if updates[item] != updated_special[item]:
                        success = False
            if success:
                dataChanged = True
                print(getSpecialString(character))
                print("\n    Special ability updated\n")
            else:
                print("\n    Something went wrong; special ability not updated properly; aborting\n")
    elif target == "item":
        updates = {}
        if args.weight:
            updates["weight"] = args.weight
        if args.count != None:
            updates["count"] = args.count
        # Special
        if args.pack != None:
            updates["pack"] = args.pack
        if args.notes:
            updates["notes"] = args.notes
        updated_item = character.update_item(name = args.name,
                                             data = updates)
        # If update_item() returned "None," it means that there was 
        # no matching item with the name given
        if updated_item == None:
            print("\n    No matching item with the name given; aborting\n")
        else:
        # Seeing if updates were applied successfully, testing all args 
        # provided
            success = True
            for item in updates.keys():
                if updates[item] != updated_item[item]:
                    success = False
            if success:
                dataChanged = True
                print(getEquipmentString(character))
                print("\n    Item updated\n")
            else:
                print("\n    Something went wrong; item not updated properly; aborting\n")
    elif target == "spell":
        updates = {}
        if args.level:
            updates["level"] = args.level
        if args.prepared:
            updates["prepared"] = args.prepared
        if args.cast:
            updates["cast"] = args.cast
        if args.description:
            updates["description"] = args.description
        updated_spell = character.update_spell(name = args.name,
                                               data = updates)
        # If update_spell() returned "None," it means that there was 
        # no matching spell with the name given
        if updated_spell == None:
            print("\n    No matching spell with the name given; aborting\n")
        else:
        # Seeing if updates were applied successfully, testing all args 
        # provided
            success = True
            for item in updates.keys():
                if updates[item] != updated_spell[item]:
                    success = False
            if success:
                dataChanged = True
                print(getSpellString(character))
                print("\n    Spell updated\n")
            else:
                print("\n    Something went wrong; spell not updated properly; aborting\n")
    elif target == "attack":
        updates = {}
        if args.attackType:
            updates["attackType"] = args.attackType
        if args.damageType:
            updates["damageType"] = args.damageType
        if args.damage:
            updates["damage"] = args.damage
        if args.critRoll:
            updates["critRoll"] = args.critRoll
        if args.critMulti:
            updates["critMulti"] = args.critMulti
        if args.range:
            updates["range_"] = args.range
        if args.notes:
            updates["notes"] = args.notes
        updated_attack = character.updateAttack(name = args.name,
                                                data = updates)
        # If updateAttack() returned "None," it means that there was no 
        # matching attack with the name given
        if updated_attack == None:
            print("\n    No matching attack with the name given; aborting\n")
        else:
        # Seeing if updates were applied successfully, testing all args 
        # provided
            success = True
            for item in updates.keys():
                # Range is special
                if item == "range_":
                    if updates["range_"] != getattr(updated_attack, "range"):
                        success = False
                else:
                    if updates[item] != getattr(updated_attack, item):
                        success = False
            if success:
                dataChanged = True
                print(getCombatString(character))
                print("\n    Attack updated\n")
            else:
                print("\n    Something went wrong; attack not updated properly; aborting\n")
    elif target == "skill":
        updates = {}
        if args.rank:
            updates["rank"] = args.rank
        # Special boolean handling
        if args.isClass != None:
            updates["isClass"] = args.isClass
        if args.notes:
            updates["notes"] = args.notes
        updated_skill = character.update_skill(name = args.name,
                                               data = updates)
        # If update_skill() returned "None," it means that there was no 
        # matching skill with the name given
        if updated_skill == None:
            print("\n    No matching skill with the name given; aborting\n")
        else:
        # Seeing if updates were applied successfully, testing all args 
        # provided
            success = True
            for item in updates.keys():
                if updates[item] != updated_skill[item]:
                    success = False
            if success:
                dataChanged = True
                print(getSkillString(character))
                print("\n    Skill updated\n")
            else:
                print("\n    Something went wrong; skill not updated properly; aborting\n")
    elif target == "ability":
        updates = {}
        if args.base:
            updates["base"] = args.base
        updated_ability = character.update_ability(name = args.name,
                                                   data = updates)
        # Seeing if updates were applied successfully, testing all args 
        # provided
        success = True
        for item in updates.keys():
            if updates[item] != updated_ability[item]:
                success = False
        if success:
            dataChanged = True
            print(getAbilityString(character))
            print("\n    Ability updated\n")
        else:
            print("\n    Something went wrong; ability not updated properly; aborting\n")

# Write check
if dataChanged:
    pf.writeCharacter(character, args.file)
    print("    Changes saved to " + args.file + "\n")
