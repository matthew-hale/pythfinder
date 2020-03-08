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
    # Add a trait to a character
    trait_data = {
        "name": "trait name",
        "description": "description",
        "notes": "notes"
    }
    
    c = pf.Character()
    c.traits = []
    trait = c.add_trait(data = trait_data)

    return (trait_data, trait, c)

# Is the trait that the method returns the same as what we put in?
def test_add_trait_return(setup_char):
    trait_data = setup_char[0]
    trait = setup_char[1]
    for key in trait_data.keys():
        assert trait[key] == trait_data[key]

# Is the actual trait in the character data the same as what we put in?
def test_add_trait_actual(setup_char):
    trait_data = setup_char[0]
    c = setup_char[2]
    for key in trait_data.keys():
        assert c.traits[0][key] == trait_data[key]

# Is the actual trait in the character data the same as the one that 
# was returned?
def test_add_trait_method(setup_char):
    trait = setup_char[1]
    c = setup_char[2]
    for key in trait.keys():
        assert c.traits[0][key] == trait[key]
