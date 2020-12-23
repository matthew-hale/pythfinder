import json
import math
import copy
from uuid import uuid4
from .helpers import remove_duplicates_by_id, remove_duplicates_by_name, numeric_filter, numeric_filter_objects
from .vars import _allowed_skill_names, _trained_only, _skill_mods, _ability_names, _saving_throw_names
from .collections import BasicItem, Ability, CharacterClass, Equipment, SavingThrow, Skill

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
        self.baseAttackBonus = data["baseAttackBonus"] if "baseAttackBonus" in keys else 0
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

        """
        Ability initialization

        Although abilities are stored as a list, they are also fixed - 
        at least, by name. There are only 6 abilities. Thus, we don't 
        have an 'add_ability' method anywhere. However, abilities are 
        still objects, so we can use their class to construct them.
        """
        self.abilities = []
        if "abilities" in keys:
            for name in _ability_names:
                target_ability_list = [a for a in data["abilities"] if a["name"] == name]
                if not target_ability_list:
                    target_ability = {
                        "name": name,
                        "base": 0,
                        "misc": []
                    }
                else:
                    target_ability = target_ability_list[0]
                subkeys = target_ability.keys()
                new_ability = {
                    "name": target_ability["name"]
                }
                new_ability["base"] = target_ability["base"] if "base" in subkeys else 0
                new_ability["misc"] = target_ability["misc"] if "misc" in subkeys else []
                self.abilities.append(Ability(data = new_ability))
        else:
            self.abilities = [
                Ability(data = {
                    "name": "str",
                    "base": 0,
                    "misc": []
                }),
                Ability(data = {
                    "name": "dex",
                    "base": 0,
                    "misc": []
                }),
                Ability(data = {
                    "name": "con",
                    "base": 0,
                    "misc": []
                }),
                Ability(data = {
                    "name": "int",
                    "base": 0,
                    "misc": []
                }),
                Ability(data = {
                    "name": "wis",
                    "base": 0,
                    "misc": []
                }),
                Ability(data = {
                    "name": "cha",
                    "base": 0,
                    "misc": []
                })
            ]

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
        self.specials = []
        #
        # If the character has no special abilities, we'll just skip it 
        # and leave it as an empty list. Otherwise, we'll want to add 
        # abilities using the BasicItem class.
        if "specials" in keys:
            for item in data["specials"]:
                self.specials.append(BasicItem(data = item))

        # Trait initialization
        #
        self.traits = []
        #
        # As above.
        if "traits" in keys:
            for item in data["traits"]:
                self.traits.append(BasicItem(data = item))

        # Feat initialization
        #
        self.feats = []
        #
        # As above.
        if "feats" in keys:
            for item in data["feats"]:
                self.feats.append(BasicItem(data = item))

        self.equipment = []
        if "equipment" in keys:
            for item in data["equipment"]:
                self.equipment.append(Equipment(data = item))

        # Saving throw initialization
        #
        self.saving_throws = []
        #
        # Saving throws are like abilities: there's only 3, and they're 
        # the same for everyone.
        if "saving_throws" in keys:
            for name in _saving_throw_names:
                target_saving_throw_list = [a for a in data["saving_throws"] if a["name"] == name]
                if not target_saving_throw_list:
                    target_saving_throw = {
                        "name": name,
                        "base": 0,
                        "misc": []
                    }
                else:
                    target_saving_throw = target_saving_throw_list[0]
                self.saving_throws.append(SavingThrow(data = target_saving_throw))
        else:
            self.saving_throws = [
                SavingThrow(data = {
                    "name": "fortitude", 
                    "base": 0,
                    "misc": []
                }),
                SavingThrow(data = {
                    "name": "reflex",
                    "base": 0,
                    "misc": []
                }),
                SavingThrow(data = {
                    "name": "will",
                    "base": 0,
                    "misc": []
                })
            ]
        
        # Skill initialization
        #
        self.skills = []
        if "skills" in keys:
            for item in data["skills"]:
                self.skills.append(Skill(data = item))

        # If there are no skills in the character data, initialize from 
        # defaults
        else:
            for skill_name in _allowed_skill_names:
                self.skills.append(Skill(data = {
                    "name": skill_name,
                    "rank": 0,
                    "is_class":  False,
                    "notes": "",
                    "misc": []
                }))

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

    """
    Returns a dict of the entire character, converting list objects 
    into dicts first
    """
    def getDict(self):
        out = copy.deepcopy(self)
        out.feats = [feat.__dict__ for feat in out.feats]
        out.traits = [trait.__dict__ for trait in out.traits]
        out.specials = [special.__dict__ for special in out.specials]
        out.equipment = [equipment.__dict__ for equipment in out.equipment]
        out.skills = [skill.get_dict() for skill in out.skills]
        out.classes = [class_.__dict__ for class_ in out.classes] # name enforcement
        out.abilities = [ability.__dict__ for ability in out.abilities]
        out.saving_throws = [saving_throw.__dict__ for saving_throw in out.saving_throws]
        return out.__dict__

    """
    Returns a formatted JSON string representation of the entire 
    character
    """
    def getJson(self):
        return json.dumps(self.getDict(), indent = 4)

    # Returns the total value of the specified skill, taking into 
    # account all of the current modifiers, including:
    #
    # + Skill ranks
    # + Class skill status
    # + Misc. skill modifiers
    # + Skill's current ability modifier
    def get_skill_value(self, skill):
        total = 0
        if skill.is_class and skill.rank >= 1:
            total += 3
        total += skill.rank
        total += sum(skill.misc)
        ability = self.get_abilities(name = skill.mod, name_search_type = "absolute")[0]# xd
        total += ability.modifier
        return total

    # Checks that the given UUID is unique within the collection
    def is_unique_id(self,
                     uuid,
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
        # Gather UUIDs from the given property, and check if 'uuid' is 
        # in the collection. If it is, it's not unique, and the 
        # function returns False; otherwise, it returns True.
        current_uuids = [item["uuid"] for item in getattr(self, prop)]
        if uuid in current_uuids:
            return False
        else:
            return True

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
        # Gather names from the given property, and check if 'name' is 
        # in the collection. If it is, it's not unique, and the 
        # function returns False; otherwise, it returns True.
        current_names = [item["name"] for item in getattr(self, prop)]
        if name in current_names:
            return False
        else:
            return True

    """
    Returns items based on given filters; multiple values for a given 
    property are treated like an 'or', while each separate property 
    is treated like an 'and'.
   
    For example:
   
    If I want to get all of the items that:
      * are currently on my person
        and
      * are either in my backpack or on my belt
    I would call this method as such:
   
    self.get_equipment(on_person = True,
                       location = ["backpack", "belt"])
   
    Numeric filters use the numeric_filter function
    """
    def get_equipment(self,
                      name_search_type = "substring",
                      name = [],
                      uuid = [],
                      weight = {},
                      count = {},
                      camp = [],
                      on_person = [],
                      location = [],
                      notes = [],
                      data = {}):
        keys = data.keys()
        # Gather values from either parameters or data, converting 
        # non-list values into lists, except for numeric values
        name = data["name"] if "name" in keys else name
        name_search_type = data["name_search_type"] if "name_search_type" in keys else name_search_type
        if not name_search_type:
            name_search_type = "substring"
        if type(name) is not list:
            name = [name]
        uuid = data["uuid"] if "uuid" in keys else uuid
        if type(uuid) is not list:
            uuid = [uuid]
        weight = data["weight"] if "weight" in keys else weight
        count = data["count"] if "count" in keys else count
        camp = data["camp"] if "camp" in keys else camp
        if type(camp) is not list:
            camp = [camp]
        on_person = data["on_person"] if "on_person" in keys else on_person
        if type(on_person) is not list:
            on_person = [on_person]
        location = data["location"] if "location" in keys else location
        if type(location) is not list:
            location = [location]
        notes = data["notes"] if "notes" in keys else notes
        if type(notes) is not list:
            notes = [notes]
        # Filter items
        items = self.equipment
        if name:
            subgroup = []
            if name_search_type == "absolute":
                for search in name:
                    for i in items:
                        if search == i.name:
                            subgroup.append(i)
            elif name_search_type == "substring":
                for search in name:
                    for i in items:
                        if search in i.name:
                            subgroup.append(i)
            else:
                raise ValueError("get_equipment: invalid name_search_type")
            items = list(set(subgroup))
        if uuid:
            subgroup = []
            for search in uuid:
                for i in items:
                    if search == i.uuid:
                        subgroup.append(i)
            items = list(set(subgroup))
        if weight:
            items = numeric_filter(items = items,
                                   key = "weight",
                                   operations = weight)
        if count:
            items = numeric_filter(items = items,
                                   key = "count",
                                   operations = count)
        if camp:
            subgroup = []
            for search in camp:
                for i in items:
                    if search == i.camp:
                        subgroup.append(i)
            items = list(set(subgroup))
        if on_person:
            subgroup = []
            for search in on_person:
                for i in items:
                    if search == i.on_person:
                        subgroup.append(i)
            items = list(set(subgroup))
        if location:
            subgroup = []
            for search in location:
                for i in items:
                    if search in i.location:
                        subgroup.append(i)
            items = list(set(subgroup))
        if notes:
            subgroup = []
            for search in notes:
                for i in items:
                    if search in i.notes:
                        subgroup.append(i)
            items = list(set(subgroup))
        return items

    # Returns abilities based on given filters; multiple values for a 
    # given property are treated like an 'or', while each separate 
    # property is treated like an 'and'.
    def get_abilities(self,
                      name_search_type = "substring",
                      name = [],
                      base = {},
                      misc = {},
                      data = {}):
        keys = data.keys()
        # Gather values from either parameters or data, converting 
        # non-list values into lists, except for numeric values
        name = data["name"] if "name" in keys else name
        name_search_type = data["name_search_type"] if "name_search_type" in keys else name_search_type
        if not name_search_type:
            name_search_type = "substring"
        if type(name) is not list:
            name = [name]
        base = data["base"] if "base" in keys else base
        misc = data["misc"] if "misc" in keys else misc
        # Filter abilities
        abilities = self.abilities
        if name:
            subgroup = []
            if name_search_type == "absolute":
                for search in name:
                    for i in abilities:
                        if search == i.name:
                            subgroup.append(i)
            elif name_search_type == "substring":
                for search in name:
                    for i in abilities:
                        if search in i.name:
                            subgroup.append(i)
            else:
                raise ValueError("get_ability: invalid name_search_type")
            abilities = list(set(subgroup))
        if base:
            abilities = numeric_filter_objects(items = abilities,
                                               attr = "base",
                                               operations = base)
        if misc:
            abilities = numeric_filter_objects(items = abilities,
                                               attr = "misc",
                                               operations = misc)
        return abilities

    # Returns saving_throws based on given filters; multiple values 
    # for a given property are treated like an 'or', while each 
    # separate property is treated like an 'and'.
    def get_saving_throw(self,
                         name_search_type = "substring",
                         name = [],
                         base = {},
                         misc = {},
                         data = {}):
        keys = data.keys()
        # Gather values from either parameters or data, converting 
        # non-list values into lists, except for numeric values
        name = data["name"] if "name" in keys else name
        name_search_type = data["name_search_type"] if "name_search_type" in keys else name_search_type
        if not name_search_type:
            name_search_type = "substring"
        if type(name) is not list:
            name = [name]
        base = data["base"] if "base" in keys else base
        misc = data["misc"] if "misc" in keys else misc
        # Filter saving_throws
        saving_throws = [throw for throw in self.saving_throws]
        if name:
            subgroup = []
            if name_search_type == "absolute":
                for search in name:
                    for i in saving_throws:
                        if search == i.name:
                            subgroup.append(i)
            elif name_search_type == "substring":
                for search in name:
                    for i in saving_throws:
                        if search in i.name:
                            subgroup.append(i)
            else:
                raise ValueError("get_saving_throw: invalid name_search_type")
            saving_throws = list(set(saving_throws))
        if base:
            saving_throws = numeric_filter(items = saving_throws,
                                       key = "base",
                                       operations = base)
        if misc:
            saving_throws = numeric_filter(items = saving_throws,
                                       key = "misc",
                                       operations = misc)
        # Convert back into a single dict, with only those saving_throws 
        # that passed the filters
        return saving_throws

    # Returns classes based on given filters; multiple values for a 
    # given property are treated like an 'or', while each separate 
    # property is treated like an 'and'.
    def get_class(self,
                  name_search_type = "substring",
                  name = [],
                  uuid = [],
                  archetypes = [],
                  level = {},
                  data = {}):
        keys = data.keys()
        # Gather values from either parameters or data, converting 
        # non-list values into lists, except for numeric values
        name = data["name"] if "name" in keys else name
        name_search_type = data["name_search_type"] if "name_search_type" in keys else name_search_type
        if not name_search_type:
            name_search_type = "substring"
        if type(name) is not list:
            name = [name]
        uuid = data["uuid"] if "uuid" in keys else uuid
        if type(uuid) is not list:
            uuid = [uuid]
        archetypes = data["archetypes"] if "archetypes" in keys else archetypes
        if type(archetypes) is not list:
            archetypes = [archetypes]
        level = data["level"] if "level" in keys else level
        # Filter classes
        classes = self.classes
        if name:
            subgroup = []
            if name_search_type == "absolute":
                for search in name:
                    for i in classes:
                        if search == i["name"]:
                            subgroup.append(i)
            elif name_search_type == "substring":
                for search in name:
                    for i in classes:
                        if search in i["name"]:
                            subgroup.append(i)
            else:
                raise ValueError("get_class: invalid name_search_type")
            classes = remove_duplicates_by_id(subgroup)
        if uuid:
            subgroup = []
            for search in uuid:
                for i in classes:
                    if search == i["uuid"]:
                        subgroup.append(i)
            classes = remove_duplicates_by_id(subgroup)
        if archetypes:
            subgroup = []
            for search in archetypes:
                for i in classes:
                    for archetype in i["archetypes"]:
                        if search in archetype:
                            subgroup.append(i)
            classes = remove_duplicates_by_id(subgroup)
        if level:
            classes = numeric_filter(items = classes,
                                     key = "level",
                                     operations = level)
        return classes


    # Returns feats based on given filters; multiple values for a given 
    # property are treated like an 'or', while each separate property 
    # is treated like an 'and'.
    def get_feats(self,
                  name_search_type = "substring",
                  name = [],
                  uuid = [],
                  description = [],
                  notes = [],
                  data = {}):
        keys = data.keys()
        # Gather values from either parameters or data, converting 
        # non-list values into lists, except for numeric values
        name = data["name"] if "name" in keys else name
        name_search_type = data["name_search_type"] if "name_search_type" in keys else name_search_type
        if not name_search_type:
            name_search_type = "substring"
        if type(name) is not list:
            name = [name]
        uuid = data["uuid"] if "uuid" in keys else uuid
        if type(uuid) is not list:
            uuid = [uuid]
        description = data["description"] if "description" in keys else description
        if type(description) is not list:
            description = [description]
        notes = data["notes"] if "notes" in keys else notes
        if type(notes) is not list:
            notes = [notes]
        # Filter feats
        feats = [feat for feat in self.feats]
        if name:
            subgroup = []
            if name_search_type == "absolute":
                for search in name:
                    for i in feats:
                        if search == i.name:
                            subgroup.append(i)
            elif name_search_type == "substring":
                for search in name:
                    for i in feats:
                        if search in i.name:
                            subgroup.append(i)
            else:
                raise ValueError("get_feat: invalid name_search_type")
            feats = list(set(subgroup))
        if uuid:
            subgroup = []
            for search in uuid:
                for i in feats:
                    if search == i.uuid:
                        subgroup.append(i)
            feats = list(set(subgroup))
        if description:
            subgroup = []
            for search in description:
                for i in feats:
                    if search in i.description:
                        subgroup.append(i)
            feats = list(set(subgroup))
        if notes:
            subgroup = []
            for search in notes:
                for i in feats:
                    if search in i.notes:
                        subgroup.append(i)
            feats = list(set(subgroup))
        return feats

    # Returns traits based on given filters; multiple values for a given 
    # property are treated like an 'or', while each separate property 
    # is treated like an 'and'.
    def get_traits(self,
                   name_search_type = "substring",
                   name = [],
                   uuid = [],
                   description = [],
                   notes = [],
                   data = {}):
        keys = data.keys()
        # Gather values from either parameters or data, converting 
        # non-list values into lists, except for numeric values
        name = data["name"] if "name" in keys else name
        name_search_type = data["name_search_type"] if "name_search_type" in keys else name_search_type
        if not name_search_type:
            name_search_type = "substring"
        if type(name) is not list:
            name = [name]
        uuid = data["uuid"] if "uuid" in keys else uuid
        if type(uuid) is not list:
            uuid = [uuid]
        description = data["description"] if "description" in keys else description
        if type(description) is not list:
            description = [description]
        notes = data["notes"] if "notes" in keys else notes
        if type(notes) is not list:
            notes = [notes]
        # Filter traits
        traits = [trait for trait in self.traits]
        if name:
            subgroup = []
            if name_search_type == "absolute":
                for search in name:
                    for i in traits:
                        if search == i.name:
                            subgroup.append(i)
            elif name_search_type == "substring":
                for search in name:
                    for i in traits:
                        if search in i.name:
                            subgroup.append(i)
            else:
                raise ValueError("get_trait: invalid name_search_type")
            traits = list(set(subgroup))
        if uuid:
            subgroup = []
            for search in uuid:
                for i in traits:
                    if search == i.uuid:
                        subgroup.append(i)
            traits = list(set(subgroup))
        if description:
            subgroup = []
            for search in description:
                for i in traits:
                    if search in i.description:
                        subgroup.append(i)
            traits = list(set(subgroup))
        if notes:
            subgroup = []
            for search in notes:
                for i in traits:
                    if search in i.notes:
                        subgroup.append(i)
            traits = list(set(subgroup))
        return traits

    # Returns specials based on given filters; multiple values for a given 
    # property are treated like an 'or', while each separate property 
    # is treated like an 'and'.
    def get_specials(self,
                     name_search_type = "substring",
                     name = [],
                     uuid = [],
                     description = [],
                     notes = [],
                     data = {}):
        keys = data.keys()
        # Gather values from either parameters or data, converting 
        # non-list values into lists, except for numeric values
        name = data["name"] if "name" in keys else name
        name_search_type = data["name_search_type"] if "name_search_type" in keys else name_search_type
        if not name_search_type:
            name_search_type = "substring"
        if type(name) is not list:
            name = [name]
        uuid = data["uuid"] if "uuid" in keys else uuid
        if type(uuid) is not list:
            uuid = [uuid]
        description = data["description"] if "description" in keys else description
        if type(description) is not list:
            description = [description]
        notes = data["notes"] if "notes" in keys else notes
        if type(notes) is not list:
            notes = [notes]
        # Filter specials
        specials = [special for special in self.specials]
        if name:
            subgroup = []
            if name_search_type == "absolute":
                for search in name:
                    for i in specials:
                        if search == i.name:
                            subgroup.append(i)
            elif name_search_type == "substring":
                for search in name:
                    for i in specials:
                        if search in i.name:
                            subgroup.append(i)
            else:
                raise ValueError("get_special: invalid name_search_type")
            specials = list(set(subgroup))
        if uuid:
            subgroup = []
            for search in uuid:
                for i in specials:
                    if search == i.uuid:
                        subgroup.append(i)
            specials = list(set(subgroup))
        if description:
            subgroup = []
            for search in description:
                for i in specials:
                    if search in i.description:
                        subgroup.append(i)
            specials = list(set(subgroup))
        if notes:
            subgroup = []
            for search in notes:
                for i in specials:
                    if search in i.notes:
                        subgroup.append(i)
            specials = list(set(subgroup))
        return specials

    # Returns skills based on given filters; multiple values for a 
    # given property are treated like an 'or', while each separate 
    # property is treated like an 'and'.
    def get_skills(self,
                   name_search_type = "substring",
                   name = [],
                   uuid = [],
                   rank = {},
                   is_class = [],
                   mod = [],
                   notes = [],
                   use_untrained = [],
                   misc = {},
                   data = {}):
        keys = data.keys()
        # Gather values from either parameters or data, converting 
        # non-list values into lists, except for numeric values
        name = data["name"] if "name" in keys else name
        name_search_type = data["name_search_type"] if "name_search_type" in keys else name_search_type
        if not name_search_type:
            name_search_type = "substring"
        if type(name) is not list:
            name = [name]
        uuid = data["uuid"] if "uuid" in keys else uuid
        if type(uuid) is not list:
            uuid = [uuid]
        rank = data["rank"] if "rank" in keys else rank
        is_class = data["is_class"] if "is_class" in keys else is_class
        if type(is_class) is not list:
            is_class = [is_class]
        mod = data["mod"] if "mod" in keys else mod
        if type(mod) is not list:
            mod = [mod]
        notes = data["notes"] if "notes" in keys else notes
        if type(notes) is not list:
            notes = [notes]
        use_untrained = data["use_untrained"] if "use_untrained" in keys else use_untrained
        if type(use_untrained) is not list:
            use_untrained = [use_untrained]
        misc = data["misc"] if "misc" in keys else misc
        # Filter skills
        skills = [skill for skill in self.skills]
        if name:
            subgroup = []
            if name_search_type == "absolute":
                for search in name:
                    for i in skills:
                        if search == i.name:
                            subgroup.append(i)
            elif name_search_type == "substring":
                for search in name:
                    for i in skills:
                        if search in i.name:
                            subgroup.append(i)
            else:
                raise ValueError("get_skill: invalid name_search_type")
            skills = list(set(subgroup))
        if uuid:
            subgroup = []
            for search in uuid:
                for i in skills:
                    if search == i.uuid:
                        subgroup.append(i)
            skills = list(set(subgroup))
        if is_class:
            subgroup = []
            for search in is_class:
                for i in skills:
                    if search == i.is_class:
                        subgroup.append(i)
            skills = list(set(subgroup))
        if mod:
            subgroup = []
            for search in mod:
                for i in skills:
                    if search in i.mod:
                        subgroup.append(i)
            skills = list(set(subgroup))
        if use_untrained:
            subgroup = []
            for search in use_untrained:
                for i in skills:
                    if search == i.use_untrained:
                        subgroup.append(i)
            skills = list(set(subgroup))
        if notes:
            subgroup = []
            for search in notes:
                for i in skills:
                    if search in i.notes:
                        subgroup.append(i)
            skills = list(set(subgroup))
        if rank:
            skills = numeric_filter(items = skills,
                                    key = "rank",
                                    operations = rank)
        if misc:
            skills = numeric_filter(items = skills,
                                    key = "misc",
                                    operations = misc)
        return skills

    # Returns spells based on given filters; multiple values for a 
    # given property are treated like an 'or', while each separate 
    # property is treated like an 'and'.
    def get_spell(self,
                  name_search_type = "substring",
                  name = [],
                  uuid = [],
                  level = {},
                  description = [],
                  prepared = {},
                  cast = {},
                  data = {}):
        keys = data.keys()
        # Gather values from either parameters or data, converting 
        # non-list values into lists, except for numeric values
        name = data["name"] if "name" in keys else name
        name_search_type = data["name_search_type"] if "name_search_type" in keys else name_search_type
        if not name_search_type:
            name_search_type = "substring"
        if type(name) is not list:
            name = [name]
        uuid = data["uuid"] if "uuid" in keys else uuid
        if type(uuid) is not list:
            uuid = [uuid]
        level = data["level"] if "level" in keys else level
        prepared = data["prepared"] if "prepared" in keys else prepared
        cast = data["cast"] if "cast" in keys else cast
        description = data["description"] if "description" in keys else description
        if type(description) is not list:
            description = [description]
        # Filter spells
        spells = self.spells
        if name:
            subgroup = []
            if name_search_type == "absolute":
                for search in name:
                    for i in spells:
                        if search == i["name"]:
                            subgroup.append(i)
            elif name_search_type == "substring":
                for search in name:
                    for i in spells:
                        if search in i["name"]:
                            subgroup.append(i)
            else:
                raise ValueError("get_spell: invalid name_search_type")
            spells = remove_duplicates_by_id(subgroup)
        if level:
            spells = numeric_filter(items = spells,
                                    key = "level",
                                    operations = level)
        if uuid:
            subgroup = []
            for search in uuid:
                for i in spells:
                    if search == i["uuid"]:
                        subgroup.append(i)
            spells = remove_duplicates_by_id(subgroup)
        if description:
            subgroup = []
            for search in description:
                for i in spells:
                    if search in i["description"]:
                        subgroup.append(i)
            spells = remove_duplicates_by_id(subgroup)
        if prepared:
            spells = numeric_filter(items = spells,
                                    key = "prepared",
                                    operations = prepared)
        if cast:
            spells = numeric_filter(items = spells,
                                    key = "cast",
                                    operations = cast)
        return spells

    # Returns armor based on given filters; multiple values for a 
    # given property are treated like an 'or', while each separate 
    # property is treated like an 'and'.
    def get_armor(self,
                  name_search_type = "substring",
                  name = [],
                  uuid = [],
                  acBonus = {},
                  acPenalty = {},
                  maxDexBonus = {},
                  arcaneFailureChance = {},
                  type_ = [],
                  data = {}):
        keys = data.keys()
        # Gather values from either parameters or data, converting 
        # non-list values into lists, except for numeric values
        name = data["name"] if "name" in keys else name
        name_search_type = data["name_search_type"] if "name_search_type" in keys else name_search_type
        if not name_search_type:
            name_search_type = "substring"
        if type(name) is not list:
            name = [name]
        uuid = data["uuid"] if "uuid" in keys else uuid
        if type(uuid) is not list:
            uuid = [uuid]
        acBonus = data["acBonus"] if "acBonus" in keys else acBonus
        acPenalty = data["acPenalty"] if "acPenalty" in keys else acPenalty
        maxDexBonus = data["maxDexBonus"] if "maxDexBonus" in keys else maxDexBonus
        arcaneFailureChance = data["arcaneFailureChance"] if "arcaneFailureChance" in keys else arcaneFailureChance
        # Filter armor
        armor = self.armor
        if name:
            subgroup = []
            if name_search_type == "absolute":
                for search in name:
                    for i in armor:
                        if search == i["name"]:
                            subgroup.append(i)
            elif name_search_type == "substring":
                for search in name:
                    for i in armor:
                        if search in i["name"]:
                            subgroup.append(i)
            else:
                raise ValueError("get_armor: invalid name_search_type")
            armor = remove_duplicates_by_id(subgroup)
        if uuid:
            subgroup = []
            for search in uuid:
                for i in armor:
                    if search == i["uuid"]:
                        subgroup.append(i)
        if acBonus:
            armor = numeric_filter(items = armor,
                                    key = "acBonus",
                                    operations = acBonus)
        if acPenalty:
            armor = numeric_filter(items = armor,
                                    key = "acPenalty",
                                    operations = acPenalty)
        if maxDexBonus:
            armor = numeric_filter(items = armor,
                                    key = "maxDexBonus",
                                    operations = maxDexBonus)
        if arcaneFailureChance:
            armor = numeric_filter(items = armor,
                                    key = "arcaneFailureChance",
                                    operations = arcaneFailureChance)
        if type_:
            subgroup = []
            for search in type_:
                for i in armor:
                    if search in i["type"]:
                        subgroup.append(i)
            armor = remove_duplicates_by_id(subgroup)
        return armor

    # Returns attacks based on given filters; multiple values for a 
    # given property are treated like an 'or', while each separate 
    # property is treated like an 'and'.
    def get_attack(self,
                   name_search_type = "substring",
                   name = [],
                   uuid = [],
                   attackType = [],
                   damageType = [],
                   attack_mod = [],
                   damage_mod = [],
                   damage = [],
                   critRoll = {},
                   critMulti = {},
                   range_ = {},
                   notes = [],
                   data = {}):
        keys = data.keys()
        # Gather values from either parameters or data, converting 
        # non-list values into lists, except for numeric values
        name = data["name"] if "name" in keys else name
        name_search_type = data["name_search_type"] if "name_search_type" in keys else name_search_type
        if not name_search_type:
            name_search_type = "substring"
        if type(name) is not list:
            name = [name]
        uuid = data["uuid"] if "uuid" in keys else uuid
        if type(uuid) is not list:
            uuid = [uuid]
        attackType = data["attackType"] if "attackType" in keys else attackType
        if type(attackType) is not list:
            attackType = [attackType]
        damageType = data["damageType"] if "damageType" in keys else damageType
        if type(damageType) is not list:
            damageType = [damageType]
        attack_mod = data["attack_mod"] if "attack_mod" in keys else attack_mod
        if type(attack_mod) is not list:
            attack_mod = [attack_mod]
        damage_mod = data["damage_mod"] if "damage_mod" in keys else damage_mod
        if type(damage_mod) is not list:
            damage_mod = [damage_mod]
        damage = data["damage"] if "damage" in keys else damage
        if type(damage) is not list:
            damage = [damage]
        critRoll = data["critRoll"] if "critRoll" in keys else critRoll
        critMulti = data["critMulti"] if "critMulti" in keys else critMulti
        range_ = data["range"] if "range" in keys else range_
        notes = data["notes"] if "notes" in keys else notes
        if type(notes) is not list:
            notes = [notes]
        # Filter attacks
        attacks = self.attacks
        if name:
            subgroup = []
            if name_search_type == "absolute":
                for search in name:
                    for i in attacks:
                        if search == i["name"]:
                            subgroup.append(i)
            elif name_search_type == "substring":
                for search in name:
                    for i in attacks:
                        if search in i["name"]:
                            subgroup.append(i)
            else:
                raise ValueError("get_attack: invalid name_search_type")
            attacks = remove_duplicates_by_id(subgroup)
        if uuid:
            subgroup = []
            for search in uuid:
                for i in attacks:
                    if search == i["uuid"]:
                        subgroup.append(i)
            attacks = remove_duplicates_by_id(subgroup)
        if attackType:
            subgroup = []
            for search in attackType:
                for i in attacks:
                    if search in i["attackType"]:
                        subgroup.append(i)
            attacks = remove_duplicates_by_id(subgroup)
        if damageType:
            subgroup = []
            for search in damageType:
                for i in attacks:
                    if search in i["damageType"]:
                        subgroup.append(i)
            attacks = remove_duplicates_by_id(subgroup)
        if attack_mod:
            subgroup = []
            for search in attack_mod:
                for i in attacks:
                    if search in i["attack_mod"]:
                        subgroup.append(i)
            attacks = remove_duplicates_by_id(subgroup)
        if damage_mod:
            subgroup = []
            for search in damage_mod:
                for i in attacks:
                    if search in i["damage_mod"]:
                        subgroup.append(i)
            attacks = remove_duplicates_by_id(subgroup)
        if damage:
            subgroup = []
            for search in damage:
                for i in attacks:
                    if search in i["damage"]:
                        subgroup.append(i)
            attacks = remove_duplicates_by_id(subgroup)
        if critRoll:
            attacks = numeric_filter(items = attacks,
                                   key = "critRoll",
                                   operations = critRoll)
        if critMulti:
            attacks = numeric_filter(items = attacks,
                                   key = "critMulti",
                                   operations = critMulti)
        if range_:
            attacks = numeric_filter(items = attacks,
                                   key = "range",
                                   operations = range_)
        return attacks

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
        new_archetypes = data["archetypes"] if "archetypes" in keys else archetypes
        new_level = data["level"] if "level" in keys else level
        new_class = CharacterClass(name = new_name,
                                   archetypes = new_archetypes,
                                   level = new_level)
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
        new_description = data["description"] if "description" in keys else description
        new_notes = data["notes"] if "notes" in keys else notes
        new_feat = BasicItem(name = new_name,
                             description = new_description,
                             notes = new_notes)
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
        new_description = data["description"] if "description" in keys else description
        new_notes = data["notes"] if "notes" in keys else notes
        new_trait = BasicItem(name = new_name,
                              description = new_description,
                              notes = new_notes)
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
        new_description = data["description"] if "description" in keys else description
        new_notes = data["notes"] if "notes" in keys else notes
        new_special = BasicItem(name = new_name,
                                description = new_description,
                                notes = new_notes)
        self.specials.append(new_special)
        return new_special

    # Add a skill to the character (craft, profession, and perform); 
    # supports either named arguments or a dictionary
    # 
    # returns the newly created skill
    def add_skill(self,
                  name = "",
                  uuid = "",
                  rank = 0,
                  is_class = False, 
                  notes = "",
                  misc = [],
                  data = {}):
        # Handle skills with variable names
        valid_names = ("Perform", "Profession", "Craft")
        skill_type = ""
        keys = data.keys()
        new_name = data["name"] if "name" in keys else name
        new_uuid = data["uuid"] if "uuid" in keys else uuid
        if not new_uuid:
            new_uuid = uuid4()
        # Validate that new_uuid is unique
        if not self.is_unique_id(uuid = new_uuid, prop = "skills"):
            raise ValueError("add_skill: uuid must be unique among skills")
        # Validate skill name is in allowed_skills
        # If so, we can use all the built-in values for things
        if new_name in _allowed_skill_names:
            new_mod = _skill_mods[new_name]
            if new_name in _trained_only:
                new_use_untrained = False
            else:
                new_use_untrained = True
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
                new_use_untrained = False
            else:
                new_use_untrained = True
            new_mod = _skill_mods[skill_type]
        # Get the rest of the properties
        new_rank = data["rank"] if "rank" in keys else rank
        new_is_class = data["is_class"] if "is_class" in keys else is_class
        new_notes = data["notes"] if "notes" in keys else notes
        new_misc = data["misc"] if "misc" in keys else misc
        new_skill = {
            "name": new_name,
            "uuid": str(new_uuid),
            "rank": new_rank,
            "is_class": new_is_class,
            "mod": new_mod,
            "notes": new_notes,
            "use_untrained": new_use_untrained,
            "misc": new_misc,
        }
        self.skills.append(new_skill)
        return new_skill


    # Add a new item to the character; supports either named arguments 
    # or a dictionary
    #
    # returns the newly created item
    def add_equipment(self,
                      name = "",
                      weight = 0.0,
                      count = 0,
                      camp = False,
                      on_person = False,
                      location = "",
                      notes = "",
                      data = {}):
        keys = data.keys()
        new_name = data["name"] if "name" in keys else name
        new_weight = data["weight"] if "weight" in keys else weight
        new_count = data["count"] if "count" in keys else count
        new_camp = data["camp"] if "camp" in keys else camp
        new_on_person = data["on_person"] if "on_person" in keys else on_person
        new_location = data["location"] if "location" in keys else location
        new_notes = data["notes"] if "notes" in keys else notes
        new_equipment = Equipment(name = new_name,
                                  weight = new_weight,
                                  count = new_count,
                                  camp = new_camp,
                                  on_person = new_on_person,
                                  location = new_location,
                                  notes = new_notes)
        self.equipment.append(new_equipment)
        return new_equipment

    # Add a new attack to the character; supports either named 
    # arguments or a dictionary
    #
    # returns the newly created attack
    def add_attack(self,
                   name = "",
                   uuid = "",
                   attackType = "",
                   damageType = "",
                   # default to str for mods so that attack creation 
                   # does not fail if not provided
                   attack_mod = "str",
                   damage_mod = "str", 
                   damage = "",
                   critRoll = 20,
                   critMulti = 2,
                   range_ = 0,
                   notes = "",
                   data = {}):
        keys = data.keys()
        new_name = data["name"] if "name" in keys else name
        new_uuid = data["uuid"] if "uuid" in keys else uuid
        if not new_uuid:
            new_uuid = uuid4()
        # Validate that new_uuid is unique
        if not self.is_unique_id(uuid = new_uuid, prop = "attacks"):
            raise ValueError("add_attack: uuid must be unique among attacks")
        new_attackType = data["attackType"] if "attackType" in keys else attackType
        new_damageType = data["damageType"] if "damageType" in keys else damageType
        new_attack_mod = data["attack_mod"] if "attack_mod" in keys else attack_mod
        new_damage_mod = data["damage_mod"] if "damage_mod" in keys else damage_mod
        # Ensure valid mod for attack & damage
        if new_attack_mod not in _ability_names:
            raise ValueError("add_attack: attack_mod not an allowed modifier")
        if new_damage_mod not in _ability_names:
            raise ValueError("add_attack: damage_mod not an allowed modifier")
        new_damage = data["damage"] if "damage" in keys else damage
        new_critRoll = data["critRoll"] if "critRoll" in keys else critRoll
        new_critMulti = data["critMulti"] if "critMulti" in keys else critMulti
        new_range = data["range"] if "range" in keys else range_
        new_notes = data["notes"] if "notes" in keys else notes
        new_attack = {
            "name": new_name,
            "uuid": str(new_uuid),
            "attackType": new_attackType,
            "damageType": new_damageType,
            "attack_mod": new_attack_mod,
            "damage_mod": new_damage_mod,
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
                  uuid = "",
                  acBonus = 0,
                  acPenalty = 0,
                  maxDexBonus = 0,
                  arcaneFailureChance = 0,
                  type_ = "",
                  data = {}):
        keys = data.keys()
        new_name = data["name"] if "name" in keys else name
        new_uuid = data["uuid"] if "uuid" in keys else uuid
        if not new_uuid:
            new_uuid = uuid4()
        # Validate that new_uuid is unique
        if not self.is_unique_id(uuid = new_uuid, prop = "armor"):
            raise ValueError("add_armor: uuid must be unique among armors")
        new_acBonus = data["acBonus"] if "acBonus" in keys else acBonus
        new_acPenalty = data["acPenalty"] if "acPenalty" in keys else acPenalty
        new_maxDexBonus = data["maxDexBonus"] if "maxDexBonus" in keys else maxDexBonus
        new_arcaneFailureChance = data["arcaneFailureChance"] if "arcaneFailureChance" in keys else arcaneFailureChance
        new_type = data["type"] if "type" in keys else type_
        new_armor = {
            "name": new_name,
            "uuid": str(new_uuid),
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
                  uuid = "",
                  level = 0,
                  description = "",
                  prepared = 0,
                  cast = 0,
                  data = {}):
        keys = data.keys()
        new_name = data["name"] if "name" in keys else name
        new_uuid = data["uuid"] if "uuid" in keys else uuid
        if not new_uuid:
            new_uuid = uuid4()
        # Validate that new_uuid is unique
        if not self.is_unique_id(uuid = new_uuid, prop = "spells"):
            raise ValueError("add_spell: uuid must be unique among spells")
        new_level = data["level"] if "level" in keys else level
        new_description = data["description"] if "description" in keys else description
        new_prepared = data["prepared"] if "prepared" in keys else prepared
        new_cast = data["cast"] if "cast" in keys else cast
        new_spell = {
            "name": new_name,
            "uuid": str(new_uuid),
            "level": new_level,
            "description": new_description,
            "prepared": new_prepared,
            "cast": new_cast,
        }
        self.spells.append(new_spell)
        return new_spell

    # Update an existing spell based on uuid; supports either named 
    # arguments or a dictionary
    #
    # returns the updated spell 
    def update_spell(self,
                     uuid = "",
                     name = None,
                     level = None,
                     description = None,
                     prepared = None,
                     cast = None,
                     data = {}):
        keys = data.keys()
        uuid = data["uuid"] if "uuid" in keys else uuid
        name = data["name"] if "name" in keys else name
        level = data["level"] if "level" in keys else level
        description = data["description"] if "description" in keys else description
        prepared = data["prepared"] if "prepared" in keys else prepared
        cast = data["cast"] if "cast" in keys else cast
        # Get target spell
        target_list = self.get_spell(uuid = uuid)
        if not target_list:
            raise ValueError("update_spell: no spell found with uuid '{}'".format(uuid))
        else:
            target = target_list[0]
        # Ignore parameters not provided, allowing for "falsey" values
        if name is not None:
            target["name"] = name
        if level is not None:
            target["level"] = level
        if prepared is not None:
            target["prepared"] = prepared
        if cast is not None:
            target["cast"] = cast
        if description is not None:
            target["description"] = description
        return target

    # Update an existing piece of armor based on uuid; supports either 
    # named arguments or a dictionary
    #
    # returns the updated armor
    def update_armor(self,
                     uuid = "",
                     name = None,
                     acBonus = None,
                     acPenalty = None,
                     maxDexBonus = None,
                     arcaneFailureChance = None,
                     type_ = None,
                     data = {}):
        keys = data.keys()
        uuid = data["uuid"] if "uuid" in keys else uuid
        name = data["name"] if "name" in keys else name
        acBonus = data["acBonus"] if "acBonus" in keys else acBonus
        acPenalty = data["acPenalty"] if "acPenalty" in keys else acPenalty
        maxDexBonus = data["maxDexBonus"] if "maxDexBonus" in keys else maxDexBonus
        arcaneFailureChance = data["arcaneFailureChance"] if "arcaneFailureChance" in keys else arcaneFailureChance
        type_ = data["type"] if "type" in keys else type_
        # Get target armor
        target_list = self.get_armor(uuid = uuid)
        if not target_list:
            raise ValueError("update_armor: no armor found with uuid '{}'".format(uuid))
        else:
            target = target_list[0]
        # Ignore parameters not provided, allowing for "falsey" values
        if name is not None:
            target["name"] = name
        if acBonus is not None:
            target["acBonus"] = acBonus
        if acPenalty is not None:
            target["acPenalty"] = acPenalty
        if maxDexBonus is not None:
            target["maxDexBonus"] = maxDexBonus
        if arcaneFailureChance is not None:
            target["arcaneFailureChance"] = arcaneFailureChance
        if type_ is not None:
            target["type"] = type_
        return target

    # Update an existing attack based on uuid; supports either named 
    # arguments or a dictionary
    #
    # returns the updated attack 
    def update_attack(self,
                      uuid = "",
                      name = None,
                      attackType = None,
                      damageType = None,
                      damage = None,
                      attack_mod = None,
                      damage_mod = None,
                      critRoll = None,
                      critMulti = None,
                      range_ = None,
                      notes = None,
                      data = {}):
        keys = data.keys()
        allowed_mods = self.abilities.keys()
        uuid = data["uuid"] if "uuid" in keys else uuid
        name = data["name"] if "name" in keys else name
        attackType = data["attackType"] if "attackType" in keys else attackType
        damageType = data["damageType"] if "damageType" in keys else damageType
        damage = data["damage"] if "damage" in keys else damage
        attack_mod = data["attack_mod"] if "attack_mod" in keys else attack_mod
        damage_mod = data["damage_mod"] if "damage_mod" in keys else damage_mod
        critRoll = data["critRoll"] if "critRoll" in keys else critRoll
        critMulti = data["critMulti"] if "critMulti" in keys else critMulti
        range_ = data["range"] if "range" in keys else range_
        notes = data["notes"] if "notes" in keys else notes
        # Get target attack
        target_list = self.get_attack(uuid = uuid)
        if not target_list:
            raise ValueError("update_attack: no attack found with uuid '{}'".format(uuid))
        else:
            target = target_list[0]
        # Ignore parameters not provided, allowing for "falsey" values
        if name is not None:
            target["name"] = name
        if attackType is not None:
            target["attackType"] = attackType
        if damageType is not None:
            target["damageType"] = damageType
        if damage is not None:
            target["damage"] = damage
        if attack_mod is not None:
            # validate mods
            if attack_mod in allowed_mods:
                target["attack_mod"] = attack_mod
            else:
                raise ValueError("update_attack: attack_mod '{}' not an allowed modifier".format(attack_mod))
        if damage_mod is not None:
            if attack_mod in allowed_mods:
                target["damage_mod"] = damage_mod
            else:
                raise ValueError("update_attack: damage_mod '{}' not an allowed modifier".format(damage_mod))
        if critRoll is not None:
            target["critRoll"] = critRoll
        if critMulti is not None:
            target["critMulti"] = critMulti
        if range_ is not None:
            target["range"] = range_
        if notes is not None:
            target["notes"] = notes
        return target

    # Delete a class by uuid
    def delete_class(self,
                     character_class):
        try:
            self.classes.remove(character_class)
        except ValueError as err:
            raise ValueError("delete_class: {}".format(err))
        return character_class

    # Delete a feat
    def delete_feat(self,
                    feat):
        try:
            self.feats.remove(feat)
        except ValueError as err:
            raise ValueError("delete_feat: {}".format(err))
        return feat

    # Delete a trait
    def delete_trait(self,
                     trait):
        try:
            self.traits.remove(trait)
        except ValueError as err:
            raise ValueError("delete_trait: {}".format(err))
        return trait

    # Delete a special
    def delete_special(self,
                       special):
        try:
            self.specials.remove(special)
        except ValueError as err:
            raise ValueError("delete_special: {}".format(err))
        return special

    # Delete a skill by uuid
    #
    # only deletes skills that a character can normally have multiple 
    # of, e.g. Craft, Profession, Perform
    def delete_skill(self,
                     skill):
        try:
            self.skills.remove(skill)
        except ValueError as err:
            raise ValueError("delete_skill: {}".format(err))
        return skill

    # Delete a piece of equipment
    def delete_equipment(self,
                         equipment):
        try:
            self.equipment.remove(equipment)
        except ValueError as err:
            raise ValueError("delete_equipment: {}".format(err))
        return equipment

    # Delete an attack by uuid
    def delete_attack(self,
                      uuid):
        # Ensure a valid target
        target_list = self.get_attack(uuid = uuid)
        if not target_list:
            raise ValueError("delete_attack: no attack with uuid '{}'".format(uuid))
        else:
            target = target_list[0]
        # Delete target
        self.attacks.remove(target)

    # Delete a piece of armor by uuid
    def delete_armor(self,
                     uuid):
        # Ensure a valid target
        target_list = self.get_armor(uuid = uuid)
        if not target_list:
            raise ValueError("delete_armor: no armor with uuid '{}'".format(uuid))
        else:
            target = target_list[0]
        # Delete target
        self.armor.remove(target)

    # Delete a spell by uuid
    def delete_spell(self,
                      uuid):
        # Ensure a valid target
        target_list = self.get_spell(uuid = uuid)
        if not target_list:
            raise ValueError("delete_spell: no spell with uuid '{}'".format(uuid))
        else:
            target = target_list[0]
        # Delete target
        self.spells.remove(target)

    # Set items' "on_person" flags to False if they are also flagged 
    # as "camp" items.
    def set_up_camp(self):
        camp_items = self.get_equipment(camp = True)
        for item in camp_items:
            item["on_person"] = False

    # Set items' "on_person" flags to True if they are also flagged 
    # as "camp" items.
    def tear_down_camp(self):
        camp_items = self.get_equipment(camp = True)
        for item in camp_items:
            item["on_person"] = True
