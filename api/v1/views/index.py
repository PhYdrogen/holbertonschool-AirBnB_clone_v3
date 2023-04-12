#!/usr/bin/python3
""" Index where route is defined """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def index():
    status = {'status': 'OK'}
    return jsonify(status)
