#!/bin/python3
#

import pythfinder as pf

# Initialize a character with some data for the basic parameters, and 
# test that character's initialization, comparing its properties with 
# those specified.
_character_data = {
    "name": "test name",
    "race": "human",
    "deity": "god",
    "homeland": "america",
    "CMB": 5,
    "CMD": 6,
    "initiativeMods": [1, 2, 3],
    "alignment": "CN",
    "description": "test character description",
    "height": "180cm",
    "weight": 125,
    "size": "M",
    "age": 100,
    "hair": "black",
    "eyes": "purple",
    "languages": ["common", "elven"],
    "baseAttackBonus": [6, 1],
    "gold": 10
}

_character = pf.Character(data = _character_data)

# Are the keys of the character.getKeys() method the same as what 
# they should be, as defined by should_dict?
def test_character_keys():
    should_dict = {
        "name": "",
        "race": "",
        "deity": "",
        "homeland": "",
        "CMB": "",
        "CMD": "",
        "initiativeMods": "",
        "alignment": "",
        "description": "",
        "height": "",
        "weight": "",
        "size": "",
        "age": "",
        "hair": "",
        "eyes": "",
        "languages": "",
        "spellsPerDay": "",
        "baseAttackBonus": "",
        "gold": "",
        "AC": "",
        "speed": "",
        "classes": "",
        "abilities": "",
        "hp": "",
        "special": "",
        "traits": "",
        "feats": "",
        "equipment": "",
        "saving_throws": "",
        "skills": "",
        "spells": "",
        "attacks": "",
        "armor": ""
    }
    should = should_dict.keys()
    actual = _character.getDict().keys()
    assert should == actual

# Are the character's basic properties what they should be?
def test_character_properties():
    for key in _character_data.keys():
        assert getattr(_character, key) == _character_data[key]
