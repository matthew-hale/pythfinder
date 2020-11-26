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
    # Add an item to a character
    item_data = {
        "name": "item name",
        "weight": 5.25,
        "count": 2,
        "camp": False,
        "on_person": True,
        "location": "backpack",
        "notes": "item notes"
    }
    
    c = pf.Character()
    c.equipment = []
    item = c.add_item(data = item_data)

    return (item_data, item, c)

# Is the item that the method returns the same as what we put in?
def test_add_item_return(setup_char):
    item_data = setup_char[0]
    item = setup_char[1]
    for key in item_data.keys():
        assert item[key] == item_data[key]

# Is the actual item in the character data the same as what we put in?
def test_add_item_actual(setup_char):
    item_data = setup_char[0]
    c = setup_char[2]
    for key in item_data.keys():
        assert c.equipment[0][key] == item_data[key]

# Is the actual item in the character data the same as the one that was 
# returned?
def test_add_item_method(setup_char):
    item = setup_char[1]
    c = setup_char[2]
    for key in item.keys():
        assert c.equipment[0][key] == item[key]
