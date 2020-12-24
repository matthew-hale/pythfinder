from uuid import uuid4
from .vars import _ability_names, _saving_throw_names, _allowed_skill_names, _trained_only, _skill_mods

_valid_names = ("Perform", "Profession", "Craft")

"""
An object containing a name, description, and notes, with a uuid. Used 
for feats, traits, and special abilities, as they all share this 
structure.
"""
class BasicItem:
    def __init__(self,
                 name = "",
                 uuid = "",
                 description = "",
                 notes = "",
                 data = {}):
        keys = data.keys()
        self.name = data["name"] if "name" in keys else name
        self.description = data["description"] if "description" in keys else description
        self.notes = data["notes"] if "notes" in keys else notes
        self.uuid = data["uuid"] if "uuid" in keys else uuid

        if not self.uuid:
            self.uuid = str(uuid4())
    
    # Accepts either named parameters or a dictionary of parameters; 
    # treat as a 'PATCH' request
    def update(self,
               name = None,
               description = None,
               notes = None,
               data = {}):
        keys = data.keys()
        name = data["name"] if "name" in keys else name
        description = data["description"] if "description" in keys else description
        notes = data["notes"] if "notes" in keys else notes
        # Ignore parameters not provided, allowing for "falsey" values
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if notes is not None:
            self.notes = notes
        return self

"""
An object containing a name, a base value, and 0 or more modifiers. 
Used to represent a character's ability scores.

As every character has a fixed set of abilities, there are no UUIDs.
"""
class Ability:
    def __init__(self,
                 name = "",
                 base = 0,
                 misc = [],
                 data = {}):
        keys = data.keys()
        self.name = data["name"] if "name" in keys else name
        self.base = data["base"] if "base" in keys else base
        self.misc = data["misc"] if "misc" in keys else misc

    # Validate ability name
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value not in _ability_names:
            raise ValueError("Ability.__init__: '{}' not an allowed ability value".format(self.value))
        self._name = value

    @property
    def modifier(self):
        total = self.base + sum(self.misc)
        if total <= 1:
            return -5
        else:
            return math.floor(0.5 * total - 5) # total modifier equation

    def get_dict(self):
        return {
            "name": self.name,
            "base": self.base,
            "misc": self.misc
        }

    # Accepts either named parameters or a dictionary of parameters; 
    # treat as a 'PATCH' request
    def update(self,
               base = None,
               misc = None,
               data = {}):
        keys = data.keys()
        base = data["base"] if "base" in keys else base
        misc = data["misc"] if "misc" in keys else misc
        # Ignore parameters not provided, allowing for "falsey" values
        if base is not None:
            self.base = base
        if misc is not None:
            self.misc = misc
        return self

"""
An object containing a name, level, and one or more archetypes, with a 
uuid. Used to represent the class(es) that the character has levels in.
"""
class CharacterClass:
    def __init__(self,
                 name = "",
                 uuid = "",
                 level = 0,
                 archetypes = [],
                 data = {}):
        keys = data.keys()
        self.name = data["name"] if "name" in keys else name
        self.uuid = data["uuid"] if "uuid" in keys else uuid
        self.level = data["level"] if "level" in keys else level
        self.archetypes = data["archetypes"] if "archetypes" in keys else archetypes

        if not self.uuid:
            self.uuid = str(uuid4())

    # Accepts either named parameters or a dictionary of parameters; 
    # treat as a 'PATCH' request
    def update(self,
               level = None,
               archetypes = None,
               data = {}):
        keys = data.keys()
        level = data["level"] if "level" in keys else level
        archetypes = data["archetypes"] if "archetypes" in keys else archetypes
        # Ignore parameters not provided, allowing for "falsey" values
        if level is not None:
            self.level = level
        if archetypes is not None:
            self.archetypes = archetypes
        return self

