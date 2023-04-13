#!/usr/bin/python3
""" New view for Places model """
from models import storage
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.place import Place

method_lt = ['GET', 'POST', 'PUT', 'DELETE']


@app_views.route('/cities/<city_id>/places', strict_slashes=False, methods=method_lt)
def place_page(city_id=None):
    """Retrieves the list of all Place objects of a City"""
    if request.method == "GET":
        ret = [ obj.to_dict() for obj in storage.all(Place).values()]
        id_list = []
        for i in ret:
            if place_id == i.get('place_id'):
                id_list.append(i)
        if len(id_list) > 0:
            return jsonify(id_list), 200
        else:
            abort(404)
    
    elif request.method == "POST":
        if not request.is_json:
            return 'Not a JSON', 400
        req_dict = request.get_json()
        if 'name' not in req_dict:
            return 'Missing name', 400
        for CityObj in storage.all(Place).values() :
            CiD = CityObj.to_dict()
            if req_dict.get('name') == CiD.get('name'):
                return jsonify(CiD), 201
        abort(404)

@app_views.route('/places/<place_id>', strict_slashes=False, methods=method_lt)
def place_get_id(place_id=None):
    """ Retrieves a Place object. """
    if request.method == "GET":
        CityObj = storage.get(Place, place_id)
        if CityObj is None:
            abort(404)
        return jsonify(CityObj.to_dict()), 200
    elif request.method == "DELETE":
        CityObj = storage.get(Place, place_id)
        if CityObj is None:
            abort(404)
        CityObj.delete()
        storage.save()
        return {}, 200
    elif request.method == "PUT":
        if place_id is None:
            abort(404)
        obj = storage.get(Place, place_id)
        if obj is None:
            abort(404)
        if not request.is_json:
            return 'Not a JSON', 400

        setattr(obj, 'name', request.get_json().get('name'))
        return jsonify(obj.to_dict()), 200

