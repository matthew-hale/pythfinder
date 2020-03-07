#!/bin/python3

from unittest.mock import Mock
import pythfinder as pf
import pytest

# Define mocks in setup function
@pytest.fixture()
def mock_setup():
    pf.Character.__init__ = Mock()
    pf.Character.__init__.return_value = None
    pf.Character.is_unique_name = Mock()
    pf.Character.is_unique_name.return_value = True

# Does add_feat return what we expect?
def test_add_feat(mock_setup):
    # Add a feat to a character
    feat_data = {
        "name": "feat name",
        "description": "description",
        "notes": "notes"
    }
    
    c = pf.Character()
    c.feats = []
    feat = c.add_feat(data = feat_data)

    for key in feat_data.keys():
        assert feat[key] == feat_data[key]
