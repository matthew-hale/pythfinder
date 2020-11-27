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

