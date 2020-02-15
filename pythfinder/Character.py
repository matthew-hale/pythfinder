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
        if ability == 1:
            return -5
        elif ability in [2, 3]:
            return -4
        elif ability in [4, 5]:
            return -3
        elif ability in [6, 7]:
            return -2
        elif ability in [8, 9]:
            return -1
        elif ability in [10, 11]:
            return 0
        elif ability in [12, 13]:
            return 1
        elif ability in [14, 15]:
            return 2
        elif ability in [16, 17]:
            return 3
        elif ability in [18, 19]:
            return 4
        elif ability in [20, 21]:
            return 5
        elif ability in [22, 23]:
            return 6
        elif ability in [24, 25]:
            return 7
        elif ability in [26, 27]:
            return 8
        elif ability in [28, 29]:
            return 9
        elif ability in [30, 31]:
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
    # or a dictionary
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

    # Add a new attack to the character; supports either named 
    # arguments or a dictionary
    #
    # returns the newly created attack
    def addAttack(self,
                  weapon = "",
                  attackType = "",
                  damageType = [],
                  damage = "",
                  critRoll = 20,
                  critMulti = 2,
                  range_ = 0,
                  notes = "",
                  data = {}):
        keys = data.keys()
        new_weapon = data["weapon"] if "weapon" in keys else weapon
        new_attackType = data["attackType"] if "attackType" in keys else attackType
        new_damageType = data["damageType"] if "damageType" in keys else damageType
        new_damage = data["damage"] if "damage" in keys else damage
        new_critRoll = data["critRoll"] if "critRoll" in keys else critRoll
        new_critMulti = data["critMulti"] if "critMulti" in keys else critMulti
        new_range_ = data["range_"] if "range_" in keys else range_
        new_notes = data["notes"] if "notes" in keys else notes
        new_attack = CharacterAttack(weapon = new_weapon,
                                     attackType = new_attackType,
                                     damageType = new_damageType,
                                     damage = new_damage,
                                     critRoll = new_critRoll,
                                     critMulti = new_critMulti,
                                     range_ = new_range_,
                                     notes = new_notes)
        self.attacks.append(new_attack)
        return new_attack

    # Add new armor to the character; supports either named arguments 
    # or a dictionary
    #
    # returns the newly created armor
    def addArmor(self,
                 name = "",
                 acBonus = 0,
                 acPenalty = 0,
                 maxDexBonus = 0,
                 arcaneFailureChance = 0,
                 type_ = "",
                 data = {}):
        keys = data.keys()
        new_name = data["name"] if "name" in keys else name
        new_acBonus = data["acBonus"] if "acBonus" in keys else acBonus
        new_acPenalty = data["acPenalty"] if "acPenalty" in keys else acPenalty
        new_maxDexBonus = data["maxDexBonus"] if "maxDexBonus" in keys else maxDexBonus
        new_arcaneFailureChance = data["arcaneFailureChance"] if "arcaneFailureChance" in keys else arcaneFailureChance
        new_type = data["type"] if "type" in keys else type_
        new_armor = CharacterArmor(name = new_name,
                                   acBonus = new_acBonus,
                                   acPenalty = new_acPenalty,
                                   maxDexBonus = new_maxDexBonus,
                                   arcaneFailureChance = new_arcaneFailureChance,
                                   type_ = new_type)
        self.armor.append(new_armor)
        return new_armor

    # Add new spell to the character; supports either named arguments 
    # or a dictionary
    #
    # returns the newly created armor
    def addSpell(self,
                 name = "",
                 level = 0,
                 description = "",
                 prepared = 0,
                 cast = 0,
                 data = {}):
        keys = data.keys()
        new_name = data["name"] if "name" in keys else name
        new_level = data["level"] if "level" in keys else level
        new_description = data["description"] if "description" in keys else description
        new_prepared = data["prepared"] if "prepared" in keys else prepared
        new_cast = data["cast"] if "cast" in keys else cast
        new_spell = CharacterSpell(name = new_name,
                                   level = new_level,
                                   description = new_description,
                                   prepared = new_prepared,
                                   cast = new_cast)
        self.spells.append(new_spell)
        return new_spell

    # Update an existing feat based on name; supports either named 
    # arguments or a dictionary
    #
    # returns the updated feat
    def updateFeat(self,
                   name = "",
                   new_name = "",
                   description = "",
                   notes = "",
                   data = {}):
        keys = data.keys()
        name = data["name"] if "name" in keys else name
        new_name = data["new_name"] if "new_name" in keys else new_name
        description = data["description"] if "description" in keys else description
        notes = data["notes"] if "notes" in keys else notes
        # Lazy selection; if there are duplicates, this will just pick 
        # up the first one that shows up
        for feat in self.feats:
            if feat.name == name:
                target_feat = feat
                break
        try:
            target_feat
        except NameError:
            return None
        else:
            # Ignore empty parameters
            target_feat.name = new_name or target_feat.name
            target_feat.description = description or target_feat.description
            target_feat.notes = notes or target_feat.notes
            return target_feat

    # Update an existing item based on name; supports either named 
    # arguments or a dictionary
    #
    # returns the updated item 
    def updateItem(self,
                   name = "",
                   weight = 0,
                   count = 0,
                   pack = None,
                   notes = "",
                   data = {}):
        keys = data.keys()
        name = data["name"] if "name" in keys else name
        weight = data["weight"] if "weight" in keys else weight
        pack = data["pack"] if "pack" in keys else pack
        count = data["count"] if "count" in keys else count
        notes = data["notes"] if "notes" in keys else notes
        # Lazy selection; if there are duplicates, this will just pick 
        # up the first one that shows up
        for item in self.equipment:
            if item.name == name:
                target_item = item
                break
        try:
            target_item
        except NameError:
            return None
        else:
            # Ignore empty parameters
            target_item.weight = weight or target_item.weight
            target_item.count = count or target_item.count
            target_item.notes = notes or target_item.notes
            # Pack is special
            print("updateItem method pack value:" + str(pack))
            if pack != None:
                target_item.pack = pack
            return target_item
