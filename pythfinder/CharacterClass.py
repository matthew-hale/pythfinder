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
