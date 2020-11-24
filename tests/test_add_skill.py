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
    skill_data = {
        "name": "Perform (Oratory)",
        "rank": 5,
        "isClass": True,
        "notes": "skill notes",
        "misc": []
    }
    return_data = {
        "name": "Perform (Oratory)",
        "rank": 5,
        "isClass": True,
        "mod": "cha",
        "notes": "skill notes",
        "useUntrained": True,
        "misc": []
    }
    
    c = pf.Character()
    c.skills = {}

    return (skill_data, return_data, c)

# Is the skill that the method returns the same as what we put in?
def test_add_skill_return(setup_char):
    skill_data = setup_char[0]
    return_data = setup_char[1]
    c = setup_char[2]
    skill = c.add_skill(data = skill_data)
    assert str(return_data) == str(skill)

# Is the actual skill in the character data the same as the one that was 
# returned?
def test_add_skill_actual(setup_char):
    skill_data = setup_char[0]
    return_data = setup_char[1]
    c = setup_char[2]
    skill = c.add_skill(data = skill_data)
    assert str(skill) == str(c.skills["Perform (Oratory)"])
