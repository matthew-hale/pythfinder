from uuid import uuid4

"""
An object containing a name, description, and notes, with a uuid.  Used 
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

        if not uuid:
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
