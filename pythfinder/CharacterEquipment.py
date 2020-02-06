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
