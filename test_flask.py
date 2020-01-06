import pythfinder as pf
import json
from flask import Flask, request, render_template, make_response

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("form.html")
    else:
        characterData = json.loads(request.form["character"])
        character = pf.Character(data = characterData)
        characterShort = character.getCharacterShort()
        response = make_response(render_template("index.html", character = characterShort))
        cookie_str = character.getJson()
        response.set_cookie(key = "character", value = cookie_str)

        return response

@app.route('/character/')
def get_character():
    response = make_response("Character cookie:\n{}".format(request.cookies.get('character')))
    return response
