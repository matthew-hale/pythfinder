#!/bin/python3
#
# carrion_crown_fighter.py

import sys

### CHARACTER VARIABLES ###

# Character information
character = {
    "name": "Qofin Parora",
    "race": "half-elf",
    "class": "fighter",
    "description": """
    A half-elf pack mule.
    Works closely with traveling merchants of the area.
    Skilled at smuggling, concealing daggers, etc.
    """,
    "height": "5'11\"",
    "weight": "160",
    "abilities": {
        "str": 17,
        "dex": 16,
        "con": 16,
        "int": 13,
        "wis": 10,
        "cha": 11
    },
    "level": 1,
    "hitDie": 10,
    "maxHP": 13,
    "currentHP": 13,
    "baseAttackBonus": 1,
    "traits": [
        {
            "name": "On the payroll",
            "description": "+150 starting gold"
        },
        {
            "name": "Ordinary",
            "description": "+4 to stealth checks when attempting to blend in a crowd"
        }
    ],
    "feats": [
        {
            "name": "Skill Focus",
            "description": "+3 to checks with chosen skill",
            "notes": "Sleight of Hand"
        },
        {
            "name": "Deft Hands",
            "description": "+2 to Disable Device and Sleight of Hand checks; bonus increases to +4 with 10 or more ranks in these skills",
            "notes": ""
        }
    ],
    "gold": 10.88
}

equipment = [
    {
        "name": "Tent, hanging",
        "weight": 15,
        "count": 1,
        "pack": False,
        "notes": ""
    },
    {
        "name": "Piton x2",
        "weight": 1,
        "count": 1,
        "pack": False,
        "notes": ""
    },
    {
        "name": "Hook, grappling",
        "weight": 4,
        "count": 1,
        "pack": True,
        "notes": ""
    },
    {
        "name": "Chalk",
        "weight": 0,
        "count": 5,
        "pack": True,
        "notes": ""
    },
    {
        "name": "Hammer",
        "weight": 2,
        "count": 1,
        "pack": True,
        "notes": ""
    },
    {
        "name": "Lantern, hooded",
        "weight": 2,
        "count": 1,
        "pack": True,
        "notes": ""
    },
    {
        "name": "Oil, lamp, pint",
        "count": 2,
        "weight": 1,
        "pack": True,
        "notes": ""
    },
    {
        "name": "Outfit, traveler's",
        "weight": 5,
        "count": 1,
        "pack": True,
        "notes": ""
    },
    {
        "name": "Backpack, masterwork",
        "weight": 4,
        "count": 1,
        "pack": True,
        "notes": "Has a capacity of 2 cubic feet. Treat strength as 1 higher for carrying capacity."
    },
    {
        "name": "Bedroll",
        "weight": 5,
        "count": 1,
        "pack": False,
        "notes": ""
    },
    {
        "name": "Blanket",
        "weight": 3,
        "count": 1,
        "pack": False,
        "notes": ""
    },
    {
        "name": "Fishing tackle",
        "weight": 5,
        "count": 1,
        "pack": False,
        "notes": "+1 circumstance bonus to survival checks to gather food around bodies of water that contain fish"
    },
    {
        "name": "Crowbar",
        "weight": 5,
        "count": 1,
        "pack": True,
        "notes": "+2 circumstance bonus to strength checks to force open a door or chest"
    },
    {
        "name": "Pouch, belt",
        "weight": 1,
        "count": 1,
        "pack": True,
        "notes": "Holds 1/5 cubic feet"
    },
    {
        "name": "Scarf, pocketed",
        "weight": 1,
        "count": 1,
        "pack": True,
        "notes": "+4 bonus on Sleight of Hand checks made to hide objects on your body"
    },
    {
        "name": "Flint & steel",
        "count": 1,
        "weight": 0,
        "pack": True,
        "notes": ""
    },
    {
        "name": "Pot, cooking, iron",
        "weight": 2,
        "count": 1,
        "pack": False,
        "notes": "Holds 1 gallon"
    },
    {
        "name": "Kit, mess",
        "weight": 1,
        "count": 1,
        "pack": False,
        "notes": ""
    },
    {
        "name": "Tools, artisan's",
        "weight": 5,
        "count": 1,
        "pack": False,
        "notes": ""
    },
    {
        "name": "Rope, hemp, 50 ft",
        "count": 1,
        "weight": 10,
        "pack": True,
        "notes": ""
    },
    {
        "name": "Block and tackle",
        "count": 1,
        "weight": 5,
        "pack": True,
        "notes": "+5 circumstance to strength checks to lift heavy objects; takes 1 minute to secure"
    },
    {
        "name": "Twine, 100 ft",
        "count": 1,
        "weight": 1,
        "pack": False,
        "notes": ""
    },
    {
        "name": "Soap",
        "weight": 1,
        "count": 1,
        "pack": False,
        "notes": ""
    },
    {
        "name": "Torch",
        "count": 10,
        "weight": 1,
        "pack": True,
        "notes": ""
    },
    {
        "name": "Sunrod",
        "count": 8,
        "weight": 1,
        "pack": True,
        "notes": ""
    },
    {
        "name": "Compass",
        "count": 1,
        "weight": 0,
        "pack": True,
        "notes": "+1 to survival checks made to avoid becoming lost, and +1 to KnowledgeDungeoneering checks made underground for navigation"
    },
    {
        "name": "Rations, trail",
        "count": 5,
        "weight": 1,
        "pack": False,
        "notes": ""
    },
    {
        "name": "Waterskin",
        "weight": 0,
        "count": 1,
        "pack": False,
        "notes": "Holds 1 gallon"
    },
    {
        "name": "Reinforced tunic",
        "weight": 5,
        "count": 1,
        "pack": True,
        "notes": ""
    },
    {
        "name": "Sword, short",
        "weight": 2,
        "count": 1,
        "pack": True,
        "notes": ""
    },
    {
        "name": "Shield, light wooden",
        "weight": 5,
        "count": 1,
        "pack": True,
        "notes": ""
    },
    {
        "name": "Longspear",
        "weight": 9,
        "count": 1,
        "pack": True,
        "notes": ""
    },
    {
        "name": "Dagger",
        "weight": 2,
        "count": 2,
        "pack": True,
        "notes": ""
    },
    {
        "name": "Crossbow, light",
        "weight": 4,
        "count": 2,
        "pack": True,
        "notes": ""
    },
    {
        "name": "Bolts, crossbow x10",
        "weight": 1,
        "count": 3,
        "pack": True,
        "notes": ""
    },
    {
        "name": "Bolt, grappling",
        "weight": 1,
        "count": 1,
        "pack": True,
        "notes": ""
    },
    {
        "name": "Arrows, ghost",
        "weight": 3,
        "count": 1,
        "pack": True,
        "notes": "see notes"
    },
    {
        "name": "Darkwood case",
        "weight": 9,
        "count": 1,
        "pack": True,
        "notes": "see notes"
    }
]

