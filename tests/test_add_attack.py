#!/bin/python3

from unittest.mock import Mock
import pythfinder as pf
import pytest

# Define mocks in setup function
@pytest.fixture()
def setup_char():
    pf.Character.__init__ = Mock()
    pf.Character.__init__.return_value = None
    pf.Character.is_unique_name = Mock()
    pf.Character.is_unique_name.return_value = True
    # Add an attack to a character
    attack_data = {
        "name": "attack name",
        "attackType": "attack type",
        "damageType": [],
        "attack_mod": "str",
        "damage_mod": "str", 
        "damage": "attack damage",
        "critRoll": 18,
        "critMulti": 4,
        "range": 55,
        "notes": "attack notes"
    }
    
    c = pf.Character()
    c.abilities = {
        "str": {
            "base": 10,
            "misc": []
        },
        "dex": {
            "base": 0,
            "misc": []
        },
        "con": {
            "base": 0,
            "misc": []
        },
        "int": {
            "base": 0,
            "misc": []
        },
        "wis": {
            "base": 0,
            "misc": []
        },
        "cha": {
            "base": 0,
            "misc": []
        }
    }
    c.attacks = []
    attack = c.add_attack(data = attack_data)

    return (attack_data, attack, c)

# Is the attack that the method returns the same as what we put in?
def test_add_attack_return(setup_char):
    attack_data = setup_char[0]
    attack = setup_char[1]
    for key in attack_data.keys():
        assert attack[key] == attack_data[key]

# Is the actual attack in the character data the same as what we put in?
def test_add_attack_actual(setup_char):
    attack_data = setup_char[0]
    c = setup_char[2]
    for key in attack_data.keys():
        assert c.attacks[0][key] == attack_data[key]

# Is the actual attack in the character data the same as the one that 
# was returned?
def test_add_attack_method(setup_char):
    attack = setup_char[1]
    c = setup_char[2]
    for key in attack.keys():
        assert c.attacks[0][key] == attack[key]
