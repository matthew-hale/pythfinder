from uuid import uuid4
from .vars import _ability_names

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
    
    """
    Accepts either named parameters or a dictionary of parameters; 
    treat as a 'PATCH' request
    """
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

    """
    Accepts either named parameters or a dictionary of parameters; 
    treat as a 'PATCH' request
    """
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

    """
    Accepts either named parameters or a dictionary of parameters; 
    treat as a 'PATCH' request
    """
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