"""
An object representing a piece of equipment owned by the character. 
Equipment has a per-unit weight, and a count; a location value; an 
'on_person' flag; and a flag to determine whether or not to leave it 
behind when the player makes camp.
"""
class Equipment:
    def __init__(self,
                 name = "",
                 uuid = "",
                 weight = 0.0,
                 count = 0,
                 camp = False,
                 on_person = False,
                 location = "",
                 notes = "",
                 data = {}):
        keys = data.keys()
        self.name = data["name"] if "name" in keys else name
        self.weight = data["weight"] if "weight" in keys else weight
        self.count = data["count"] if "count" in keys else count
        self.camp = data["camp"] if "camp" in keys else camp
        self.on_person = data["on_person"] if "on_person" in keys else on_person
        self.location = data["location"] if "location" in keys else location
        self.notes = data["notes"] if "notes" in keys else notes
        self.uuid = data["uuid"] if "uuid" in keys else uuid

        if not self.uuid:
            self.uuid = str(uuid4())

    # Accepts either named parameters or a dictionary of parameters; 
    # treat as a 'PATCH' request
    def update(self,
               name = None,
               weight = None,
               count = None,
               camp = None,
               on_person = None,
               location = None,
               notes = None,
               data = {}):
        keys = data.keys()
        name = data["name"] if "name" in keys else name
        weight = data["weight"] if "weight" in keys else weight
        count = data["count"] if "count" in keys else count
        camp = data["camp"] if "camp" in keys else camp
        on_person = data["on_person"] if "on_person" in keys else on_person
        location = data["location"] if "location" in keys else location
        notes = data["notes"] if "notes" in keys else notes
        # Ignore parameters not provided, allowing for "falsey" values
        if name is not None:
            self.name = name
        if weight is not None:
            self.weight = weight
        if count is not None:
            self.count = count
        if camp is not None:
            self.camp = camp
        if on_person is not None:
            self.on_person = on_person
        if location is not None:
            self.location = location
        if notes is not None:
            self.notes = notes
        return self

"""
Similar in structure to an Ability, but with a different purpose.
"""
class SavingThrow:
    def __init__(self,
                 name = "",
                 base = 0,
                 misc = [],
                 data = {}):
        keys = data.keys()
        self.name = data["name"] if "name" in keys else name
        self.base = data["base"] if "base" in keys else base
        self.misc = data["misc"] if "misc" in keys else misc
        # Validate saving throw name
        if self.name not in _saving_throw_names:
            raise ValueError("SavingThrow.__init__: '{}' not an allowed saving throw name".format(self.name))

    # Accepts either named parameters or a dictionary of parameters; 
    # treat as a 'PATCH' request
    def update(self,
               base = None,
               misc = None,
               data = {}):
        keys = data.keys()
        base = data["base"] if "base" in keys else base
        misc = data["misc"] if "misc" in keys else misc
        # Ignore parameters not provided, allowing for "falsey" values
        if base is not None:
            self.base = base
        if misc is not None:
            self.misc = misc
        return self

