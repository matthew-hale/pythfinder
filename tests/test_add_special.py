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

# First setup function adds a single special
@pytest.fixture()
@patch("pythfinder.collections.uuid4", uuid4_mock().__next__)
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
    special = c.add_special(data = special_data)

    return [special_data, special, c]

# Second setup function adds two identical specials
@pytest.fixture()
@patch("pythfinder.collections.uuid4", uuid4_mock().__next__)
def setup_char2():
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

    # Add a second identical special to the character, but this time using 
    # the named parameters
    special_from_parameters = c.add_special(name = special_data["name"],
                                      description = special_data["description"],
                                      notes = special_data["notes"])

    return [special_from_data, special_from_parameters, c]

# Third setup function adds two different specials
@pytest.fixture()
@patch("pythfinder.collections.uuid4", uuid4_mock().__next__)
def setup_char3():
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
    special_1 = c.add_special(data = special_data)

    # Add a second special
    special_data_2 = {
        "name": "second special",
        "description": "unique description",
        "notes": "unique notes"
    }
    special_2 = c.add_special(data = special_data_2)

    return [special_1, special_2, c]

# Is the special added to the character the one we wanted?
## Is the special in the character == the special that's returned by 
## add_special?
def test_add_special_eq(setup_char):
    special = setup_char[1]
    c = setup_char[2]
    assert special == c.specials[0]

## Is the special in the character the same object as the special 
## that's returned by add_special?
def test_add_special_is(setup_char):
    special = setup_char[1]
    c = setup_char[2]
    assert special is c.specials[0]

## Is the data equivalent to the special in the character?
def test_add_special_data(setup_char):
    special_data = setup_char[0]
    c = setup_char[2]
    assert special_data["name"] == c.specials[0].name and \
           special_data["description"] == c.specials[0].description and \
           special_data["notes"] == c.specials[0].notes

## Are the two specials added exactly the same, save for their uuids?
def test_add_special_double(setup_char2):
    special_from_data = setup_char2[0]
    special_from_parameters = setup_char2[1]
    c = setup_char2[2]
    assert special_from_data == special_from_parameters
    assert special_from_data is c.specials[0]
    assert special_from_parameters is c.specials[1]

## Are the two specials added different?
def test_add_special_unique(setup_char3):
    special_1 = setup_char3[0]
    special_2 = setup_char3[1]
    assert special_1 != special_2
