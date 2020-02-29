# API endpoints
This document describes the API endpoint structure for the Flask 
implementation of the pythfinder module.

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
