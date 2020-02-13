class CharacterAbilities:
    def __init__(self,
                 str_ = 10,
                 dex = 10,
                 con = 10,
                 int_ = 10,
                 wis = 10,
                 cha = 10,
                 data = {}):
        keys = data.keys()
        self.str = {}
        self.str["base"] = data["str"]["base"] if "str" in keys else str_
        self.str["mods"] = data["str"]["mods"] if "str" in keys else []
        self.dex = {}
        self.dex["base"] = data["dex"]["base"] if "dex" in keys else dex
        self.dex["mods"] = data["dex"]["mods"] if "dex" in keys else []
        self.con = {}
        self.con["base"] = data["con"]["base"] if "con" in keys else con
        self.con["mods"] = data["con"]["mods"] if "con" in keys else []
        self.int = {}
        self.int["base"] = data["int"]["base"] if "int" in keys else int_
        self.int["mods"] = data["int"]["mods"] if "int" in keys else []
        self.wis = {}
        self.wis["base"] = data["wis"]["base"] if "wis" in keys else wis
        self.wis["mods"] = data["wis"]["mods"] if "wis" in keys else []
        self.cha = {}
        self.cha["base"] = data["cha"]["base"] if "cha" in keys else cha
        self.cha["mods"] = data["cha"]["mods"] if "cha" in keys else []

    # Returns the ability score after summing all modifiers
    def get_total_value(self,
                        ability):
        ability_range = ["str", "dex", "con", "int", "wis", "cha"]
        if ability not in ability_range:
            raise ValueError("ability must be one of " + ability_range)
        scores = []
        scores.append(getattr(self, ability)["base"])
        for item in getattr(self, ability)["mods"]:
            scores.append(item)
        return(sum(scores))

    # Like get_total_value, but for just the base value
    def get_base_value(self,
                       ability):
        ability_range = ["str", "dex", "con", "int", "wis", "cha"]
        if ability not in ability_range:
            raise ValueError("ability must be one of " + ability_range)
        return getattr(self, ability)["base"]
