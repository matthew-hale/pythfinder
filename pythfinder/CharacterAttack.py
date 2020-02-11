class CharacterAttack:
    def __init__(self,
                 name = "",
                 attackType = "",
                 damageType = [],
                 damage = "",
                 critRoll = 20,
                 critMulti = 2,
                 range_ = 0,
                 notes = "",
                 data = {}):
        keys = data.keys()
        self.name = data["name"] if "name" in keys else name
        self.attackType = data["attackType"] if "attackType" in keys else attackType
        self.damageType = data["damageType"] if "damageType" in keys else damageType
        self.damage = data["damage"] if "damage" in keys else damage
        self.critRoll = data["critRoll"] if "critRoll" in keys else critRoll
        self.critMulti = data["critMulti"] if "critMulti" in keys else critMulti
        self.range = data["range"] if "range" in keys else range_
        self.notes = data["notes"] if "notes" in keys else notes
