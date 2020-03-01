# API endpoints
This document describes the API endpoint structure for the Flask 
implementation of the pythfinder module.

## A note on names
The pythfinder module enforces unique names for collection properties, 
like equipment, attacks, spells, etc. This is to ensure that things 
like update\_feat only affect a single resource, and that the selection 
is not ambiguous or arbitrary. Now, I _could_ use UUIDs, but I figured 
unique names would be easier to reason about and implement, for both 
myself and users.

## A note on collections
Many properties in the Character class are represented as lists, 
containing multiple different entries of dictionaries. Examples include 
equipment, attacks, spells, etc. With these properties, the results 
of a GET request will always be returned as a list, even if the request 
only returns one result. This simplifies the implementation on both 
ends, as you can always assume the result is iterable.

## /character

Supports:

+ GET
+ PATCH

### GET
Returns the full character object that Flask is currently serving.


### PATCH
Allows changes to single value properties:

+ name
+ race
+ deity
+ homeland
+ CMB
+ CMD
+ alignment
+ description
+ height
+ weight
+ size
+ age
+ hair
+ eyes

Accepts json:

```
{
    "name": <new name>,
    "deity": <new deity>
}
```

## /character/name

Supports:

+ GET

### GET
Returns the character's name property as a single JSON string:

```
"<name>"
```

## /character/race

Supports:

+ GET

### GET
Returns the character's race property as a single JSON string:

```
"<race>"
```

## /character/deity

Supports:

+ GET

### GET
Returns the character's deity property as a single JSON string:

```
"<deity>"
```

## /character/homeland

Supports:

+ GET

### GET
Returns the character's homeland property as a single JSON string:

```
"<homeland>"
```

## /character/speed

Supports:

+ GET
+ PATCH

### GET
Returns the chraacter's speed properties:

```
{
    "base": <base>,
    "armor": <armor>,
    "fly": <fly>,
    "swim": <swim>,
    "climb": <climb>,
    "burrow": <burrow>
}
```

Accepts a `type` parameter, which will subsequently return only the 
specified property, as a single JSON string:

GET /character/speed?type=base
```
"<base>"
```

### PATCH
Accepts json:

```
{
    "base": <new base>,
    "swim": <new swim>
}
```

## /character/CMB

Supports:

+ GET

### GET
Returns the character's CMB property as a single JSON string:

```
"<CMB>"
```

## /character/CMD

Supports:

+ GET

### GET
Returns the character's CMD property as a single JSON string:

```
"<CMD>"
```

## /character/initiativeMods

Supports:

+ GET

### GET
Returns the character's initiativeMods property as json:

```
[<mod1>,<mod2>]
```

## /character/classes

Supports:

+ GET
+ PATCH
+ POST

### GET
Returns the character's classes as json:

```
[
    {
        <class>
    },
    {
        <class>
    }
]
```

Supports parameters to filter results:

GET /character/classes?name=Fighter&level=5
```
[
    {
        "name": "Fighter",
        "archetypes": [],
        "level": 5
    }
]
```

