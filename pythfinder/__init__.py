#!/bin/python3
#
# pythfinder.py

import json
from pythfinder.Character import Character

### FUNCTIONS ###

# Write the given character data to the file in path
def writeCharacter(character, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(character.getDict(), f, indent=4)

# Filters the given list according to the provided filter dictionary
def filter_list(items, filters):
    keys = items[0].keys()
    # Prevent modification of "items" parameter
    result = items.copy()
    for key in filters.keys():
        if not key in keys:
            continue
        # Prevent breakage of for loop
        current_results = result.copy()
        for item in current_results:
            # String conversion due to API requirements
            if str(item[key]) != filters[key]:
                result.remove(item)
    return result