"""
Contains a rank, one or more misc modifiers, and a flag to determine if 
it's a "class" skill.
"""
class Skill:
    def __init__(self,
                 name = "",
                 uuid = "",
                 rank = 0,
                 is_class = False, 
                 notes = "",
                 misc = [],
                 use_untrained = "",
                 mod = "",
                 data = {}):
        keys = data.keys()
        self._name = data["name"] if "name" in keys else name
        self.rank = data["rank"] if "rank" in keys else rank
        self.is_class = data["is_class"] if "is_class" in keys else is_class
        self.notes = data["notes"] if "notes" in keys else notes
        self.misc = data["misc"] if "misc" in keys else misc
        self.use_untrained = data["use_untrained"] if "use_untrained" in keys else use_untrained
        self.mod = data["mod"] if "mod" in keys else mod
        self.uuid = data["uuid"] if "uuid" in keys else uuid
        if not self.use_untrained:
            if self._name in _trained_only:
                self.use_untrained = False
            else:
                self.use_untrained = True
        if not self.mod:
            self.mod = _skill_mods[self._name]

        if not self.uuid:
            self.uuid = str(uuid4())

    # We want a "name" key, not a "_name" key
    def get_dict(self):
        return {
            "name": self._name,
            "rank": self.rank,
            "is_class": self.is_class,
            "notes": self.notes,
            "misc": self.misc,
            "uuid": self.uuid
        }

    # Enforce name rules
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value not in _allowed_skill_names and \
           all([n not in value for n in _valid_names]):
            raise ValueError("Skill.__init__: '{}' not a valid skill value".format(value))
        self._name = value

    # Accepts either named parameters or a dictionary of parameters; 
    # treat as a 'PATCH' request
    def update(self,
               name = None,
               rank = None,
               is_class = None,
               notes = None,
               misc = None,
               data = {}):
        keys = data.keys()
        name = data["name"] if "name" in keys else name
        rank = data["rank"] if "rank" in keys else rank
        is_class = data["is_class"] if "is_class" in keys else is_class
        notes = data["notes"] if "notes" in keys else notes
        misc = data["misc"] if "misc" in keys else misc
        # Ignore parameters not provided, allowing for "falsey" values
        if name is not None:
            self.name = name
        if rank is not None:
            self.rank = rank
        if is_class is not None:
            self.is_class = is_class
        if notes is not None:
            self.notes = notes
        if misc is not None:
            self.misc = misc
        return self

