class CharacterHP:
    def __init__(self,
                 max_ = 0,
                 current = 0,
                 temporary = 0,
                 nonlethal = 0,
                 data = {}):
        keys = data.keys()
        self.max = data["max"] if "max" in keys else max_
        self.current = data["current"] if "current" in keys else current
        self.temporary = data["temporary"] if "temporary" in keys else temporary
        self.nonlethal = data["nonlethal"] if "nonlethal" in keys else nonlethal
