#!/usr/bin/python3
""" New view for Places model """
from models import storage
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.place import Place

method_lt = ['GET', 'POST', 'PUT', 'DELETE']


@app_views.route('/cities/<city_id>/places', strict_slashes=False, methods=method_lt)
def place_page(city_id):
    """Retrieves the list of all Place objects of a City"""
    from models.city import City
    # Check valid city_id
    doexist = False
    ci_list = [obj.to_dict() for obj in storage.all(City).values()]
    for city_dict in ci_list:
        if city_id == city_dict.get('id'):
            doexist = True
    if not doexist:
        abort(404)
    #
    if request.method == "GET":
        ret = [obj.to_dict() for obj in storage.all(Place).values()]
        id_list = []
        for i in ret:
            if city_id == i.get('city_id'):
                id_list.append(i)
        return jsonify(id_list), 200
    
    elif request.method == "POST":
        if not request.is_json:
            return 'Not a JSON', 400
        req_dict = request.get_json()
        if 'name' not in req_dict:
            return 'Missing name', 400
        new_place = Place(**req_dict)
        new_place.city_id = city_id
        new_place.save()
        storage.save()
        return jsonify(new_place.to_dict()), 201

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

