import json
from pythfinder.CharacterAbilities import CharacterAbilities
from pythfinder.CharacterArmor import CharacterArmor
from pythfinder.CharacterAttack import CharacterAttack
from pythfinder.CharacterBasicItem import CharacterBasicItem
from pythfinder.CharacterClass import CharacterClass
from pythfinder.CharacterEquipment import CharacterEquipment
from pythfinder.CharacterHP import CharacterHP
from pythfinder.CharacterSavingThrow import CharacterSavingThrow
from pythfinder.CharacterSkill import CharacterSkill
from pythfinder.CharacterSpeed import CharacterSpeed
from pythfinder.CharacterSpell import CharacterSpell

# Main character class
class Character:
    def __init__(self, data = {}):
        # Grab keys from imported json data
        keys = data.keys()

        # These are the simple values (those of a type like string, int, etc.). 
        # More complex values will get their own objects initialized.
        self.name = data["name"] if "name" in keys else ""
        self.race = data["race"] if "race" in keys else ""
        self.deity = data["deity"] if "deity" in keys else ""
        self.homeland = data["homeland"] if "homeland" in keys else ""
        self.CMB = data["CMB"] if "CMB" in keys else 0
        self.CMD = data["CMD"] if "CMD" in keys else 10
        self.initiativeMods = data["initiativeMods"] if "initiativeMods" in keys else []
        self.alignment = data["alignment"] if "alignment" in keys else ""
        self.description = data["description"] if "description" in keys else ""
        self.height = data["height"] if "height" in keys else ""
        self.weight = data["weight"] if "weight" in keys else 0
        self.size = data["size"] if "size" in keys else ""
        self.age = data["age"] if "age" in keys else 0
        self.hair = data["hair"] if "hair" in keys else ""
        self.eyes = data["eyes"] if "eyes" in keys else ""
        self.languages = data["languages"] if "languages" in keys else []
        self.spellsPerDay = data["spellsPerDay"] if "spellsPerDay" in keys else {
            "0": 0,
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 0,
            "5": 0,
            "6": 0,
            "7": 0,
            "8": 0,
            "9": 0
        }
        self.baseAttackBonus = data["baseAttackBonus"] if "baseAttackBonus" in keys else []
        self.gold = data["gold"] if "gold" in keys else 0

        # Complex object members
        if "speed" in keys:
            self.speed = CharacterSpeed(data = data["speed"])
        else:
            self.speed = CharacterSpeed() 

        self.classes = []
        if "classes" in keys:
            for item in data["classes"]:
                self.classes.append(CharacterClass(data = item))

        if "abilities" in keys:
            self.abilities = CharacterAbilities(data = data["abilities"])
        else:
            self.abilities = CharacterAbilities()

        if "hp" in keys:
            self.hp = CharacterHP(data = data["hp"])
        else:
            self.hp = CharacterHP()

        self.special = []
        if "special" in keys:
            for item in data["special"]:
                self.special.append(CharacterBasicItem(data = item))

        self.traits = []
        if "traits" in keys:
            for item in data["traits"]:
                self.traits.append(CharacterBasicItem(data = item))

        self.feats = []
        if "feats" in keys:
            for item in data["feats"]:
                self.feats.append(CharacterBasicItem(data = item))


        self.equipment = []
        if "equipment" in keys:
            for item in data["equipment"]:
                self.equipment.append(CharacterEquipment(data = item))

        self.savingThrows = {}
        if "savingThrows" in keys:
            for item in data["savingThrows"].keys():
                self.savingThrows[item] = CharacterSavingThrow(data = data["savingThrows"][item])
        
        self.skills = []
        if "skills" in keys:
            for item in data["skills"]:
                self.skills.append(CharacterSkill(data = item))

        self.spells = []
        if "spells" in keys:
            for item in data["spells"]:
                self.spells.append(CharacterSpell(data = item))

        self.attacks = []
        if "attacks" in keys:
            for item in data["attacks"]:
                self.attacks.append(CharacterAttack(data = item))

        self.armor = []
        if "armor" in keys:
            for item in data["armor"]:
                self.armor.append(CharacterArmor(data = item))

    # Get the modifier for a given ability
    def getAbilityMod(self, ability):
        abilityRange = ["str","dex","con","int","wis","cha"]
        if ability not in abilityRange:
            raise ValueError("getAbilityMod: ability must be one of " + abilityRange)
        value = getattr(self.abilities, ability)
        if value == 1:
            return -5
        elif value in [2, 3]:
            return -4
        elif value in [4, 5]:
            return -3
        elif value in [6, 7]:
            return -2
        elif value in [8, 9]:
            return -1
        elif value in [10, 11]:
            return 0
        elif value in [12, 13]:
            return 1
        elif value in [14, 15]:
            return 2
        elif value in [16, 17]:
            return 3
        elif value in [18, 19]:
            return 4
        elif value in [20, 21]:
            return 5
        elif value in [22, 23]:
            return 6
        elif value in [24, 25]:
            return 7
        elif value in [26, 27]:
            return 8
        elif value in [28, 29]:
            return 9
        elif value in [30, 31]:
            return 10
        else:
            raise ValueError("getAbilityMod: ability must be within range of 1-31, inclusive.")

    # Returns a dict containing the character object, without long elements 
    # like skills, feats, traits, spells, and equipment.
    def getCharacterShort(self):
        output = {}
        output["name"] = self.name
        output["race"] = self.race
        output["classes"] = []
        for item in self.classes:
            output["classes"].append(item.__dict__)
        output["alignment"] = self.alignment
        output["description"] = self.description
        output["height"] = self.height
        output["weight"] = self.weight
        output["abilities"] = self.abilities.__dict__
        output["hp"] = self.hp.__dict__
        return output

    # Returns a dict containing keys for each level of spell present in the 
    # character's list of spells. Within each key, the spells are sorted by 
    # name.
    def getSortedSpells(self):
        output = {}
        spellLevels = []

        # We're doing this because we don't want to end up with empty keys 
        # (makes things easier later)
        for spell in self.spells:
            spellLevels.append(spell.level)

        spellLevelsUnique = sorted(set(spellLevels))

        # Initializing an empty list for each spell level present in th espell 
        # list
        for level in spellLevelsUnique:
            output[level] = []

        for spell in self.spells:
            output[spell.level].append(spell)

        return output

    # Returns a dict of the entire character
    def getDict(self):
        return json.loads(
            json.dumps(self, default = lambda o: getattr(o, '__dict__', str(o)))
        )

    # Returns a JSON string representation of the entire character
    def getJson(self):
        return json.dumps(self, default = lambda o: getattr(o, '__dict__', str(o)))

    # Add a new feat to the character; supports either named arguments 
    # or a dictionary
    #
    # returns the newly created feat
    def addFeat(self,
                name = "",
                description = "",
                notes = "",
                data = {}):
        keys = data.keys()
        new_name = data["name"] if "name" in keys else name
        new_description = data["description"] if "description" in keys else description
        new_notes = data["notes"] if "notes" in keys else notes
        new_feat = CharacterBasicItem(name = new_name,
                                      description = new_description,
                                      notes = new_notes)
        self.feats.append(new_feat)
        return new_feat

    # Add a new feat to the character; supports either named arguments 
    # or a dictionary
    #
    # returns the newly created trait
    def addTrait(self,
                name = "",
                description = "",
                notes = "",
                data = {}):
        keys = data.keys()
        new_name = data["name"] if "name" in keys else name
        new_description = data["description"] if "description" in keys else description
        new_notes = data["notes"] if "notes" in keys else notes
        new_trait = CharacterBasicItem(name = new_name,
                                      description = new_description,
                                      notes = new_notes)
        self.traits.append(new_trait)
        return new_trait

    # Add a new special ability to the character; supports either named 
    # arguments or a dictionary
    #
    # returns the newly created special ability
    def addSpecial(self,
                name = "",
                description = "",
                notes = "",
                data = {}):
        keys = data.keys()
        new_name = data["name"] if "name" in keys else name
        new_description = data["description"] if "description" in keys else description
        new_notes = data["notes"] if "notes" in keys else notes
        new_special = CharacterBasicItem(name = new_name,
                                      description = new_description,
                                      notes = new_notes)
        self.special.append(new_special)
        return new_special

    # Add a new item to the character; supports either named arguments 
    # or a dictionary.
    #
    # returns the newly created item
    def addItem(self,
                name = "",
                weight = 0.0,
                count = 0,
                pack = False,
                notes = "",
                data = {}):
        keys = data.keys()
        new_name = data["name"] if "name" in keys else name
        new_weight = data["weight"] if "weight" in keys else weight
        new_count = data["count"] if "count" in keys else count
        new_pack = data["pack"] if "pack" in keys else pack
        new_notes = data["notes"] if "notes" in keys else notes
        new_item = CharacterEquipment(name = new_name,
                                      weight = new_weight,
                                      count = new_count,
                                      pack = new_pack,
                                      notes = new_notes)
        self.equipment.append(new_item)
        return new_item
