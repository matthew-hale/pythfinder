#!/bin/python3

from unittest.mock import Mock
import pythfinder as pf

# Generate test data
_characters = []
for i in range(5):
    c_data = {
        "name": "name {}".format(i),
        "race": "race {}".format(i),
        "deity": "deity {}".format(i),
        "homeland": "homeland".format(i),
        "CMB": i,
        "CMD": i+10,
        "initiativeMods": [i, i-5, i+5],
        "alignment": "alignment {}".format(i),
        "description": "description {}".format(i),
        "height": "",
        "weight": i+100,
        "size": "M {}".format(i),
        "age": i+20,
        "hair": "hair {}".format(i),
        "eyes": "eyes {}".format(i),
        "languages": ["common {}".format(i), "elven {}".format(i)],
        "baseAttackBonus": [i+5, i],
        "gold": 10.21*i
    }
    # Append a dictionary containing the character and its input data
    _characters.append({
        "character": pf.Character(data = c_data),
        "data": c_data
    })

# The add_* methods should not have been called, as our data didn't 
# have any keys that would call them.
def test_add_not_called():
    # Mock add_* methods
    pf.Character.add_class = Mock()
    pf.Character.add_feat = Mock()
    pf.Character.add_trait = Mock()
    pf.Character.add_item = Mock()
    pf.Character.add_special = Mock()
    pf.Character.add_spell = Mock()
    pf.Character.add_attack = Mock()
    pf.Character.add_armor = Mock()

    pf.Character.add_class.assert_not_called()
    pf.Character.add_feat.assert_not_called()
    pf.Character.add_trait.assert_not_called()
    pf.Character.add_item.assert_not_called()
    pf.Character.add_special.assert_not_called()
    pf.Character.add_spell.assert_not_called()
    pf.Character.add_attack.assert_not_called()
    pf.Character.add_armor.assert_not_called()

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
    for c in _characters:
        actual = c["character"].getDict().keys()
        assert should == actual

# Are the characters' basic properties what they should be?
def test_character_properties():
    for c in _characters:
        for key in c["data"].keys():
            assert getattr(c["character"], key) == c["data"][key]
