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
    # Add a special ability to a character
    special_data = {
        "name": "special name",
        "description": "description",
        "notes": "notes"
    }
    
    c = pf.Character()
    c.special = []
    special = c.add_special(data = special_data)

    return (special_data, special, c)

# Is the special ability that the method returns the same as what we 
# put in?
def test_add_special_return(setup_char):
    special_data = setup_char[0]
    special = setup_char[1]
    for key in special_data.keys():
        assert special[key] == special_data[key]

# Is the actual special ability in the character data the same as what 
# we put in?
def test_add_special_actual(setup_char):
    special_data = setup_char[0]
    c = setup_char[2]
    for key in special_data.keys():
        assert c.special[0][key] == special_data[key]

# Is the actual special ability in the character data the same as the 
# one that was returned?
def test_add_special_method(setup_char):
    special = setup_char[1]
    c = setup_char[2]
    for key in special.keys():
        assert c.special[0][key] == special[key]
