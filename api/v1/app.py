#!/usr/bin/python3

from flask import Flask, Blueprint, render_template, abort
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext("/")
def app_teardown():
    storage.close()

if __name__ == "__main__":
    host = "0.0.0.0" #HBNB_API_HOST
    port = 5000 #HBNB_API_PORT
    threaded=True