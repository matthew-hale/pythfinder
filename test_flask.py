import pythfinder as pf
import json
from flask import Flask, session, request, render_template, make_response

app = Flask(__name__)

# Testing purposes only (duh)
app.secret_key = "super_secret_development_key.jpg"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["character"] = request.form["character"]
        characterData = json.loads(session["character"])
        character = pf.Character(data = characterData)
        characterShort = character.getCharacterShort()
        response = make_response(render_template("index.html", character = characterShort))
        return response
    else:
        if "character" in session:
            characterData = json.loads(session["character"])
            character = pf.Character(data = characterData)
            characterShort = character.getCharacterShort()
            response = make_response(render_template("index.html", character = characterShort))
            return response
        else:
            character = ""
            return render_template("index.html", character = character)

@app.route("/character")
def get_character():
    if "character" in session:
        return session["character"]
    else:
        return ""

@app.route("/name")
def get_name():
    if "character" in session:
        character = pf.Character(json.loads(session["character"]))
        return character.name
    else:
        return ""

@app.route("/race")
def get_race():
    if "character" in session:
        character = pf.Character(json.loads(session["character"]))
        return character.race
    else:
        return ""

@app.route("/homeland")
def get_homeland():
    if "character" in session:
        character = pf.Character(json.loads(session["character"]))
        return character.homeland
    else:
        return ""
