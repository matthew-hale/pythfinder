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
Returns the character's name property as plain text:

```
<name>
```

## /character/race

Supports:

+ GET

### GET
Returns the character's race property as plain text:

```
<race>
```

## /character/deity

Supports:

+ GET

### GET
Returns the character's deity property as plain text:

```
<deity>
```

## /character/homeland

Supports:

+ GET

### GET
Returns the character's homeland property as plain text:

```
<homeland>
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
specified property, as plain text:

GET /character/speed?type=base
```
<base>
```

### PATCH
Accepts json:

```
{
    "base": <new base>,
    "swim": <new swim>
}
```
