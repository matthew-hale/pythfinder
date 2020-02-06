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
        self.str = data["str"] if "str" in keys else str_
        self.dex = data["dex"] if "dex" in keys else dex
        self.con = data["con"] if "con" in keys else con
        self.int = data["int"] if "int" in keys else int_
        self.wis = data["wis"] if "wis" in keys else wis
        self.cha = data["cha"] if "cha" in keys else cha
