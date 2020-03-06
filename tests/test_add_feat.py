#!/bin/python3

import pythfinder as pf

# Does add_feat return what we expect?
def test_add_feat():
    # Add a feat to a character
    feat_data = {
        "name": "feat name",
        "description": "description",
        "notes": "notes"
    }
    
    c = pf.Character()
    feat = c.add_feat(data = feat_data)

    for key in feat_data.keys():
        assert feat[key] == feat_data[key]
