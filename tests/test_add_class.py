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
    # Add a class to a character
    class_data = {
        "name": "class name",
        "archetypes": ["1", "2"],
        "level": 5
    }
    
    c = pf.Character()
    c.classes = []
    returned_class = c.add_class(data = class_data)

    return (class_data, returned_class, c)

# Is the class that the method returns the same as what we put in?
def test_add_class_return(setup_char):
    class_data = setup_char[0]
    returned_class = setup_char[1]
    for key in class_data.keys():
        assert returned_class[key] == class_data[key]

# Is the actual class in the character data the same as what we put in?
def test_add_class_actual(setup_char):
    class_data = setup_char[0]
    c = setup_char[2]
    for key in class_data.keys():
        assert c.classes[0][key] == class_data[key]

# Is the actual class in the character data the same as the one that 
# was returned?
def test_add_class_method(setup_char):
    returned_class = setup_char[1]
    c = setup_char[2]
    for key in returned_class.keys():
        assert c.classes[0][key] == returned_class[key]
