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
    response = make_response(render_template("index.html"))
    return response

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

@app.route("/deity")
def get_deity():
    if "character" in session:
        character = pf.Character(json.loads(session["character"]))
        return character.deity
    else:
        return ""

@app.route("/CMB")
def get_CMB():
    if "character" in session:
        character = pf.Character(json.loads(session["character"]))
        return character.CMB
    else:
        return ""

@app.route("/CMD")
def get_CMD():
    if "character" in session:
        character = pf.Character(json.loads(session["character"]))
        return character.CMD
    else:
        return ""

@app.route("/alignment")
def get_alignment():
    if "character" in session:
        character = pf.Character(json.loads(session["character"]))
        return character.alignment
    else:
        return ""

@app.route("/description")
def get_description():
    if "character" in session:
        character = pf.Character(json.loads(session["character"]))
        return character.description
    else:
        return ""

@app.route("/height")
def get_height():
    if "character" in session:
        character = pf.Character(json.loads(session["character"]))
        return character.height
    else:
        return ""

@app.route("/weight")
def get_weight():
    if "character" in session:
        character = pf.Character(json.loads(session["character"]))
        return character.weight
    else:
        return ""

@app.route("/size")
def get_size():
    if "character" in session:
        character = pf.Character(json.loads(session["character"]))
        return character.size
    else:
        return ""

@app.route("/age")
def get_age():
    if "character" in session:
        character = pf.Character(json.loads(session["character"]))
        return character.age
    else:
        return ""

@app.route("/initiativeMods")
def get_initiativeMods():
    if "character" in session:
        character = pf.Character(json.loads(session["character"]))
        return character.initiativeMods
    else:
        return ""

@app.route("/hair")
def get_hair():
    if "character" in session:
        character = pf.Character(json.loads(session["character"]))
        return character.hair
    else:
        return ""

@app.route("/eyes")
def get_eyes():
    if "character" in session:
        character = pf.Character(json.loads(session["character"]))
        return character.eyes
    else:
        return ""

@app.route("/languages")
def get_languages():
    if "character" in session:
        character = pf.Character(json.loads(session["character"]))
        return character.languages
    else:
        return ""

@app.route("/baseAttackBonus")
def get_baseAttackBonus():
    if "character" in session:
        character = pf.Character(json.loads(session["character"]))
        return character.baseAttackBonus
    else:
        return ""

@app.route("/gold")
def get_gold():
    if "character" in session:
        character = pf.Character(json.loads(session["character"]))
        return character.gold
    else:
        return ""

@app.route("/speed")
def get_speed():
    if "character" in session:
        character = pf.Character(json.loads(session["character"]))
        type_ = request.args.get("type", None)
        if type_:
            typeList = type_.split(",")
            output = {}
            keys = character.speed.__dict__.keys()
            for item in typeList:
                if item in keys:
                    output[item] = getattr(character.speed, item)
            return output
        else:
            return character.speed.__dict__
    else:
        return ""

@app.route("/class")
def get_class():
    if "character" in session:
        character = pf.Character(json.loads(session["character"]))
        result = []
        for item in character.classes:
            result.append(item.getClassDict())
        return json.dumps(result)
    else:
        return ""