"""
# Weapons
weapons="Sword, short: damage=1d6 critRoll=19 critMulti=2 damageType=piercing
Longspear: damage=1d8 critRoll=20 critMulti=3 damageType=piercing special=brace,reach 2h
Dagger: damage=1d4 critRoll=19 critMulti=3 damageType=piercing,slashing
Crossbow, light: damage=1d8 critRoll=19 critMulti=2 damageType=piercing ammo=20 ranged"

armor="Reinforced tunic: ac=1 maxDex=5 penalty=0 special=(+2 to AC against crit confirmation rolls against you)
Shield, light wooden: ac=1 penalty=-1"
# Skills
skills="Acrobatics: rank=0 isClass=0 mod=dex bonus=0
Appraise: rank=0 isClass=0 mod=int bonus=0
Bluff: rank=0 isClass=1 mod=cha bonus=0
Climb: rank=0 isClass=1 mod=str bonus=0
Craft: rank=1 isClass=1 mod=int bonus=0 special=weapons
Diplomacy: rank=0 isClass=0 mod=cha bonus=0
DisableDevice: rank=0 isClass=0 mod=dex bonus=2
Disguise: rank=0 isClass=1 mod=cha bonus=0
EscapeArtist: rank=0 isClass=0 mod=dex bonus=0
Fly: rank=0 isClass=0 mod=dex bonus=0
HandleAnimal: rank=0 isClass=1 mod=cha bonus=0
Heal: rank=0 isClass=0 mod=wis bonus=0
Intimidate: rank=1 isClass=1 mod=cha bonus=0
KnowledgeArcana: rank=0 isClass=0 mod=int bonus=0
KnowledgeDungeoneering: rank=0 isClass=1 mod=int bonus=0
KnowledgeEngineering: rank=0 isClass=1 mod=int bonus=0
KnowledgeGeography: rank=0 isClass=0 mod=int bonus=0
KnowledgeHistory: rank=0 isClass=0 mod=int bonus=0
KnowledgeLocal: rank=0 isClass=0 mod=int bonus=0
KnowledgeNature: rank=0 isClass=0 mod=int bonus=0
KnowledgeNobility: rank=0 isClass=0 mod=int bonus=0
KnowledgePlanes: rank=0 isClass=0 mod=int bonus=0
KnowledgeReligion: rank=0 isClass=0 mod=int bonus=0
Linguistics: rank=0 isClass=0 mod=int bonus=0
Perception: rank=0 isClass=0 mod=wis bonus=0
Perform: rank=0 isClass=0 mod=cha bonus=0
Profession: rank=1 isClass=1 mod=wis bonus=0 special=smuggler
Ride: rank=0 isClass=1 mod=dex bonus=0
SenseMotive: rank=0 isClass=0 mod=wis bonus=0
SleightOfHand: rank=1 isClass=1 mod=dex bonus=5
Spellcraft: rank=0 isClass=0 mod=int bonus=0
Stealth: rank=1 isClass=1 mod=dex bonus=0
Survival: rank=1 isClass=1 mod=wis bonus=0
Swim: rank=0 isClass=1 mod=str bonus=0
UseMagicDevice: rank=0 isClass=0 mod=cha bonus=0"
"""

###########################

### MAIN ###

# Check for argument
if not (len(sys.argv) >= 2):
    print("Usage: " + sys.argv[0] + " {character|abilities|skills|items|weapons|feats|traits}")
    sys.exit()

# Argument options
if sys.argv[1] == "character":
    print("character")
elif sys.argv[1] == "abilities":
    print("abilities")
elif sys.argv[1] == "skills":
    print("skills")
elif sys.argv[1] == "items":
    print("items")
elif sys.argv[1] == "weapons":
    print("weapons")
elif sys.argv[1] == "feats":
    print("feats")
elif sys.argv[1] == "traits":
    print("traits")
else:
    print("Usage: " + sys.argv[0] + " {character|abilities|skills|items|weapons|feats|traits}")
    sys.exit()
