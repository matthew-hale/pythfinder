class CharacterSpeed:
    def __init__(self,
                 base = 0,
                 armor = 0,
                 fly = 0,
                 swim = 0,
                 climb = 0,
                 burrow = 0,
                 data = {}):
        keys = data.keys()
        self.base = data["base"] if "base" in keys else base
        self.armor = data["armor"] if "armor" in keys else armor
        self.fly = data["fly"] if "fly" in keys else fly
        self.swim = data["swim"] if "swim" in keys else swim
        self.climb = data["climb"] if "climb" in keys else climb
        self.burrow = data["burrow"] if "burrow" in keys else burrow
