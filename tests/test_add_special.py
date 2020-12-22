#!/bin/python3

import pytest
from unittest.mock import Mock
from pythfinder import Character
from pythfinder.collections import BasicItem

# Define mocks in setup function
@pytest.fixture()
def setup_char():
    # Mock Character class constructor
    Character.__init__ = Mock()
    Character.__init__.return_value = None

    # Add a special to a character
    special_data = {
        "name": "special name",
        "description": "description",
        "notes": "notes"
    }
    
    c = Character()
    c.specials = []
    special_from_data = c.add_special(data = special_data)

    # Add a second identical special, but using named parameters
    special_from_parameters = c.add_special(name = special_data["name"],
                                      description = special_data["description"],
                                      notes = special_data["notes"])
    return [special_data, special_from_data, special_from_parameters, c]

# Are both specials added to the character, and are they "equal"?
def test_add_special(setup_char):
    special_from_data = setup_char[1]
    special_from_parameters = setup_char[2]
    c = setup_char[3]
    assert c.specials[0] == special_from_data
    assert c.specials[1] == special_from_parameters
    assert special_from_parameters == special_from_data
