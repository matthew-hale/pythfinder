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
    
    # Compare attributes excluding uuid
    def __eq__(self, other):
        if not isinstance(other, BasicItem):
            return NotImplemented
        keys = ["name", "description", "notes"]
        return all([getattr(self, key) == getattr(other, key) for key in keys])

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
        # Validate abiltiy name
        if self.name not in _ability_names:
            raise ValueError("Ability.__init__: '{}' not an allowed ability name".format(self.name))

    @property
    def modifier(self):
        total = self.base + sum(self.misc)
        if total <= 1:
            return -5
        else:
            return math.floor(0.5 * total - 5) # total modifier equation

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

    # Compare attributes excluding uuid
    def __eq__(self, other):
        if not isinstance(other, CharacterClass):
            return NotImplemented
        return self.name == other.name and \
        self.level == other.level and \
        self.archetypes == other.archetypes

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

    # Compare attributes excluding uuid
    def __eq__(self, other):
        if not isinstance(other, Equipment):
            return NotImplemented
        keys = ["name", "weight", "count", "camp", "on_person", "location", "notes"]
        return all([getattr(self, key) == getattr(other, key) for key in keys])

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
