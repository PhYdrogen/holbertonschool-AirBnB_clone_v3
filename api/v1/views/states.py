#!/usr/bin/python3
""" New view for state model """
from models import storage
from flask import jsonify
from models import storage
from api.v1.views import app_views

@app_views.route('/states', strict_slashes=False)
def state_page():
    return jsonify('hello')