#!/usr/bin/python3
""" New view for state model """
from models import storage
from flask import jsonify
from models import storage
from api.v1.views import app_views
from models.state import State

@app_views.route('/states', strict_slashes=False)
def state_page():
    arr = []
    for values in storage.all(State).values():
      arr.append(values.to_dict())
    return jsonify(arr)