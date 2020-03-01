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
GET /character/classes?name=Fighter&archetypes=Pack Mule&level=2
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

## /character/AC

Supports:

+ GET

### GET
Returns the character's AC property:

```
[4, 1, -2]
```
