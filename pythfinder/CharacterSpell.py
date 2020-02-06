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