class Spell:
    def __init__(self,
                 name = "",
                 uuid = "",
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
        self.uuid = data["uuid"] if "uuid" in keys else uuid

        if not self.uuid:
            self.uuid = str(uuid4())

    def update(self,
               name = None,
               level = None,
               description = None,
               prepared = None,
               cast = None,
               data = {}):
        keys = data.keys()
        name = data["name"] if "name" in keys else name
        level = data["level"] if "level" in keys else level
        description = data["description"] if "description" in keys else description
        prepared = data["prepared"] if "prepared" in keys else prepared
        cast = data["cast"] if "cast" in keys else cast
        # Ignore parameters not provided, allowing for "falsey" values
        if name is not None:
            self.name = name
        if level is not None:
            self.level = level
        if description is not None:
            self.description = description
        if prepared is not None:
            self.prepared = prepared
        if cast is not None:
            self.cast = cast
        return self

class Attack:
    def __init__(self,
                 name = "",
                 uuid = "",
                 attack_type = "",
                 damage_type = "",
                 # default to str for mods so that attack creation 
                 # does not fail if not provided
                 attack_mod = "str",
                 damage_mod = "str",
                 damage = "",
                 crit_roll = 20,
                 crit_multi = 2,
                 range_ = 0,
                 notes = "",
                 data = {}):
        keys = data.keys()
        self.name = data["name"] if "name" in keys else name
        self.attack_type = data["attack_type"] if "attack_type" in keys else attack_type
        self.damage_type = data["damage_type"] if "damage_type" in keys else damage_type
        self.attack_mod = data["attack_mod"] if "attack_mod" in keys else attack_mod
        self.damage_mod = data["damage_mod"] if "damage_mod" in keys else damage_mod
        self.damage = data["damage"] if "damage" in keys else damage
        self.crit_roll = data["crit_roll"] if "crit_roll" in keys else crit_roll
        self.crit_multi = data["crit_multi"] if "crit_multi" in keys else crit_multi
        self.range = data["range"] if "range" in keys else range_
        self.notes = data["notes"] if "notes" in keys else notes
        self.uuid = data["uuid"] if "uuid" in keys else uuid

        if not self.uuid:
            self.uuid = str(uuid4())

    # Validate ability name
    @property
    def attack_mod(self):
        return self._attack_mod

    @attack_mod.setter
    def attack_mod(self, value):
        if value not in _ability_names:
            raise ValueError("Attack.attack_mod: '{}' not a valid ability name".format(value))
        self._attack_mod = value

    @property
    def damage_mod(self):
        return self._damage_mod

    @damage_mod.setter
    def damage_mod(self, value):
        if value not in _ability_names:
            raise ValueError("Attack.damage_mod: '{}' not a valid ability name".format(value))
        self._damage_mod = value

    def get_dict(self):
        return {
            "name": self.name,
            "attack_type": self.attack_type,
            "damage_type": self.damage_type,
            "attack_mod": self.attack_mod,
            "damage_mod": self.damage_mod,
            "damage": self.damage,
            "crit_roll": self.crit_roll,
            "crit_multi": self.crit_multi,
            "range": self.range,
            "notes": self.notes,
            "uuid": self.uuid
        }

    def update(self,
               name = None,
               attack_type = None,
               damage_type = None,
               attack_mod = None,
               damage_mod = None,
               damage = None,
               crit_roll = None,
               crit_multi = None,
               range_ = None,
               notes = None,
               data = {}):
        keys = data.keys()
        name = data["name"] if "name" in keys else name
        # Ignore parameters not provided, allowing for "falsey" values
        if name is not None:
            self.name = name
        if attack_type is not None:
            self.attack_type = attack_type
        if damage_type is not None:
            self.damage_type = damage_type
        if attack_mod is not None:
            self.attack_mod = attack_mod
        if damage_mod is not None:
            self.damage_mod = damage_mod
        if damage is not None:
            self.damage = damage
        if crit_roll is not None:
            self.crit_roll = crit_roll
        if crit_multi is not None:
            self.crit_multi = crit_multi
        if range_ is not None:
            self.range = range_
        if notes is not None:
            self.notes = notes
        return self

class Armor:
    def __init__(self,
                 name = "",
                 uuid = "",
                 ac_bonus = 0,
                 ac_penalty = 0,
                 max_dex_bonus = 0,
                 arcane_failure_chance = 0,
                 type_ = "",
                 data = {}):
        keys = data.keys()
        self.name = data["name"] if "name" in keys else name
        self.ac_bonus = data["ac_bonus"] if "ac_bonus" in keys else ac_bonus
        self.ac_penalty = data["ac_penalty"] if "ac_penalty" in keys else ac_penalty
        self.max_dex_bonus = data["max_dex_bonus"] if "max_dex_bonus" in keys else max_dex_bonus
        self.arcane_failure_chance = data["arcane_failure_chance"] if "arcane_failure_chance" in keys else arcane_failure_chance
        self.type = data["type"] if "type" in keys else type_
        self.uuid = data["uuid"] if "uuid" in keys else uuid

        if not self.uuid:
            self.uuid = str(uuid4())

    def update(self,
               name = None,
               ac_bonus = None,
               ac_penalty = None,
               max_dex_bonus = None,
               arcane_failure_chance = None,
               type_ = None,
               data = {}):
        keys = data.keys()
        name = data["name"] if "name" in keys else name
        ac_bonus = data["ac_bonus"] if "ac_bonus" in keys else ac_bonus
        ac_penalty = data["ac_penalty"] if "ac_penalty" in keys else ac_penalty
        max_dex_bonus = data["max_dex_bonus"] if "max_dex_bonus" in keys else max_dex_bonus
        arcane_failure_chance = data["arcane_failure_chance"] if "arcane_failure_chance" in keys else arcane_failure_chance
        type_ = data["type"] if "type" in keys else type_
        # Ignore parameters not provided, allowing for "falsey" values
        if name is not None:
            self.name = name
        if ac_bonus is not None:
            self.ac_bonus = ac_bonus
        if ac_penalty is not None:
            self.ac_penalty = ac_penalty
        if max_dex_bonus is not None:
            self.max_dex_bonus = max_dex_bonus
        if arcane_failure_chance is not None:
            self.arcane_failure_chance = arcane_failure_chance
        if type_ is not None:
            self.type = type_
        return self
