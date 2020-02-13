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
        self.str = {"base": data["str"], "mods": []} if "str" in keys else str_
        self.dex = {"base": data["dex"], "mods": []} if "dex" in keys else dex
        self.con = {"base": data["con"], "mods": []} if "con" in keys else con
        self.int = {"base": data["int"], "mods": []} if "int" in keys else int_
        self.wis = {"base": data["wis"], "mods": []} if "wis" in keys else wis
        self.cha = {"base": data["cha"], "mods": []} if "cha" in keys else cha_
