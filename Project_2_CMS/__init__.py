from flask import Flask
app = Flask(__name__)

from .routes import *

app.config["SECRET_KEY"]= "abcd"

