#!/bin/python3

import pytest
from unittest.mock import Mock, patch
from pythfinder import Character

# Mock uuid4 in the collections package
def uuid4_mock():
    yield "00000000-0000-0000-0000-000000000000"
    yield "00000000-0000-0000-0000-000000000001"
    yield "00000000-0000-0000-0000-000000000002"
    yield "00000000-0000-0000-0000-000000000003"
    yield "00000000-0000-0000-0000-000000000004"
    yield "00000000-0000-0000-0000-000000000005"
    yield "00000000-0000-0000-0000-000000000006"
    yield "00000000-0000-0000-0000-000000000007"
    yield "00000000-0000-0000-0000-000000000008"
    yield "00000000-0000-0000-0000-000000000009"
    yield "00000000-0000-0000-0000-00000000000a"

# First setup function adds a single trait
@pytest.fixture()
@patch("pythfinder.collections.uuid4", uuid4_mock().__next__)
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
    trait = c.add_trait(data = trait_data)

    return [trait_data, trait, c]

# Second setup function adds two identical traits
@pytest.fixture()
@patch("pythfinder.collections.uuid4", uuid4_mock().__next__)
def setup_char2():
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

    # Add a second identical trait to the character, but this time using 
    # the named parameters
    trait_from_parameters = c.add_trait(name = trait_data["name"],
                                      description = trait_data["description"],
                                      notes = trait_data["notes"])

    return [trait_from_data, trait_from_parameters, c]

# Third setup function adds two different traits
@pytest.fixture()
@patch("pythfinder.collections.uuid4", uuid4_mock().__next__)
def setup_char3():
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
    trait_1 = c.add_trait(data = trait_data)

    # Add a second trait
    trait_data_2 = {
        "name": "second trait",
        "description": "unique description",
        "notes": "unique notes"
    }
    trait_2 = c.add_trait(data = trait_data_2)

    return [trait_1, trait_2, c]

# Is the trait added to the character the one we wanted?
## Is the trait in the character == the trait that's returned by add_trait?
def test_add_trait_eq(setup_char):
    trait = setup_char[1]
    c = setup_char[2]
    assert trait == c.traits[0]

## Is the trait in the character the same object as the trait that's 
## returned by add_trait?
def test_add_trait_is(setup_char):
    trait = setup_char[1]
    c = setup_char[2]
    assert trait is c.traits[0]

## Is the data equivalent to the trait in the character?
def test_add_trait_data(setup_char):
    trait_data = setup_char[0]
    c = setup_char[2]
    assert trait_data["name"] == c.traits[0].name and \
           trait_data["description"] == c.traits[0].description and \
           trait_data["notes"] == c.traits[0].notes

## Are the two traits added exactly the same, save for their uuids?
def test_add_trait_double(setup_char2):
    trait_from_data = setup_char2[0]
    trait_from_parameters = setup_char2[1]
    c = setup_char2[2]
    assert trait_from_data == trait_from_parameters
    assert trait_from_data is c.traits[0]
    assert trait_from_parameters is c.traits[1]

## Are the two traits added different?
def test_add_trait_unique(setup_char3):
    trait_1 = setup_char3[0]
    trait_2 = setup_char3[1]
    assert trait_1 != trait_2
