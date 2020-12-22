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

# Add a piece of equipment
@pytest.fixture()
@patch("pythfinder.collections.uuid4", uuid4_mock().__next__)
def setup_char():
    # Mock Character class constructor
    Character.__init__ = Mock()
    Character.__init__.return_value = None

    # Add equipment to a character
    equipment_data = {
        "name": "equipment name",
        "weight": 5,
        "count": 2,
        "camp": True,
        "on_person": True,
        "location": "location",
        "notes": "notes"
    }
    c = Character()
    c.equipment = []
    equipment = c.add_equipment(data = equipment_data)

    return [equipment_data, equipment, c]

def test_add_equipment_eq(setup_char):
    equipment = setup_char[1]
    c = setup_char[2]
    assert equipment == c.equipment[0]

def test_add_equipment_is(setup_char):
    equipment = setup_char[1]
    c = setup_char[2]
    assert equipment is c.equipment[0]

def test_add_equipment_data(setup_char):
    equipment_data = setup_char[0]
    equipment = setup_char[1]
    keys = equipment_data.keys()
    assert all([True for key in keys if equipment_data[key] == getattr(equipment, key)])
