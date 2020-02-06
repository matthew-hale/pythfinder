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
