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

# Filters the given list according to the provided two-tuples
def filter_list(items, filters):
    keys = items[0].keys()
    # Prevent modification of "items" parameter
    result = items.copy()
    for tup in filters:
        if not tup[0] in keys:
            continue
        # Prevent breakage of for loop
        current_results = result.copy()
        for item in current_results:
            if item[tup[0]] != tup[1]:
                result.remove(item)
    return result
