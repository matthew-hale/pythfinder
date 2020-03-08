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
    # Add a piece of armor to a character
    armor_data = {
        "name": "armor name",
        "acBonus": 2,
        "acPenalty": 3,
        "maxDexBonus": 4,
        "arcaneFailureChance": 5,
        "type": "armor type"
    }
    
    c = pf.Character()
    c.armor = []
    armor = c.add_armor(data = armor_data)

    return (armor_data, armor, c)

# Is the armor that the method returns the same as what we put 
# in?
def test_add_armor_return(setup_char):
    armor_data = setup_char[0]
    armor = setup_char[1]
    for key in armor_data.keys():
        assert armor[key] == armor_data[key]

# Is the actual armor in the character data the same as what we put 
# in?
def test_add_armor_actual(setup_char):
    armor_data = setup_char[0]
    c = setup_char[2]
    for key in armor_data.keys():
        assert c.armor[0][key] == armor_data[key]

# Is the actual armor in the character data the same as the one that 
# was returned?
def test_add_armor_method(setup_char):
    armor = setup_char[1]
    c = setup_char[2]
    for key in armor.keys():
        assert c.armor[0][key] == armor[key]