(`archetypes` is like a "contains" operation, as it's a list of strings)
GET /character/classes?name=Fighter&archetypes=Pack%20Mule&level=2
```
[
    {
        "name": "Fighter",
        "archetypes": [
            "Pack Mule",
            "Child of War"
        ],
        "level": 2
    }
]
```

### PATCH
Allows changes to classes, specified by name:

PATCH /character/classes?name=Fighter
```
{
    "level": 3
}
```

### POST
Allows creation of classes:

POST /character/classes
```
{
    "name": "Fighter",
    "archetypes": [
        "Child of War"
    ],
    "level": 1
}
```

## /character/AC

Supports:

+ GET

### GET
Returns the character's AC property as a list:

```
[4, 1, -2]
```

## /character/alignment

Supports:

+ GET

### GET
Returns the character's alignment property as a single JSON string:

```
"<alignment>"
```

## /character/description

Supports:

+ GET

### GET
Returns the character's description property as a single JSON string:

```
"<description>"
```

## /character/height

Supports:

+ GET

### GET
Returns the character's height property as a single JSON string:

```
"<height>"
```

## /character/weight

Supports:

+ GET

### GET
Returns the character's weight property as a single JSON string:

```
"<weight>"
```

## /character/size

Supports:

+ GET

### GET
Returns the character's size property as a single JSON string:

```
"<size>"
```

## /character/age

Supports:

+ GET

### GET
Returns the character's age property as a single JSON string:

```
"<age>"
```

## /character/hair

Supports:

+ GET

### GET
Returns the character's hair property as a single JSON string:

```
"<hair>"
```

## /character/eyes

Supports:

+ GET

### GET
Returns the character's eyes property as a single JSON string:

```
"<eyes>"
```

## /character/languages

Supports:

+ GET

### GET
Returns the character's languages property as a list:

```
["<language>","<language>"]
```

## /character/abilities

Supports:

+ GET
+ PATCH

### GET
Returns the character's abilities property:

```
{
    "str": {
        "base": 0,
        "mods": []
    },
    "dex": {
        "base": 1,
        "mods": []
    },
    "con": {
        "base": 2,
        "mods": []
    },
    "int": {
        "base": 3,
        "mods": []
    },
    "wis": {
        "base": 4,
        "mods": []
    },
    "cha": {
        "base": 5,
        "mods": []
    }
}
```

Supports an `ability` parameter to return a single ability:

GET /character/abilities?ability=str
```
{
    "base": 0,
    "mods": []
}
```

## /character/hp

Supports:

+ GET

### GET
Returns the character's HP property:

```
{
    "max": 0,
    "current": 0,
    "temporary": 0,
    "nonlethal": 0
}
```

Accepts a `type` parameter to specify a specific HP property:

GET /character/hp?type=max
```
"0"
```

## /character/baseAttackBonus

Supports:

+ GET

### GET
Returns the character's baseAttackBonus property as a list:

```
[11, 6, 1]
```

## /character/special

Supports:

+ GET
+ PATCH
+ POST

### GET
Returns the character's special abilities as a list:

```
[
    {
        "name": "",
        "description": "",
        "notes": ""
    }
]
```

Supports parameters to filter results:

GET /character/special?name=Special%20beam%20cannon&description=bwaoaoaoaoaom
```
[
    {
        "name": "Special beam cannon",
        "description": "bwaoaoaoaoaom",
        "notes": ""
    }
]
```

### PATCH
Allows changes to special abilities, specified by name:

PATCH /character/special?name=Special%20beam%20cannon
```
{
    "notes": "new ability notes"
}
```

### POST
Allows creation of new special abilities:

POST /character/special
```
{
    "name": "Solar flare",
    "description": "Blinds everyone in a huge radius",
    "notes": "Super annoying"
}
```

## /character/traits
As special

## /character/feats
As special

## /character/gold
Supports:

+ GET

### GET
Returns the character's gold property as a single JSON string:

```
"<gold>"
```

## /character/equipment
Supports:

+ GET
+ PATCH
+ POST

### GET
Returns the character's equipment property as a list:

```
[
    {
        "name": "",
        "weight": 0,
        "count": 0,
        "pack": false,
        "notes": ""
    }
]
```

### PATCH
Allows updates to items specified by name:

PATCH /character/equipment?name=Torch
```
{
    "count": 12
}
```

### POST
Allows creation of new items:

POST /character/equipment
```
{
    "name": "Candle",
    "weight": -,
    "count": 10,
    "pack": true,
    "notes": "Illuminates a small area"
}
```

## /character/saving_throws
Supports:

+ GET
+ PATCH

### GET
Returns the character's saving_throws property:

```
{
    "fortitude": {
        "base": 0,
        "misc": []
    },
    "reflex": {
        "base": 1,
        "misc": []
    },
    "will": {
        "base": 2,
        "misc": []
    }
}
```

Accepts a `type` parameter to return a specific saving throw type:

GET /character/saving_throws?type=fortitude
```
{
    "base": 0,
    "misc": []
}
```

### PATCH
Allows for updates to saving throws, by type:

PATCH /character/saving_throws?type=will

```
{
    "base": 5
}
```

## /character/skills
Supports:

+ GET
+ PATCH

### GET
Returns the character's skills property:

```
{
    "Acrobatics": {
        "name": "Acrobatics",
        ...
    }
    ...
}
```

Accepts parameters to filter results:

GET /character/skills?name=Fly
```
{
    "name": "Fly",
    "rank": 0,
    "isClass": false,
    "notes": "",
    "misc": [],
    "mod": dex,
    "useUntrained": true
}
```

GET /character/skills?rank=5
```
[
    {
        "name": "Fly",
        "rank": 5,
        "isClass": false,
        "notes": "",
        "misc": [],
        "mod": dex,
        "useUntrained": true
    },
    {
        "name": "Acrobatics",
        "rank": 5,
        "isClass": false,
        "notes": "",
        "misc": [],
        "mod": dex,
        "useUntrained": true
    },
]
```

### PATCH
Allows for updates to specific skills, by name:

PATCH /character/skills?name=Heal
```
{
    "rank": 5,
    "misc": [2, 4]
}
```

## /character/attacks
Supports:

+ GET
+ PATCH
+ POST

### GET
Returns the character's attacks in a list:

```
[
    {
        "name": "",
        "attackType": "",
        ...
    },
    ...
]
```

Accepts parameters to filter results:

GET /character/attacks?name=Spear&damage=1d8
```
{
    "name": "spear",
    "attackType": "melee",
    "damageType": "piercing",
    "damage": "1d8",
    "critRoll": 19,
    "critMulti": 2,
    "range": 0,
    "notes": ""
}
```

### PATCH
Allows updates to specific attacks by name:

PATCH /character/attacks?name=Spear
```
{
    "critMulti": 3
}
```

### POST
Allows creation of new attacks:

POST /character/attacks
```
{
    "name": "Longsword",
    "attackType": "melee",
    "damageType": "slashing, piercing",
    "damage": "1d8",
    "critRoll": 19,
    "critMulti": 2,
    "range": 0,
    "notes": ""
}
```

## /character/armor
Supports:

+ GET
+ PATCH
+ POST

### GET
Returns the character's armor property as a list:

```
[
    {
        "name": "Chainmail",
        ...
    },
    ...
]
```

### PATCH
Allows updates to specific armor by name:

PATCH /character/armor?name=Chainmail
```
{
    "acPenalty": 2,
    "acBonus": 6
}
```

Accepts parameters to filter results:

GET /character/armor?acBonus=6&acPenalty=2
```
{
    "name": "Chainmail",
    "acBonus": 6,
    "acPenalty": 2,
    "maxDexBonus": 0,
    "arcaneFailureChance": 25,
    "type": "medium"
}
```

### POST
Allows creation of new armor:

POST /character/armor
```
{
    "name": "Full Plate",
    "acBonus": 5,
    "acPenalty": 5,
    "maxDexBonus": 5,
    "arcaneFailureChance": 25,
    "type": "heavy"
}
```

## /character/spells
Supports:

+ GET
+ PATCH
+ POST
