class CharacterSavingThrow:
    def __init__(self,
                 base = 0,
                 misc = [0],
                 data = {}):
        keys = data.keys()
        self.base = data["base"] if "base" in keys else base
        self.misc = data["misc"] if "misc" in keys else misc
