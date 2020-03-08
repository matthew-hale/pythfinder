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
    # Add a spell to a character
    spell_data = {
        "name": "spell name",
        "level": 5,
        "description": "spell description",
        "prepared": 2,
        "cast": 1
    }
    
    c = pf.Character()
    c.spells = []
    spell = c.add_spell(data = spell_data)

    return (spell_data, spell, c)

# Is the spell that the method returns the same as what we put in?
def test_add_spell_return(setup_char):
    spell_data = setup_char[0]
    spell = setup_char[1]
    for key in spell_data.keys():
        assert spell[key] == spell_data[key]

# Is the actual spell in the character data the same as what we put in?
def test_add_spell_actual(setup_char):
    spell_data = setup_char[0]
    c = setup_char[2]
    for key in spell_data.keys():
        assert c.spells[0][key] == spell_data[key]

# Is the actual spell in the character data the same as the one that 
# was returned?
def test_add_spell_method(setup_char):
    spell = setup_char[1]
    c = setup_char[2]
    for key in spell.keys():
        assert c.spells[0][key] == spell[key]
