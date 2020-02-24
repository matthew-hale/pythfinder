import json
from pythfinder.CharacterAbilities import CharacterAbilities
from pythfinder.CharacterArmor import CharacterArmor
from pythfinder.CharacterAttack import CharacterAttack
from pythfinder.CharacterBasicItem import CharacterBasicItem
from pythfinder.CharacterClass import CharacterClass
from pythfinder.CharacterEquipment import CharacterEquipment
from pythfinder.CharacterHP import CharacterHP
from pythfinder.CharacterSavingThrow import CharacterSavingThrow
from pythfinder.CharacterSpeed import CharacterSpeed
from pythfinder.CharacterSpell import CharacterSpell

# These vars are used for skill initialization
_allowed_skill_names = (
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
_trained_only = (
    "Disable Device", "Handle Animal", "Knowledge (Arcana)",
    "Knowledge (Dungeoneering)", "Knowledge (Engineering)", "Knowledge (Geography)",
    "Knowledge (History)", "Knowledge (Local)", "Knowledge (Nature)",
    "Knowledge (Nobility)", "Knowledge (Planes)", "Knowledge (Religion)",
    "Linguistics", "Perception", "Profession",
    "Sleight Of Hand", "Spellcraft", "Use Magic Device"
)
_skill_mods = {
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

# Main character class
class Character:
    def __init__(self, data = {}):
        # Grab keys from imported json data
        keys = data.keys()

        # These are the simple values (those of a type like string, 
        # int, etc.). More complex values will use more complex dicts
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

        # Special ability initialization
        #
        self.special = []
        #
        # If the character has no special abilities, we'll just skip it 
        # and leave it as an empty list. Otherwise, we'll want to add 
        # abilities using a constructor method.
        if "special" in keys:
            for item in data["special"]:
                # add_special returns the special ability dict, and we 
                # don't want it, so we're throwing it out
                _ = self.add_special(data = item)

        # Trait initialization
        #
        self.traits = []
        #
        # As above.
        if "traits" in keys:
            for item in data["traits"]:
                # add_trait returns the trait dict, and we don't want 
                # it, so we're throwing it out
                _ = self.add_trait(data = item)

        # Feat initialization
        #
        self.feats = []
        #
        # As above.
        if "feats" in keys:
            for item in data["feats"]:
                # add_feat returns the feat dict, and we don't want 
                # it, so we're throwing it out
                _ = self.add_feat(data = item)

        self.equipment = []
        if "equipment" in keys:
            for item in data["equipment"]:
                self.equipment.append(CharacterEquipment(data = item))

        self.savingThrows = {}
        if "savingThrows" in keys:
            for item in data["savingThrows"].keys():
                self.savingThrows[item] = CharacterSavingThrow(data = data["savingThrows"][item])
        
        # Skill initialization
        #
        self.skills = {}
        #
        # This is pretty simple. For each allowed skill name, we'll 
        # check the data to see if it has it. If it does, we'll 
        # validate the data's structure as we assign values to our 
        # skill. If any of the data doesn't match what we need, we'll 
        # just use a default value. This way, malformed data doesn't 
        # impact the Character object initialization, and we end up 
        # with a consistent structure every time.
        #
        # First, we get all of the keys from the data:
        #
        data_skill_keys = data["skills"].keys() if "skills" in keys else []
        #
        # Note that if the data doesn't have any skills at all, our 
        # data_skill_keys will be empty, resulting in default values 
        # for everything.
        #
        # Now we can begin iterating through all of the allowed skills:
        for skill_name in _allowed_skill_names:
            # Here we do the same as above: if the skill name is in 
            # data["skills"].keys(), we'll get that skill's keys; 
            # otherwise, we'll just leave it blank.
            data_skill_entry_keys = data["skills"][skill_name].keys() if skill_name in data_skill_keys else []
            # Now we can create the actual skill entry, falling back to 
            # default values if any of the above dictionary keys were 
            # missing.
            self.skills[skill_name] = {
                "name": skill_name,
                "rank": data["skills"][skill_name]["rank"] if "rank" in data_skill_entry_keys else 0,
                "isClass": data["skills"][skill_name]["isClass"] if "isClass" in data_skill_entry_keys else 0,
                "notes": data["skills"][skill_name]["notes"] if "notes" in data_skill_entry_keys else 0,
                "misc": data["skills"][skill_name]["misc"] if "misc" in data_skill_entry_keys else 0,
                "mod": _skill_mods[skill_name],
                "useUntrained": False if skill_name in _trained_only else True
            }

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

    # Returns the total value of the specified skill, taking into 
    # account all of the current modifiers, including:
    #
    # + Skill ranks
    # + Class skill status
    # + Misc. skill modifiers
    # + Skill's current ability modifier
    def get_skill_value(self, skill):
        total = 0
        if not skill in _allowed_skill_names:
            raise ValueError("Character.skills: name must be one of: " + _allowed_skill_names)
        current_skill = self.skills[skill]
        if current_skill["isClass"] and current_skill["rank"] >= 1:
            total += 3
        total += current_skill["rank"]
        total += sum(current_skill["misc"])
        total += self.getAbilityMod(self.abilities.get_total_value(current_skill["mod"]))
        return total

    # Add a new feat to the character; supports either named arguments 
    # or a dictionary
    #
    # returns the newly created feat
    def add_feat(self,
                 name = "",
                 description = "",
                 notes = "",
                 data = {}):
        keys = data.keys()
        new_name = data["name"] if "name" in keys else name
        new_description = data["description"] if "description" in keys else description
        new_notes = data["notes"] if "notes" in keys else notes
        new_feat = {
            "name": new_name,
            "description": new_description,
            "notes": new_notes,
        }
        self.feats.append(new_feat)
        return new_feat

    # Add a new trait to the character; supports either named arguments 
    # or a dictionary
    #
    # returns the newly created trait
    def add_trait(self,
                  name = "",
                  description = "",
                  notes = "",
                  data = {}):
        keys = data.keys()
        new_name = data["name"] if "name" in keys else name
        new_description = data["description"] if "description" in keys else description
        new_notes = data["notes"] if "notes" in keys else notes
        new_trait = {
            "name": new_name,
            "description": new_description,
            "notes": new_notes,
        }
        self.traits.append(new_trait)
        return new_trait

    # Add a new special ability to the character; supports either named 
    # arguments or a dictionary
    #
    # returns the newly created special ability
    def add_special(self,
                    name = "",
                    description = "",
                    notes = "",
                    data = {}):
        keys = data.keys()
        new_name = data["name"] if "name" in keys else name
        new_description = data["description"] if "description" in keys else description
        new_notes = data["notes"] if "notes" in keys else notes
        new_special = {
            "name": new_name,
            "description": new_description,
            "notes": new_notes,
        }
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
        new_name = data["name"] if "name" in keys else name
        new_attackType = data["attackType"] if "attackType" in keys else attackType
        new_damageType = data["damageType"] if "damageType" in keys else damageType
        new_damage = data["damage"] if "damage" in keys else damage
        new_critRoll = data["critRoll"] if "critRoll" in keys else critRoll
        new_critMulti = data["critMulti"] if "critMulti" in keys else critMulti
        new_range_ = data["range_"] if "range_" in keys else range_
        new_notes = data["notes"] if "notes" in keys else notes
        new_attack = CharacterAttack(name = new_name,
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
    def update_feat(self,
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
            if feat["name"] == name:
                target_feat = feat
                break
        try:
            target_feat
        except NameError:
            return None
        else:
            # Ignore empty parameters
            target_feat["name"] = new_name or target_feat["name"]
            target_feat["description"] = description or target_feat["description"]
            target_feat["notes"] = notes or target_feat["notes"]
            return target_feat

    # Update an existing trait based on name; supports either named 
    # arguments or a dictionary
    #
    # returns the updated trait
    def update_trait(self,
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
        for trait in self.traits:
            if trait["name"] == name:
                target_trait = trait
                break
        try:
            target_trait
        except NameError:
            return None
        else:
            # Ignore empty parameters
            target_trait["name"] = new_name or target_trait["name"]
            target_trait["description"] = description or target_trait["description"]
            target_trait["notes"] = notes or target_trait["notes"]
            return target_trait

    # Update an existing special ability based on name; supports either 
    # named arguments or a dictionary
    #
    # returns the updated special ability
    def update_special(self,
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
        for special in self.special:
            if special["name"] == name:
                target_special = special
                break
        try:
            target_special
        except NameError:
            return None
        else:
            # Ignore empty parameters
            target_special["name"] = new_name or target_special["name"]
            target_special["description"] = description or target_special["description"]
            target_special["notes"] = notes or target_special["notes"]
            return target_special

    # Update an existing item based on name; supports either named 
    # arguments or a dictionary
    #
    # returns the updated item 
    def updateItem(self,
                   name = "",
                   weight = None,
                   count = None,
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
            # Handle zero ints
            if weight != None:
                target_item.weight = weight
            if count != None:
                target_item.count = count
            target_item.notes = notes or target_item.notes
            # Pack is special
            if pack != None:
                target_item.pack = pack
            return target_item

    # Update an existing spell based on name; supports either named 
    # arguments or a dictionary
    #
    # returns the updated spell 
    def updateSpell(self,
                    name = None,
                    level = None,
                    description = None,
                    prepared = None,
                    cast = None,
                    data = {}):
        keys = data.keys()
        if "name" in keys:
            name = data["name"]
        if "level" in keys:
            level = data["level"]
        if "description" in keys:
            description = data["description"]
        if "prepared" in keys:
            prepared = data["prepared"]
        if "cast" in keys:
            cast = data["cast"]
        # Lazy selection; if there are duplicates, this will just pick 
        # up the first one that shows up
        for spell in self.spells:
            if spell.name == name:
                target_spell = spell
                break
        try:
            target_spell
        except NameError:
            return None
        else:
            # Ignore empty parameters
            target_spell.level = level or target_spell.level
            target_spell.description = description or target_spell.description
            target_spell.prepared = prepared or target_spell.prepared
            target_spell.cast = cast or target_spell.cast
            return target_spell

    # Update an existing attack based on name; supports either named 
    # arguments or a dictionary
    #
    # returns the updated attack 
    def updateAttack(self,
                    name = None,
                    attackType = None,
                    damageType = None,
                    damage = None,
                    critRoll = None,
                    critMulti = None,
                    range_ = None,
                    notes = None,
                    data = {}):
        keys = data.keys()
        if "name" in keys:
            name = data["name"]
        if "attackType" in keys:
            attackType = data["attackType"]
        if "damageType" in keys:
            damageType = data["damageType"]
        if "damage" in keys:
            damage = data["damage"]
        if "critRoll" in keys:
            critRoll = data["critRoll"]
        if "critMulti" in keys:
            critMulti = data["critMulti"]
        if "range_" in keys:
            range_ = data["range_"]
        if "notes" in keys:
            notes = data["notes"]
        # Lazy selection; if there are duplicates, this will just pick 
        # up the first one that shows up
        for attack in self.attacks:
            if attack.name == name:
                target_attack = attack
                break
        try:
            target_attack
        except NameError:
            return None
        else:
            # Ignore empty parameters
            target_attack.attackType = attackType or target_attack.attackType
            target_attack.damageType = damageType or target_attack.damageType
            target_attack.damage = damage or target_attack.damage
            target_attack.critRoll = critRoll or target_attack.critRoll
            target_attack.critMulti = critMulti or target_attack.critMulti
            target_attack.range = range_ or target_attack.range_
            target_attack.notes = notes or target_attack.notes
            return target_attack

    # Update an existing skill based on name; supports either named 
    # arguments or a dictionary
    #
    # returns the updated skill 
    def updateSkill(self,
                    name = None,
                    rank = None,
                    isClass = None,
                    notes = None,
                    data = {}):
        keys = data.keys()
        if "name" in keys:
            name = data["name"]
        if "rank" in keys:
            rank = data["rank"]
        if "isClass" in keys:
            isClass = data["isClass"]
        if "notes" in keys:
            notes = data["notes"]
        # Skill selection is selecting a dict key; if it doesn't error 
        # out, we're probably fine, but we'll check it just in case
        target_skill = self.skills[name]
        try:
            target_skill
        except NameError:
            return None
        else:
            # Ignore empty parameters
            target_skill["rank"] = rank or target_skill["rank"]
            target_skill["isClass"] = isClass or target_skill["isClass"]
            target_skill["notes"] = notes or target_skill["notes"]
            return target_skill

    # Update an existing skill based on name; supports either named 
    # arguments or a dictionary
    #
    # returns the updated ability dict
    def updateAbility(self,
                      name = None,
                      base = None,
                      data = {}):
        keys = data.keys()
        if "name" in keys:
            name = data["name"]
        if "base" in keys:
            base = data["base"]
        # Abilities are all fixed, so selection is easy
        allowed_values = self.abilities.__dict__.keys()
        if not name in allowed_values:
            raise ValueError("Character().updateAbility: name must be one of " + allowed_values)
        else:
            target_ability = getattr(self.abilities, name)
        # Ignore empty parameters
        target_ability["base"] = base or target_ability["base"]
        return target_ability
