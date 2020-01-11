#!/bin/python3
#
# pythfinder.py

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
                self.classes.append(CharacterClass(data = item))

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
                self.special.append(CharacterBasicItem(data = item))

        self.traits = []
        if "traits" in keys:
            for item in data["traits"]:
                self.traits.append(CharacterBasicItem(data = item))

        self.feats = []
        if "feats" in keys:
            for item in data["feats"]:
                self.feats.append(CharacterBasicItem(data = item))


        self.equipment = []
        if "equipment" in keys:
            for item in data["equipment"]:
                self.equipment.append(CharacterEquipment(data = item))

        self.savingThrows = {}
        if "savingThrows" in keys:
            for item in data["savingThrows"].keys():
                self.savingThrows[item] = CharacterSavingThrow(data = data["savingThrows"][item])
        
        self.skills = []
        if "skills" in keys:
            for item in data["skills"]:
                self.skills.append(CharacterSkill(data = item))

        self.spells = []
        if "spells" in keys:
            for item in data["spells"]:
                self.spells.append(CharacterSpell(data = item))

        self.attacks = []
        if "attacks" in keys:
            for item in data["attacks"]:
                self.attacks.append(CharacterAttack(data = item))

        self.armor = []
        if "armor" in keys:
            for item in data["armor"]:
                self.armor.append(CharacterArmor(data = item))

    # Get the modifier for a given ability
    def getAbilityMod(self, ability):
        abilityRange = ["str","dex","con","int","wis","cha"]
        if ability not in abilityRange:
            raise ValueError("getAbilityMod: ability must be one of " + abilityRange)
        value = getattr(self.abilities, ability)
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
        output["classes"] = []
        for item in self.classes:
            output["classes"].append(item.__dict__)
        output["alignment"] = self.alignment
        output["description"] = self.description
        output["height"] = self.height
        output["weight"] = self.weight
        output["abilities"] = self.abilities.__dict__
        output["hp"] = self.hp.__dict__
        return output

    # Returns a dict containing keys for each level of spell present in the 
    # character's list of spells. Within each key, the spells are sorted by 
    # name.
    def getSortedSpells(self):
        output = {}
        spellLevels = []

        # We're doing this because we don't want to end up with empty keys 
        # (makes things easier later)
        for spell in self.spells:
            spellLevels.append(spell.level)

        spellLevelsUnique = sorted(set(spellLevels))

        # Initializing an empty list for each spell level present in th espell 
        # list
        for level in spellLevelsUnique:
            output[level] = []

        for spell in self.spells:
            output[spell.level].append(spell)

        return output

    # Returns a dict of the entire character
    def getDict(self):
        return json.loads(
            json.dumps(self, default = lambda o: getattr(o, '__dict__', str(o)))
        )

    # Returns a JSON string representation of the entire character
    def getJson(self):
        return json.dumps(self, default = lambda o: getattr(o, '__dict__', str(o)))

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

    # Returns dict of the class
    def getClassDict(self):
        return self.__dict__

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

class CharacterSpell:
    def __init__(self,
                 name = "",
                 level = 0,
                 description = "",
                 prepared = 0,
                 cast = 0,
                 data = {}):
        keys = data.keys()
        self.name = data["name"] if "name" in keys else name
        self.level = data["level"] if "level" in keys else level
        self.description = data["description"] if "description" in keys else description
        self.prepared = data["prepared"] if "prepared" in keys else prepared
        self.cast = data["cast"] if "cast" in keys else cast

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

class CharacterEquipment:
    def __init__(self,
                 name = "",
                 weight = 0,
                 count = 0,
                 pack = False,
                 notes = "",
                 data = {}):
        keys = data.keys()
        self.name = data["name"] if "name" in keys else name
        self.weight = data["weight"] if "weight" in keys else weight
        self.count = data["count"] if "count" in keys else count
        self.pack = data["pack"] if "pack" in keys else pack
        self.notes = data["notes"] if "notes" in keys else notes

class CharacterSavingThrow:
    def __init__(self,
                 base = 0,
                 misc = 0,
                 data = {}):
        keys = data.keys()
        self.base = data["base"] if "base" in keys else base
        self.misc = data["misc"] if "misc" in keys else misc

