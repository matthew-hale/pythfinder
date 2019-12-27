import pythfinder as pf
import json
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("form.html")
    else:
        characterData = pf.readCharacterString(request.form["character"])
        character = pf.getCharacterShort(characterData)
        return render_template("index.html", character = character)
