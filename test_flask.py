import pythfinder as pf
import json
from flask import Flask, session, request, render_template, make_response

app = Flask(__name__)

# Obviously not going to stay like this; this is for local dev only
app.secret_key = "temporary_dev_secret_key"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("form.html")
    else:
        characterData = json.loads(request.form["character"])
        character = pf.Character(data = characterData)
        characterShort = character.getCharacterShort()
        response = make_response(render_template("index.html", character = characterShort))
        session["character"] = characterData

        return response

@app.route('/character/')
def get_character():
    return session["character"]
