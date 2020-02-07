import pythfinder as pf
import json
from flask import Flask, session, request, render_template, make_response

app = Flask(__name__)

"""
Object Model & URIs

The object model is pretty much just characters. Everything else is a 
property or method of the character object.

I haven't quite decided yet how - or even if - I want to store 
character data, so there may be support for either 1 or multiple 
characters. If only one, URIs will look like this:

/character
/character/homeland
/character/class?name=Fighter&level=4
/character/name

etc.

If I'm storing multiple characters somehow, URIs would look more like 
this:

/character/<UUID>
/character/<UUID>/homeland
/character/<UUID>/class?name=Fighter&level=4
/character/<UUID>/name

I originally wanted something relatively easy to self-host, which to me 
means:

+ Simple to launch and/or 1-step launch
+ No database backend
+ No login functionality

I'll start with mapping out the URIs based on the first option (support 
for only 1 character), and in the process I'll improve the object model 
within the python module, adding methods and properties here necessary.
"""
