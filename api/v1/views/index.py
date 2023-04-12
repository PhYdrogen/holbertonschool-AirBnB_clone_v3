#!/usr/bin/python3
""" Index where route is defined """
from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status', strict_slashes=False)
def index():
    status = {'status': 'OK'}
    return jsonify(status)

@app_views.route('/stats', strict_slashes=False)
def count_object():
    print(storage.count())
    return jsonify(storage.count())
