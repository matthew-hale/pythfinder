class CharacterArmor:
    def __init__(self,
                 name = "",
                 acBonus = 0,
                 acPenalty = 0,
                 maxDexBonus = 0,
                 arcaneFailureChance = 0,
                 type_ = "",
                 data = {}):
        keys = data.keys()
        self.name = data["name"] if "name" in keys else name
        self.acBonus = data["acBonus"] if "acBonus" in keys else acBonus
        self.acPenalty = data["acPenalty"] if "acPenalty" in keys else acPenalty
        self.maxDexBonus = data["maxDexBonus"] if "maxDexBonus" in keys else maxDexBonus
        self.arcaneFailureChance = data["arcaneFailureChance"] if "arcaneFailureChance" in keys else arcaneFailureChance
        self.type = data["type"] if "type" in keys else type_
