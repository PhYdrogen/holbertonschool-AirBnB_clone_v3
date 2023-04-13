#!/usr/bin/python3
""" Index where route is defined """
from api.v1.views import app_views
from flask import jsonify
from models import storage

from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

Classes = {'cities': City,
           'amenities': Amenity,
           'places': Place,
           'reviews': Review,
           'states': State,
           'users': User}


@app_views.route('/status', strict_slashes=False)
def index():
    status = {'status': 'OK'}
    return jsonify(status)


@app_views.route('/stats', strict_slashes=False)
def count_object():
    new_dict = {}
    for key, value in Classes.items():
        new_dict[key] = storage.count(value)
    return jsonify(new_dict)
