from pythfinder.CharacterAbilities import CharacterAbilities

class CharacterSkill:
    def __init__(self,
                 name = "",
                 rank = 0,
                 isClass = False,
                 notes = "",
                 misc = [],
                 data = {}):
        keys = data.keys()
        allowedNames = (
            "Acrobatics", "Appraise", "Bluff",
            "Climb", "Craft", "Diplomacy",
            "Disable Device", "Disguise", "Escape Artist",
            "Fly", "Handle Animal", "Heal",
            "Intimidate", "Knowledge (Arcana)", "Knowledge (Dungeoneering)",
            "Knowledge (Engineering)", "Knowledge (Geography)", "Knowledge (History)",
            "Knowledge (Local)", "Knowledge (Nature)", "Knowledge (Nobility)",
            "Knowledge (Planes)", "Knowledge (Religion)", "Linguistics",
            "Perception", "Perform", "Profession",
            "Ride", "Sense Motive", "Sleight Of Hand",
            "Spellcraft", "Stealth", "Survival",
            "Swim", "Use Magic Device"
        )
        trainedOnly = (
            "Disable Device", "Handle Animal", "Knowledge (Arcana)",
            "Knowledge (Dungeoneering)", "Knowledge (Engineering)", "Knowledge (Geography)",
            "Knowledge (History)", "Knowledge (Local)", "Knowledge (Nature)",
            "Knowledge (Nobility)", "Knowledge (Planes)", "Knowledge (Religion)",
            "Linguistics", "Perception", "Profession",
            "Sleight Of Hand", "Spellcraft", "Use Magic Device"
        )
        mods = {
            "Climb": "str",
            "Swim": "str",
            "Acrobatics": "dex",
            "Disable Device": "dex",
            "Escape Artist": "dex",
            "Fly": "dex",
            "Ride": "dex",
            "Sleight Of Hand": "dex",
            "Stealth": "dex",
            "Appraise": "int",
            "Craft": "int",
            "Knowledge (Arcana)": "int",
            "Knowledge (Dungeoneering)": "int",
            "Knowledge (Engineering)": "int",
            "Knowledge (Geography)": "int",
            "Knowledge (History)": "int",
            "Knowledge (Local)": "int",
            "Knowledge (Nature)": "int",
            "Knowledge (Nobility)": "int",
            "Knowledge (Planes)": "int",
            "Knowledge (Religion)": "int",
            "Linguistics": "int",
            "Spellcraft": "int",
            "Heal": "wis",
            "Perception": "wis",
            "Profession": "wis",
            "Sense Motive": "wis",
            "Survival": "wis",
            "Bluff": "cha",
            "Diplomacy": "cha",
            "Disguise": "cha",
            "Handle Animal": "cha",
            "Intimidate": "cha",
            "Perform": "cha",
            "Use Magic Device": "cha"
        }

        self.name = data["name"] if "name" in keys else name
        if not self.name in allowedNames:
            raise ValueError("CharacterSkill: name must be one of " + allowedNames)
        self.rank = data["rank"] if "rank" in keys else rank
        self.isClass = data["isClass"] if "isClass" in keys else isClass
        self.notes = data["notes"] if "notes" in keys else notes
        self.misc = data["misc"] if "misc" in keys else misc

        self.mod = mods[self.name]
        self.useUntrained = False if self.name in trainedOnly else True

    # Returns the total value of the skill modifier
    def get_total_value(self, c):
        total = 0
        if self.isClass and self.rank >= 1:
            total += 3
        total += self.rank
        total += sum(self.misc)
        total += c.getAbilityMod(c.abilities.get_total_value(self.mod))
        return total
