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

    # Add a feat to a character
    feat_data = {
        "name": "feat name",
        "description": "description",
        "notes": "notes"
    }
    
    c = Character()
    c.feats = []
    feat_from_data = c.add_feat(data = feat_data)

    # Add a second identical feat, but using named parameters
    feat_from_parameters = c.add_feat(name = feat_data["name"],
                                      description = feat_data["description"],
                                      notes = feat_data["notes"])
    return [feat_data, feat_from_data, feat_from_parameters, c]

# Are both feats added to the character, and are they "equal"?
def test_add_feat(setup_char):
    feat_from_data = setup_char[1]
    feat_from_parameters = setup_char[2]
    c = setup_char[3]
    assert c.feats[0] == feat_from_data
    assert c.feats[1] == feat_from_parameters
    assert feat_from_parameters == feat_from_data
