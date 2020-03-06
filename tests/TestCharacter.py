#!/bin/python3
#

import pythfinder as pf
import unittest

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
