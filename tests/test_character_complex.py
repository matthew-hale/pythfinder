#!/bin/python3

import pythfinder as pf

# Initializa a character with data for complex parameters, and test 
# each one.
_character_data = {
    "abilities": {
        "str": {
            "base": 9,
            "misc": [1]
        },
        "dex": {
            "base": 10,
            "misc": [1, 1]
        },
        "con": {
            "base": 11,
            "misc": [1, 2]
        },
        "int": {
            "base": 12,
            "misc": [1, 3]
        },
        "wis": {
            "base": 13,
            "misc": [1, 4]
        },
        "cha": {
            "base": 14,
            "misc": [1, 5]
        }
    },
    "speed": {
        "base": 30,
        "armor": 31,
        "fly": 32,
        "swim": 33,
        "climb": 34,
        "burrow": 35
    },
    "hp": {
        "max": 10,
        "current": 9,
        "temporary": 8,
        "nonlethal": 7
    },
    "AC": [1, 2, 3],
    "saving_throws": {
        "fortitude": {
            "base": 10,
            "misc": [1]
        },
        "reflex": {
            "base": 11,
            "misc": [1, 2]
        },
        "will": {
            "base": 12,
            "misc": [1, 2, 3]
        }
    }
}

_character = pf.Character(data = _character_data)

# Are the character's abilities, speed, and hp the same as the those in 
# _character_data?
def test_complex_properties():
    for key in _character_data.keys():
        assert getattr(_character, key) == _character_data[key]