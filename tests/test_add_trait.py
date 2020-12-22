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

    # Add a trait to a character
    trait_data = {
        "name": "trait name",
        "description": "description",
        "notes": "notes"
    }
    
    c = Character()
    c.traits = []
    trait_from_data = c.add_trait(data = trait_data)

    # Add a second identical trait, but using named parameters
    trait_from_parameters = c.add_trait(name = trait_data["name"],
                                      description = trait_data["description"],
                                      notes = trait_data["notes"])
    return [trait_data, trait_from_data, trait_from_parameters, c]

# Are both traits added to the character, and are they "equal"?
def test_add_trait(setup_char):
    trait_from_data = setup_char[1]
    trait_from_parameters = setup_char[2]
    c = setup_char[3]
    assert c.traits[0] == trait_from_data
    assert c.traits[1] == trait_from_parameters
    assert trait_from_parameters == trait_from_data
