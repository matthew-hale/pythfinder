#!/bin/python3

from unittest.mock import Mock
import pythfinder as pf
import pytest

# Define mocks
@pytest.fixture()
def setup_char():
    pf.Character.__init__ = Mock()
    pf.Character.__init__.return_value = None
    pf.Character.is_unique_name = Mock()
    pf.Character.is_unique_name.return_value = None

    # Add two of each deletable element to a character
    # Ensure elements are blank
    c = pf.Character()
    c.feats = []
    c.traits = []
    c.special = []
    c.skills = {}
    c.equipment = []
    c.attacks = []
    c.armor = []
    c.spells = []
    # Add items to each element
    delete_data = {"name": "delete me"}
    non_delete_data = {"name": "not me"}
    skill_delete_data = {"name": "Perform (Oratory)"}
    skills_pre_delete = {
        "Perform (Oratory)": {
            "name": "Perform (Oratory)"
        },
        "Perception": {
            "name": "Perception"
        }
    }
    skills_post_delete = {
        "Perception": {
            "name": "Perception"
        }
    }

    c.feats = [
        delete_data,
        non_delete_data
    ]
    c.traits = [
        delete_data,
        non_delete_data
    ]
    c.special = [
        delete_data,
        non_delete_data
    ]
    c.skills = skills_pre_delete
    c.equipment = [
        delete_data,
        non_delete_data
    ]
    c.attacks = [
        delete_data,
        non_delete_data
    ]
    c.armor = [
        delete_data,
        non_delete_data
    ]
    c.spells = [
        delete_data,
        non_delete_data
    ]

    return (delete_data, non_delete_data, skill_delete_data, skills_pre_delete, skills_post_delete, c)

# Is each returned item the same as what was put in?
def test_delete_element_feat_return(setup_char):
    delete_data = setup_char[0]
    c = setup_char[5]

    return_feat = c.delete_element(name = "delete me", _type = "feats")
    assert delete_data["name"] == return_feat["name"]

def test_delete_element_trait_return(setup_char):
    delete_data = setup_char[0]
    c = setup_char[5]

    return_trait = c.delete_element(name = "delete me", _type = "traits")
    assert delete_data["name"] == return_trait["name"]

def test_delete_element_special_return(setup_char):
    delete_data = setup_char[0]
    c = setup_char[5]

    return_special = c.delete_element(name = "delete me", _type = "special")
    assert delete_data["name"] == return_special["name"]

def test_delete_element_equipment_return(setup_char):
    delete_data = setup_char[0]
    c = setup_char[5]

    return_equipment = c.delete_element(name = "delete me", _type = "equipment")
    assert delete_data["name"] == return_equipment["name"]

def test_delete_element_attack_return(setup_char):
    delete_data = setup_char[0]
    c = setup_char[5]

    return_attack = c.delete_element(name = "delete me", _type = "attacks")
    assert delete_data["name"] == return_attack["name"]

def test_delete_element_armor_return(setup_char):
    delete_data = setup_char[0]
    c = setup_char[5]

    return_armor = c.delete_element(name = "delete me", _type = "armor")
    assert delete_data["name"] == return_armor["name"]

def test_delete_element_spell_return(setup_char):
    delete_data = setup_char[0]
    c = setup_char[5]

    return_spell = c.delete_element(name = "delete me", _type = "spells")
    assert delete_data["name"] == return_spell["name"]

def test_delete_element_skill_return(setup_char):
    skill_delete_data = setup_char[2]
    c = setup_char[5]

    return_skill = c.delete_element(name = "Perform (Oratory)", _type = "skills")
    assert skill_delete_data["name"] == return_skill["name"]

# Are we stopped from deleting skills that aren't Perform, Profession, 
# or Craft?
def test_delete_element_skill_stop(setup_char):
    c = setup_char[5]
    error_message = ""
    should_message = "delete_element: cannot delete skills that are not of the type: ('Craft', 'Perform', 'Profession')"
    try:
        c.delete_element("Perception", "skills")
    except ValueError as err:
        error_message = str(err)
    assert error_message == should_message

# Does an invalid element name throw an error?
def test_delete_element_invalid_name(setup_char):
    c = setup_char[5]
    error_message = ""
    should_message = "delete_element: name not found in element type: feats"
    try:
        c.delete_element("doesn't exist", "feats")
    except ValueError as err:
        error_message = str(err)
    assert error_message == should_message
