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
            if city_id == i.get('city_id'):
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
        for PlaceObj in storage.all(Place).values() :
            PlD = PlaceObj.to_dict()
            if req_dict.get('name') == PlD.get('name'):
                return jsonify(PlD), 201
        abort(404)

@app_views.route('/places/<place_id>', strict_slashes=False, methods=method_lt)
def place_get_id(place_id=None):
    """ Retrieves a Place object. """
    if request.method == "GET":
        PlaceObj = storage.get(Place, place_id)
        if PlaceObj is None:
            abort(404)
        return jsonify(PlaceObj.to_dict()), 200
    elif request.method == "DELETE":
        PlaceObj = storage.get(Place, place_id)
        if PlaceObj is None:
            abort(404)
        PlaceObj.delete()
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

