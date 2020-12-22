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

# First setup function adds a single feat
@pytest.fixture()
@patch("pythfinder.collections.uuid4", uuid4_mock().__next__)
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
    feat = c.add_feat(data = feat_data)

    return [feat_data, feat, c]

# Second setup function adds two identical feats
@pytest.fixture()
@patch("pythfinder.collections.uuid4", uuid4_mock().__next__)
def setup_char2():
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

    # Add a second identical feat to the character, but this time using 
    # the named parameters
    feat_from_parameters = c.add_feat(name = feat_data["name"],
                                      description = feat_data["description"],
                                      notes = feat_data["notes"])

    return [feat_from_data, feat_from_parameters, c]

# Third setup function adds two different feats
@pytest.fixture()
@patch("pythfinder.collections.uuid4", uuid4_mock().__next__)
def setup_char3():
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
    feat_1 = c.add_feat(data = feat_data)

    # Add a second feat
    feat_data_2 = {
        "name": "second feat",
        "description": "unique description",
        "notes": "unique notes"
    }
    feat_2 = c.add_feat(data = feat_data_2)

    return [feat_1, feat_2, c]

# Is the feat added to the character the one we wanted?
## Is the feat in the character == the feat that's returned by add_feat?
def test_add_feat_eq(setup_char):
    feat = setup_char[1]
    c = setup_char[2]
    assert feat == c.feats[0]

## Is the feat in the character the same object as the feat that's 
## returned by add_feat?
def test_add_feat_is(setup_char):
    feat = setup_char[1]
    c = setup_char[2]
    assert feat is c.feats[0]

## Is the data equivalent to the feat in the character?
def test_add_feat_data(setup_char):
    feat_data = setup_char[0]
    c = setup_char[2]
    assert feat_data["name"] == c.feats[0].name and \
           feat_data["description"] == c.feats[0].description and \
           feat_data["notes"] == c.feats[0].notes

## Are the two feats added exactly the same, save for their uuids?
def test_add_feat_double(setup_char2):
    feat_from_data = setup_char2[0]
    feat_from_parameters = setup_char2[1]
    c = setup_char2[2]
    assert feat_from_data == feat_from_parameters
    assert feat_from_data is c.feats[0]
    assert feat_from_parameters is c.feats[1]

## Are the two feats added different?
def test_add_feat_unique(setup_char3):
    feat_1 = setup_char3[0]
    feat_2 = setup_char3[1]
    assert feat_1 != feat_2
