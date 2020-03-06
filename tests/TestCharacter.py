#!/bin/python3
#

import pythfinder as pf
import unittest

# Initialize a character with some data for the basic parameters, and 
# test that character's initialization, comparing its properties with 
# those specified.
class TestCharacterInitialization(unittest.TestCase):
    def setUp(self):
        character_data = {
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
            "weight": "95kg",
            "size": "M",
            "age": 100,
            "hair": "black",
            "eyes": "purple",
            "languages": ["common", "elven"],
            "baseAttacBonus": [6, 1],
            "gold": 10
        }
        self.character = pf.Character(data = character_data)
    # Are the keys of the character.getKeys() method the same as what 
    # they should be, as defined by should_dict?
    def test_character_keys(self):
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
        should_keys = should_dict.keys()
        actual_keys = self.character.getDict().keys()
        self.assertEqual(actual_keys, should_keys)

if __name__ == "__main__":
    unittest.main()
