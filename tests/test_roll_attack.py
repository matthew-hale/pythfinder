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
    # Add an attack
    attack_data = {
        "name": "attack name",
        "description": "attack description",
    }
    
    c = pf.Character()
    c.attacks = [
        attack_data
    ]
    return (attack_data, c)
