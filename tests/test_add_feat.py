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
    # Add a feat to a character
    feat_data = {
        "name": "feat name",
        "description": "description",
        "notes": "notes"
    }
    
    c = pf.Character()
    c.feats = []
    feat = c.add_feat(data = feat_data)

    return (feat_data, feat, c)

# Is the feat that the method returns the same as what we put in?
def test_add_feat_return(setup_char):
    feat_data = setup_char[0]
    feat = setup_char[1]
    for key in feat_data.keys():
        assert feat[key] == feat_data[key]

# Is the actual feat in the character data the same as what we put in?
def test_add_feat_actual(setup_char):
    feat_data = setup_char[0]
    c = setup_char[2]
    for key in feat_data.keys():
        assert c.feats[0][key] == feat_data[key]

# Is the actual feat in the character data the same as the one that was 
# returned?
def test_add_feat_method(setup_char):
    feat = setup_char[1]
    c = setup_char[2]
    for key in feat.keys():
        assert c.feats[0][key] == feat[key]