class CharacterSkill:
    def __init__(self,
                 name = "",
                 rank = 0,
                 isClass = False,
                 notes = "",
                 misc = 0,
                 data = {}):
        keys = data.keys()
        allowedNames = (
            "Acrobatics", "Appraise", "Bluff",
            "Climb", "Craft", "Diplomacy",
            "Disable Device", "Disguise", "Escape Artist",
            "Fly", "Handle Animal", "Heal",
            "Intimidate", "Knowledge (Arcana)", "Knowledge (Dungeoneering)",
            "Knowledge (Engineering)", "Knowledge (Geography)", "Knowledge (History)",
            "Knowledge (Local)", "Knowledge (Nature)", "Knowledge (Nobility)",
            "Knowledge (Planes)", "Knowledge (Religion)", "Linguistics",
            "Perception", "Perform", "Profession",
            "Ride", "Sense Motive", "Sleight Of Hand",
            "Spellcraft", "Stealth", "Survival",
            "Swim", "Use Magic Device"
        )
        trainedOnly = (
            "Disable Device", "Handle Animal", "Knowledge (Arcana)",
            "Knowledge (Dungeoneering)", "Knowledge (Engineering)", "Knowledge (Geography)",
            "Knowledge (History)", "Knowledge (Local)", "Knowledge (Nature)",
            "Knowledge (Nobility)", "Knowledge (Planes)", "Knowledge (Religion)",
            "Linguistics", "Perception", "Profession",
            "Sleight Of Hand", "Spellcraft", "Use Magic Device"
        )
        mods = {
            "Climb": "str",
            "Swim": "str",
            "Acrobatics": "dex",
            "Disable Device": "dex",
            "Escape Artist": "dex",
            "Fly": "dex",
            "Ride": "dex",
            "Sleight Of Hand": "dex",
            "Stealth": "dex",
            "Appraise": "int",
            "Craft": "int",
            "Knowledge (Arcana)": "int",
            "Knowledge (Dungeoneering)": "int",
            "Knowledge (Engineering)": "int",
            "Knowledge (Geography)": "int",
            "Knowledge (History)": "int",
            "Knowledge (Local)": "int",
            "Knowledge (Nature)": "int",
            "Knowledge (Nobility)": "int",
            "Knowledge (Planes)": "int",
            "Knowledge (Religion)": "int",
            "Linguistics": "int",
            "Spellcraft": "int",
            "Heal": "wis",
            "Perception": "wis",
            "Profession": "wis",
            "Sense Motive": "wis",
            "Survival": "wis",
            "Bluff": "cha",
            "Diplomacy": "cha",
            "Disguise": "cha",
            "Handle Animal": "cha",
            "Intimidate": "cha",
            "Perform": "cha",
            "Use Magic Device": "cha"
        }

        self.name = data["name"] if "name" in keys else name
        if not self.name in allowedNames:
            raise ValueError("CharacterSkill: name must be one of " + allowedNames)
        self.rank = data["rank"] if "rank" in keys else rank
        self.isClass = data["isClass"] if "isClass" in keys else isClass
        self.notes = data["notes"] if "notes" in keys else notes
        self.misc = data["misc"] if "misc" in keys else misc

        self.mod = mods[self.name]
        self.useUntrained = False if self.name in trainedOnly else True

class CharacterAttack:
    def __init__(self,
                 weapon = "",
                 attackType = "",
                 damageType = [],
                 damage = "",
                 critRoll = 20,
                 critMulti = 2,
                 range_ = 0,
                 notes = "",
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

class CharacterArmor:
    def __init__(self,
                 name = "",
                 acBonus = 0,
                 acPenalty = 0,
                 maxDexBonus = 0,
                 arcaneFailureChance = 0,
                 type_ = "",
                 data = {}):
        keys = data.keys()
        self.name = data["name"] if "name" in keys else name
        self.acBonus = data["acBonus"] if "acBonus" in keys else acBonus
        self.acPenalty = data["acPenalty"] if "acPenalty" in keys else acPenalty
        self.maxDexBonus = data["maxDexBonus"] if "maxDexBonus" in keys else maxDexBonus
        self.arcaneFailureChance = data["arcaneFailureChance"] if "arcaneFailureChance" in keys else arcaneFailureChance
        self.type = data["type"] if "type" in keys else type_

### FUNCTIONS ###

# Write the given character data to the file in path
def writeCharacter(character, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(character.getDict, f, indent=4)
