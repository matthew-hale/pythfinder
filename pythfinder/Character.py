import json
import math

from pythfinder.roll import roll

# These vars are used for skill initialization
_allowed_skill_names = (
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
_trained_only = (
    "Disable Device", "Handle Animal", "Knowledge (Arcana)",
    "Knowledge (Dungeoneering)", "Knowledge (Engineering)", "Knowledge (Geography)",
    "Knowledge (History)", "Knowledge (Local)", "Knowledge (Nature)",
    "Knowledge (Nobility)", "Knowledge (Planes)", "Knowledge (Religion)",
    "Linguistics", "Profession",
    "Sleight Of Hand", "Spellcraft", "Use Magic Device"
)
_skill_mods = {
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

# Main character class
class Character:
    def __init__(self, data = {}):
        # Grab keys from imported json data
        keys = data.keys()

        # These are the simple values (those of a type like string, 
        # int, etc.). More complex values will use more complex dicts
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
        self.spellsPerDay = data["spellsPerDay"] if "spellsPerDay" in keys else {
            "0": 0,
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 0,
            "5": 0,
            "6": 0,
            "7": 0,
            "8": 0,
            "9": 0
        }
        self.baseAttackBonus = data["baseAttackBonus"] if "baseAttackBonus" in keys else []
        self.gold = data["gold"] if "gold" in keys else 0

        # Complex object members

        # AC modifiers
        self.AC = []
        if "AC" in keys:
            for item in data["AC"]:
                self.AC.append(item)

        # Speed initialization
        if "speed" in keys:
            data_keys = data["speed"].keys()
            self.speed = {
                "base": data["speed"]["base"] if "base" in data_keys else 0,
                "armor": data["speed"]["armor"] if "armor" in data_keys else 0,
                "fly": data["speed"]["fly"] if "fly" in data_keys else 0,
                "swim": data["speed"]["swim"] if "swim" in data_keys else 0,
                "climb": data["speed"]["climb"] if "climb" in data_keys else 0,
                "burrow": data["speed"]["burrow"] if "burrow" in data_keys else 0,
            }
        else:
            self.speed = {
                "base": 0,
                "armor": 0,
                "fly": 0,
                "swim": 0,
                "climb": 0,
                "burrow": 0
            }

        self.classes = []
        if "classes" in keys:
            for item in data["classes"]:
                _ = self.add_class(data = item)

        # Ability initialization
        #
        self.abilities = {}
        #
        # Abilities are nested dicts, so more validation is necessary 
        # (like with saving throws)
        if "abilities" in keys:
            data_keys = data["abilities"].keys()
            for key in data_keys:
                if key in ("str","dex","con","int","wis","cha"):
                    data_subkeys = data["abilities"][key].keys()
                    self.abilities[key] = {
                        "base": data["abilities"][key]["base"] if "base" in data_subkeys else 0,
                        "misc": data["abilities"][key]["misc"] if "misc" in data_subkeys else [],
                    }
        else:
            self.abilities = {
                "str": {
                    "base": 0,
                    "misc": []
                },
                "dex": {
                    "base": 0,
                    "misc": []
                },
                "con": {
                    "base": 0,
                    "misc": []
                },
                "int": {
                    "base": 0,
                    "misc": []
                },
                "wis": {
                    "base": 0,
                    "misc": []
                },
                "cha": {
                    "base": 0,
                    "misc": []
                }
            }

        if "hp" in keys:
            data_keys = data["hp"].keys()
            self.hp = {
                "max": data["hp"]["max"] if "max" in data_keys else 0,
                "current": data["hp"]["current"] if "current" in data_keys else 0,
                "temporary": data["hp"]["temporary"] if "temporary" in data_keys else 0,
                "nonlethal": data["hp"]["nonlethal"] if "nonlethal" in data_keys else 0,
            }
        else:
            self.hp = {
                "max": 0,
                "current": 0,
                "temporary": 0,
                "nonlethal": 0
            }

        # Special ability initialization
        #
        self.special = []
        #
        # If the character has no special abilities, we'll just skip it 
        # and leave it as an empty list. Otherwise, we'll want to add 
        # abilities using a constructor method.
        if "special" in keys:
            for item in data["special"]:
                # add_special returns the special ability dict, and we 
                # don't want it, so we're throwing it out
                _ = self.add_special(data = item)

        # Trait initialization
        #
        self.traits = []
        #
        # As above.
        if "traits" in keys:
            for item in data["traits"]:
                # add_trait returns the trait dict, and we don't want 
                # it, so we're throwing it out
                _ = self.add_trait(data = item)

        # Feat initialization
        #
        self.feats = []
        #
        # As above.
        if "feats" in keys:
            for item in data["feats"]:
                # add_feat returns the feat dict, and we don't want 
                # it, so we're throwing it out
                _ = self.add_feat(data = item)

        self.equipment = []
        if "equipment" in keys:
            for item in data["equipment"]:
                _ = self.add_item(data = item)

        # Saving throw initialization
        #
        self.saving_throws = {}
        #
        # Saving throws are nested dictionaries, so we have to do more 
        # key checking than usual.
        if "saving_throws" in keys:
            data_keys = data["saving_throws"].keys()
            for key in data_keys:
                if key in ("fortitude","reflex","will"):
                    data_subkeys = data["saving_throws"][key].keys()
                    self.saving_throws[key] = {
                        "base": data["saving_throws"][key]["base"] if "base" in data_subkeys else 0,
                        "misc": data["saving_throws"][key]["misc"] if "misc" in data_subkeys else [],
                    }
        else:
            self.saving_throws = {
                "fortitude": {
                    "base": 0,
                    "misc": []
                },
                "reflex": {
                    "base": 0,
                    "misc": []
                },
                "will": {
                    "base": 0,
                    "misc": []
                }
            }
        
        # Skill initialization
        #
        self.skills = {}
        if "skills" in keys:
            for item in data["skills"]:
                _ = self.add_skill(data = data["skills"][item])
        # If there are no skills in the character data, initialize from 
        # defaults
        else:
            for skill_name in _allowed_skill_names:
                self.skills[skill_name] = {
                    "name": skill_name,
                    "rank": 0,
                    "isClass":  False,
                    "notes": "",
                    "misc": [],
                    "mod": _skill_mods[skill_name],
                    "useUntrained": False if skill_name in _trained_only else True
                }

        # Spells, attacks, and armor are all collections of 
        # dictionaries; their initialization is pretty boring
        self.spells = []
        if "spells" in keys:
            for item in data["spells"]:
                _ = self.add_spell(data = item)

        self.attacks = []
        if "attacks" in keys:
            for item in data["attacks"]:
                _ = self.add_attack(data = item)

        self.armor = []
        if "armor" in keys:
            for item in data["armor"]:
                _ = self.add_armor(data = item)

    # Get the modifier for a given ability
    def getAbilityMod(self, ability):
        if ability <= 1:
            return -5
        else:
            return math.floor(0.5 * ability - 5) # ability modifier equation

    # Returns a dict containing the character object, without long elements 
    # like skills, feats, traits, spells, and equipment.
    def getCharacterShort(self):
        output = {}
        output["name"] = self.name
        output["race"] = self.race
        output["classes"] = []
        for item in self.classes:
            output["classes"].append(item)
        output["alignment"] = self.alignment
        output["description"] = self.description
        output["height"] = self.height
        output["weight"] = self.weight
        output["abilities"] = self.abilities
        output["hp"] = self.hp
        return output

    # Returns the character's calculated AC value
    def get_total_AC(self,
                     flat_footed = False,
                     touch = False):
        total_dex_mod = self.getAbilityMod(self.get_total_ability_value("dex"))
        # Flat footed sets dex bonus to 0
        if flat_footed:
            total_dex_mod = 0
        total_armor_bonus = 0
        for item in self.armor:
            total_armor_bonus += item["acBonus"]
            if item["maxDexBonus"] < total_dex_mod:
                total_dex_mod = item["maxDexBonus"]
        # Touch sets armor bonuses to 0
        if touch:
            total_armor_bonus = 0
        # If there are no modifiers to AC in the character, this 
        # defaults to 0
        total_AC_mods = sum(self.AC) or 0
        ac_total = sum([10, total_dex_mod, total_armor_bonus, total_AC_mods])
        return ac_total

    # Returns a dict containing keys for each level of spell present in the 
    # character's list of spells. Within each key, the spells are sorted by 
    # name.
    def get_sorted_spells(self):
        output = {}
        spellLevels = []

        # We're doing this because we don't want to end up with empty keys 
        # (makes things easier later)
        for spell in self.spells:
            spellLevels.append(spell["level"])

        spellLevelsUnique = sorted(set(spellLevels))

        # Initializing an empty list for each spell level present in th espell 
        # list
        for level in spellLevelsUnique:
            output[level] = []

        for spell in self.spells:
            output[spell["level"]].append(spell)

        return output

    # Returns a dict of the entire character
    def getDict(self):
        return json.loads(
            json.dumps(self, default = lambda o: getattr(o, '__dict__', str(o)))
        )

    # Returns a JSON string representation of the entire character
    def getJson(self):
        return json.dumps(self, default = lambda o: getattr(o, '__dict__', str(o)))

    # Returns the total value of the specified skill, taking into 
    # account all of the current modifiers, including:
    #
    # + Skill ranks
    # + Class skill status
    # + Misc. skill modifiers
    # + Skill's current ability modifier
    def get_skill_value(self, skill):
        total = 0
        skill_names = self.skills.keys()
        if not skill in skill_names:
            raise ValueError("get_skill_value: '" + skill + "' not in character skills")
        current_skill = self.skills[skill]
        if current_skill["isClass"] and current_skill["rank"] >= 1:
            total += 3
        total += current_skill["rank"]
        total += sum(current_skill["misc"])
        total += self.getAbilityMod(self.get_total_ability_value(current_skill["mod"]))
        return total

    # Returns the base ability score given an ability string
    def get_base_ability_value(self, ability):
        ability_strings = ("str", "dex", "con", "int", "wis", "cha")
        if ability not in ability_strings:
            raise ValueError("ability must be one of " + ability_strings)
        return self.abilities[ability]["base"]

    # Returns the ability value after summing modifiers
    def get_total_ability_value(self, ability):
        ability_strings = ("str", "dex", "con", "int", "wis", "cha")
        if ability not in ability_strings:
            raise ValueError("ability must be one of " + ability_strings)
        return sum(self.abilities[ability]["misc"], self.abilities[ability]["base"])

    # Checks that the given name string is unique among the collection 
    # contained within the property name
    def is_unique_name(self,
                       name,
                       prop):
        allowed_props = ("classes",
                         "special",
                         "traits",
                         "feats",
                         "skills",
                         "equipment",
                         "attacks",
                         "armor",
                         "spells")
        if not prop in allowed_props:
            raise ValueError("check_unique_name: prop must be one of " + str(allowed_props))
        # Skills are a special case
        if prop == "skills":
            current_names = [item for item in self.skills]
        else:
        # Gather names from the given property, and check if 'name' is 
        # in the collection. If it is, it's not unique, and the 
        # function returns False; otherwise, it returns True.
            current_names = [item["name"] for item in getattr(self, prop)]
        if name in current_names:
            return False
        else:
            return True

    # Add a new class to the character; supports either named arguments 
    # or a dictionary
    #
    # returns the newly created class
    def add_class(self,
                  name = "",
                  archetypes = [],
                  level = 0,
                  data = {}):
        keys = data.keys()
        new_name = data["name"] if "name" in keys else name
        # Validate that new_name is not null or empty
        if new_name == None or new_name == "":
            raise ValueError("add_class: name must not be null or empty")
        # Validate that new_name is unique
        if not self.is_unique_name(name = new_name, prop = "classes"):
            raise ValueError("add_class: name must be unique among classes")
        new_archetypes = data["archetypes"] if "archetypes" in keys else archetypes
        new_level = data["level"] if "level" in keys else level
        new_class = {
            "name": new_name,
            "archetypes": new_archetypes,
            "level": new_level
        }
        self.classes.append(new_class)
        return new_class

    # Add a new feat to the character; supports either named arguments 
    # or a dictionary
    #
    # returns the newly created feat
    def add_feat(self,
                 name = "",
                 description = "",
                 notes = "",
                 data = {}):
        keys = data.keys()
        new_name = data["name"] if "name" in keys else name
        # Validate that new_name is not null or empty
        if new_name == None or new_name == "":
            raise ValueError("add_feat: name must not be null or empty")
        # Validate that new_name is unique
        if not self.is_unique_name(name = new_name, prop = "feats"):
            raise ValueError("add_feat: name must be unique among feats")
        new_description = data["description"] if "description" in keys else description
        new_notes = data["notes"] if "notes" in keys else notes
        new_feat = {
            "name": new_name,
            "description": new_description,
            "notes": new_notes,
        }
        self.feats.append(new_feat)
        return new_feat

    # Add a new trait to the character; supports either named arguments 
    # or a dictionary
    #
    # returns the newly created trait
    def add_trait(self,
                  name = "",
                  description = "",
                  notes = "",
                  data = {}):
        keys = data.keys()
        new_name = data["name"] if "name" in keys else name
        # Validate that new_name is not null or empty
        if new_name == None or new_name == "":
            raise ValueError("add_trait: name must not be null or empty")
        # Validate that new_name is unique
        if not self.is_unique_name(name = new_name, prop = "traits"):
            raise ValueError("add_trait: name must be unique among traits")
        new_description = data["description"] if "description" in keys else description
        new_notes = data["notes"] if "notes" in keys else notes
        new_trait = {
            "name": new_name,
            "description": new_description,
            "notes": new_notes,
        }
        self.traits.append(new_trait)
        return new_trait

    # Add a new special ability to the character; supports either named 
    # arguments or a dictionary
    #
    # returns the newly created special ability
    def add_special(self,
                    name = "",
                    description = "",
                    notes = "",
                    data = {}):
        keys = data.keys()
        new_name = data["name"] if "name" in keys else name
        # Validate that new_name is not null or empty
        if new_name == None or new_name == "":
            raise ValueError("add_special: name must not be null or empty")
        # Validate that new_name is unique
        if not self.is_unique_name(name = new_name, prop = "special"):
            raise ValueError("add_special: name must be unique among specials")
        new_description = data["description"] if "description" in keys else description
        new_notes = data["notes"] if "notes" in keys else notes
        new_special = {
            "name": new_name,
            "description": new_description,
            "notes": new_notes,
        }
        self.special.append(new_special)
        return new_special

    # Add a skill to the character (craft, profession, and perform); 
    # supports either named arguments or a dictionary
    # 
    # returns the newly created skill
    def add_skill(self,
                  name = "",
                  rank = 0,
                  isClass = False, 
                  notes = "",
                  misc = [],
                  data = {}):
        # Handle skills with variable names
        valid_names = ("Perform", "Profession", "Craft")
        skill_type = ""
        keys = data.keys()
        new_name = data["name"] if "name" in keys else name
        # Validate that new_name is not null or empty
        if new_name == None or new_name == "":
            raise ValueError("add_item: name must not be null or empty")
        # Validate skill name is in allowed_skills
        # If so, we can use all the built-in values for things
        if new_name in _allowed_skill_names:
            new_mod = _skill_mods[new_name]
            if new_name in _trained_only:
                new_useUntrained = False
            else:
                new_useUntrained = True
        # Validate skill name is one of the three above
        # These skills can exist multiple times with variable names
        else:
            is_valid = False
            for valid in valid_names:
                if valid in new_name:
                    is_valid = True
                    skill_type = valid
            if not is_valid:
                raise ValueError("add_skill: skill with custom name must be a Perform, Profession, or Craft skill")
            # Validate that new name is unique
            if not self.is_unique_name(name = new_name, prop = "skills"):
                raise ValueError("add_skill: name must be unique among skills")
            if skill_type in _trained_only:
                new_useUntrained = False
            else:
                new_useUntrained = True
            new_mod = _skill_mods[skill_type]
        # Get the rest of the properties
        new_rank = data["rank"] if "rank" in keys else rank
        new_isClass = data["isClass"] if "isClass" in keys else isClass
        new_notes = data["notes"] if "notes" in keys else notes
        new_misc = data["misc"] if "misc" in keys else misc
        new_skill = {
            "name": new_name,
            "rank": new_rank,
            "isClass": new_isClass,
            "mod": new_mod,
            "notes": new_notes,
            "useUntrained": new_useUntrained,
            "misc": new_misc,
        }
        self.skills[new_name] = new_skill
        return new_skill


    # Add a new item to the character; supports either named arguments 
    # or a dictionary
    #
    # returns the newly created item
    def add_item(self,
                 name = "",
                 weight = 0.0,
                 count = 0,
                 pack = False,
                 notes = "",
                 data = {}):
        keys = data.keys()
        new_name = data["name"] if "name" in keys else name
        # Validate that new_name is not null or empty
        if new_name == None or new_name == "":
            raise ValueError("add_item: name must not be null or empty")
        # Validate that new_name is unique
        if not self.is_unique_name(name = new_name, prop = "equipment"):
            raise ValueError("add_item: name must be unique among equipment")
        new_weight = data["weight"] if "weight" in keys else weight
        new_count = data["count"] if "count" in keys else count
        new_pack = data["pack"] if "pack" in keys else pack
        new_notes = data["notes"] if "notes" in keys else notes
        new_item = {
            "name": new_name,
            "weight": new_weight,
            "count": new_count,
            "pack": new_pack,
            "notes": new_notes,
        }
        self.equipment.append(new_item)
        return new_item

    # Add a new attack to the character; supports either named 
    # arguments or a dictionary
    #
    # returns the newly created attack
    def add_attack(self,
                   name = "",
                   attackType = "",
                   damageType = [],
                   damage = "",
                   critRoll = 20,
                   critMulti = 2,
                   range_ = 0,
                   notes = "",
                   data = {}):
        keys = data.keys()
        new_name = data["name"] if "name" in keys else name
        # Validate that new_name is not null or empty
        if new_name == None or new_name == "":
            raise ValueError("add_attack: name must not be null or empty")
        # Validate that new_name is unique
        if not self.is_unique_name(name = new_name, prop = "attacks"):
            raise ValueError("add_attack: name must be unique among attacks")
        new_attackType = data["attackType"] if "attackType" in keys else attackType
        new_damageType = data["damageType"] if "damageType" in keys else damageType
        new_damage = data["damage"] if "damage" in keys else damage
        new_critRoll = data["critRoll"] if "critRoll" in keys else critRoll
        new_critMulti = data["critMulti"] if "critMulti" in keys else critMulti
        new_range = data["range"] if "range" in keys else range_
        new_notes = data["notes"] if "notes" in keys else notes
        new_attack = {
            "name": new_name,
            "attackType": new_attackType,
            "damageType": new_damageType,
            "damage": new_damage,
            "critRoll": new_critRoll,
            "critMulti": new_critMulti,
            "range": new_range,
            "notes": new_notes
        }
        self.attacks.append(new_attack)
        return new_attack

    # Add new armor to the character; supports either named arguments 
    # or a dictionary
    #
    # returns the newly created armor
    def add_armor(self,
                  name = "",
                  acBonus = 0,
                  acPenalty = 0,
                  maxDexBonus = 0,
                  arcaneFailureChance = 0,
                  type_ = "",
                  data = {}):
        keys = data.keys()
        new_name = data["name"] if "name" in keys else name
        # Validate that new_name is not null or empty
        if new_name == None or new_name == "":
            raise ValueError("add_armor: name must not be null or empty")
        # Validate that new_name is unique
        if not self.is_unique_name(name = new_name, prop = "armor"):
            raise ValueError("add_armor: name must be unique among armor")
        new_acBonus = data["acBonus"] if "acBonus" in keys else acBonus
        new_acPenalty = data["acPenalty"] if "acPenalty" in keys else acPenalty
        new_maxDexBonus = data["maxDexBonus"] if "maxDexBonus" in keys else maxDexBonus
        new_arcaneFailureChance = data["arcaneFailureChance"] if "arcaneFailureChance" in keys else arcaneFailureChance
        new_type = data["type"] if "type" in keys else type_
        new_armor = {
            "name": new_name,
            "acBonus": new_acBonus,
            "acPenalty": new_acPenalty,
            "maxDexBonus": new_maxDexBonus,
            "arcaneFailureChance": new_arcaneFailureChance,
            "type": new_type
        }
        self.armor.append(new_armor)
        return new_armor

    # Add new spell to the character; supports either named arguments 
    # or a dictionary
    #
    # returns the newly created spell
    def add_spell(self,
                  name = "",
                  level = 0,
                  description = "",
                  prepared = 0,
                  cast = 0,
                  data = {}):
        keys = data.keys()
        new_name = data["name"] if "name" in keys else name
        # Validate that new_name is not null or empty
        if new_name == None or new_name == "":
            raise ValueError("add_spell: name must not be null or empty")
        # Validate that new_name is unique
        if not self.is_unique_name(name = new_name, prop = "spells"):
            raise ValueError("add_spell: name must be unique among spells")
        new_level = data["level"] if "level" in keys else level
        new_description = data["description"] if "description" in keys else description
        new_prepared = data["prepared"] if "prepared" in keys else prepared
        new_cast = data["cast"] if "cast" in keys else cast
        new_spell = {
            "name": new_name,
            "level": new_level,
            "description": new_description,
            "prepared": new_prepared,
            "cast": new_cast,
        }
        self.spells.append(new_spell)
        return new_spell

    # Update an existing feat based on name; supports either named 
    # arguments or a dictionary
    #
    # returns the updated feat
    def update_feat(self,
                    name = "",
                    new_name = "",
                    description = "",
                    notes = "",
                    data = {}):
        keys = data.keys()
        name = data["name"] if "name" in keys else name
        new_name = data["new_name"] if "new_name" in keys else new_name
        # Validate that new_name is unique
        if not self.is_unique_name(name = new_name, prop = "feats"):
            raise ValueError("update_feat: name must be unique among feats")
        description = data["description"] if "description" in keys else description
        notes = data["notes"] if "notes" in keys else notes
        # Lazy selection; if there are duplicates, this will just pick 
        # up the first one that shows up
        for feat in self.feats:
            if feat["name"] == name:
                target_feat = feat
                break
        try:
            target_feat
        except NameError:
            return None
        else:
            # Ignore empty parameters
            target_feat["name"] = new_name or target_feat["name"]
            target_feat["description"] = description or target_feat["description"]
            target_feat["notes"] = notes or target_feat["notes"]
            return target_feat

    # Update an existing trait based on name; supports either named 
    # arguments or a dictionary
    #
    # returns the updated trait
    def update_trait(self,
                     name = "",
                     new_name = "",
                     description = "",
                     notes = "",
                     data = {}):
        keys = data.keys()
        name = data["name"] if "name" in keys else name
        new_name = data["new_name"] if "new_name" in keys else new_name
        # Validate that new_name is unique
        if not self.is_unique_name(name = new_name, prop = "traits"):
            raise ValueError("update_trait: name must be unique among traits")
        description = data["description"] if "description" in keys else description
        notes = data["notes"] if "notes" in keys else notes
        # Lazy selection; if there are duplicates, this will just pick 
        # up the first one that shows up
        for trait in self.traits:
            if trait["name"] == name:
                target_trait = trait
                break
        try:
            target_trait
        except NameError:
            return None
        else:
            # Ignore empty parameters
            target_trait["name"] = new_name or target_trait["name"]
            target_trait["description"] = description or target_trait["description"]
            target_trait["notes"] = notes or target_trait["notes"]
            return target_trait

    # Update an existing special ability based on name; supports either 
    # named arguments or a dictionary
    #
    # returns the updated special ability
    def update_special(self,
                       name = "",
                       new_name = "",
                       description = "",
                       notes = "",
                       data = {}):
        keys = data.keys()
        name = data["name"] if "name" in keys else name
        new_name = data["new_name"] if "new_name" in keys else new_name
        # Validate that new_name is unique
        if not self.is_unique_name(name = new_name, prop = "special"):
            raise ValueError("update_special: name must be unique among specials")
        description = data["description"] if "description" in keys else description
        notes = data["notes"] if "notes" in keys else notes
        # Lazy selection; if there are duplicates, this will just pick 
        # up the first one that shows up
        for special in self.special:
            if special["name"] == name:
                target_special = special
                break
        try:
            target_special
        except NameError:
            return None
        else:
            # Ignore empty parameters
            target_special["name"] = new_name or target_special["name"]
            target_special["description"] = description or target_special["description"]
            target_special["notes"] = notes or target_special["notes"]
            return target_special

    # Update an existing item based on name; supports either named 
    # arguments or a dictionary
    #
    # returns the updated item 
    def update_item(self,
                    name = "",
                    new_name = "",
                    weight = None,
                    count = None,
                    pack = None,
                    notes = "",
                    data = {}):
        keys = data.keys()
        name = data["name"] if "name" in keys else name
        new_name = data["new_name"] if "new_name" in keys else new_name
        # Validate that new_name is unique
        if not self.is_unique_name(name = new_name, prop = "equipment"):
            raise ValueError("update_item: name must be unique among equipment")
        weight = data["weight"] if "weight" in keys else weight
        pack = data["pack"] if "pack" in keys else pack
        count = data["count"] if "count" in keys else count
        notes = data["notes"] if "notes" in keys else notes
        # Lazy selection; if there are duplicates, this will just pick 
        # up the first one that shows up
        for item in self.equipment:
            if item["name"] == name:
                target_item = item
                break
        try:
            target_item
        except NameError:
            return None
        else:
            # Ignore empty parameters
            # Handle zero ints
            if weight != None:
                target_item["weight"] = weight
            if count != None:
                target_item["count"] = count
            target_item["name"] = new_name or target_item["name"]
            target_item["notes"] = notes or target_item["notes"]
            # Pack is special
            if pack != None:
                target_item["pack"] = pack
            return target_item

    # Update an existing spell based on name; supports either named 
    # arguments or a dictionary
    #
    # returns the updated spell 
    def update_spell(self,
                     name = None,
                     new_name = "",
                     level = None,
                     description = None,
                     prepared = None,
                     cast = None,
                     data = {}):
        keys = data.keys()
        if "name" in keys:
            name = data["name"]
        new_name = data["new_name"] if "new_name" in keys else new_name
        # Validate that new_name is unique
        if not self.is_unique_name(name = new_name, prop = "spells"):
            raise ValueError("update_spell: name must be unique among spells")
        if "level" in keys:
            level = data["level"]
        if "description" in keys:
            description = data["description"]
        if "prepared" in keys:
            prepared = data["prepared"]
        if "cast" in keys:
            cast = data["cast"]
        # Lazy selection; if there are duplicates, this will just pick 
        # up the first one that shows up
        for spell in self.spells:
            if spell["name"] == name:
                target_spell = spell
                break
        try:
            target_spell
        except NameError:
            return None
        else:
            # Ignore empty parameters
            target_spell["name"] = new_name or target_spell["name"]
            target_spell["level"] = level or target_spell["level"]
            target_spell["description"] = description or target_spell["description"]
            target_spell["prepared"] = prepared or target_spell["prepared"]
            target_spell["cast"] = cast or target_spell["cast"]
            return target_spell

    # Update an existing piece of armor based on name; supports either 
    # named arguments or a dictionary
    #
    # returns the updated armor
    def update_armor(self,
                     name = None,
                     new_name = "",
                     acBonus = None,
                     acPenalty = None,
                     maxDexBonus = None,
                     arcaneFailureChance = None,
                     type_ = None,
                     data = {}):
        keys = data.keys()
        if "name" in keys:
            name = data["name"]
        new_name = data["new_name"] if "new_name" in keys else new_name
        # Validate that new_name is unique
        if not self.is_unique_name(name = new_name, prop = "armor"):
            raise ValueError("update_armor: name must be unique among armor")
        if "acBonus" in keys:
            acBonus = data["acBonus"]
        if "acPenalty" in keys:
            acPenalty = data["acPenalty"]
        if "maxDexBonus" in keys:
            maxDexBonus = data["maxDexBonus"]
        if "arcaneFailureChance" in keys:
            arcaneFailureChance = data["arcaneFailureChance"]
        if "type" in keys:
            type_ = data["type"]
        # Lazy selection; if there are duplicates, this will just pick 
        # up the first one that shows up
        for armor in self.armor:
            if armor["name"] == name:
                target_armor = armor
                break
        try:
            target_armor
        except NameError:
            return None
        else:
            # Ignore empty parameters
            target_armor["name"] = new_name or target_armor["name"]
            target_armor["acBonus"] = acBonus or target_armor["acBonus"]
            target_armor["acPenalty"] = acPenalty or target_armor["acPenalty"]
            target_armor["maxDexBonus"] = maxDexBonus or target_armor["maxDexBonus"]
            target_armor["arcaneFailureChance"] = arcaneFailureChance or target_armor["arcaneFailureChance"]
            target_armor["type"] = type_ or target_armor["type"]
            return target_armor

    # Update an existing attack based on name; supports either named 
    # arguments or a dictionary
    #
    # returns the updated attack 
    def update_attack(self,
                      name = None,
                      new_name = "",
                      attackType = None,
                      damageType = None,
                      damage = None,
                      critRoll = None,
                      critMulti = None,
                      range_ = None,
                      notes = None,
                      data = {}):
        keys = data.keys()
        if "name" in keys:
            name = data["name"]
        new_name = data["new_name"] if "new_name" in keys else new_name
        # Validate that new_name is unique
        if not self.is_unique_name(name = new_name, prop = "attacks"):
            raise ValueError("update_attack: name must be unique among attacks")
        if "attackType" in keys:
            attackType = data["attackType"]
        if "damageType" in keys:
            damageType = data["damageType"]
        if "damage" in keys:
            damage = data["damage"]
        if "critRoll" in keys:
            critRoll = data["critRoll"]
        if "critMulti" in keys:
            critMulti = data["critMulti"]
        if "range_" in keys:
            range_ = data["range_"]
        if "notes" in keys:
            notes = data["notes"]
        # Lazy selection; if there are duplicates, this will just pick 
        # up the first one that shows up
        for attack in self.attacks:
            if attack["name"] == name:
                target_attack = attack
                break
        try:
            target_attack
        except NameError:
            return None
        else:
            # Ignore empty parameters
            target_attack["name"] = new_name or target_attack["name"]
            target_attack["attackType"] = attackType or target_attack["attackType"]
            target_attack["damageType"] = damageType or target_attack["damageType"]
            target_attack["damage"] = damage or target_attack["damage"]
            target_attack["critRoll"] = critRoll or target_attack["critRoll"]
            target_attack["critMulti"] = critMulti or target_attack["critMulti"]
            target_attack["range"] = range_ or target_attack["range"]
            target_attack["notes"] = notes or target_attack["notes"]
            return target_attack

    # Update an existing skill based on name; supports either named 
    # arguments or a dictionary
    #
    # returns the updated skill 
    def update_skill(self,
                     name = None,
                     rank = None,
                     isClass = None,
                     notes = None,
                     data = {}):
        keys = data.keys()
        if "name" in keys:
            name = data["name"]
        if "rank" in keys:
            rank = data["rank"]
        if "isClass" in keys:
            isClass = data["isClass"]
        if "notes" in keys:
            notes = data["notes"]
        # Skill selection is selecting a dict key; if it doesn't error 
        # out, we're probably fine, but we'll check it just in case
        target_skill = self.skills[name]
        try:
            target_skill
        except NameError:
            return None
        else:
            # Ignore empty parameters
            target_skill["rank"] = rank or target_skill["rank"]
            target_skill["isClass"] = isClass or target_skill["isClass"]
            target_skill["notes"] = notes or target_skill["notes"]
            return target_skill

    # Update an existing skill based on name; supports either named 
    # arguments or a dictionary
    #
    # returns the updated ability dict
    def update_ability(self,
                       name = None,
                       base = None,
                       data = {}):
        keys = data.keys()
        if "name" in keys:
            name = data["name"]
        if "base" in keys:
            base = data["base"]
        # Abilities are all fixed, so selection is easy
        allowed_values = self.abilities.keys()
        if not name in allowed_values:
            raise ValueError("Character().update_ability: name must be one of " + allowed_values)
        else:
            target_ability = self.abilities[name]
        # Ignore empty parameters
        target_ability["base"] = base or target_ability["base"]
        return target_ability

    # Delete an element by name and type; supports named arguments or a 
    # dictionary
    #
    # returns the deleted element
    def delete_element(self,
                       name = None,
                       _type = None,
                       data = {}):
        valid_types = ("class",
                 "feats",
                 "traits",
                 "special",
                 "skills",
                 "equipment",
                 "attacks",
                 "armor",
                 "spells")
        keys = data.keys()
        name = data["name"] if "name" in keys else name
        _type = data["_type"] if "_type" in keys else _type

        # Ensure a valid element type
        if _type not in valid_types:
            raise ValueError("delete_element: type must be one of: " + valid_types)

        # Skills are a special case; we don't want to delete any skills 
        # that aren't craft, perform, or profession
        deletable_skills = ("Craft", "Perform", "Profession")
        valid_target = False
        if _type == "skills":
            skill_keys = self.skills.keys()
            names = [self.skills[item]["name"] for item in self.skills]
            for item in deletable_skills:
                if item in name:
                    valid_target = True
        else:
            names = [item["name"] for item in getattr(self, _type)]
            valid_target = True

        # Ensure a valid name
        if name not in names:
            raise ValueError("delete_element: name not found in element type: " + _type)
        if not valid_target:
            raise ValueError("delete_element: cannot delete skills that are not of the type: " + str(deletable_skills))

        # Remove element and return
        if _type == "skills":
            removed = getattr(self, _type).pop(name)
        else:
            index = 0
            for item in getattr(self, _type):
                if item["name"] == name:
                    break
                index = index + 1
            removed = getattr(self, _type)[index]
            del getattr(self, _type)[index]
        return removed

    # Uses the roll function to make a skill check
    #
    # Accepts an additional integer modifier (e.g. situational boosts)
    #
    # returns the roll result as an integer
    def roll_skill(self,
                   skill_name,
                   modifier = 0):
        skill_modifier = self.get_skill_value(skill_name)
        total_modifier = skill_modifier + modifier
        roll_string = "1d20+{}".format(total_modifier)
        result = roll(roll_string)
        return result
