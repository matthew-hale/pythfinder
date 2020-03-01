#!/bin/python3


import sys
sys.path.append("/home/matt/pythfinder")
import pythfinder as pf
from flask import Flask

c = pf.Character()
c.name = "Test character"

app = Flask(__name__)

@app.route("/")
def hey():
    return "Browse to /character to view character json"

@app.route("/character")
def character():
    return c.getJson()

@app.route("/character/name")
def character_name():
    return c.name
