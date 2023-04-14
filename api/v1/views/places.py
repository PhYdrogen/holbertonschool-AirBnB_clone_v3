#!/usr/bin/python3
""" New view for Places model """
from models import storage
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.place import Place

method_lt = ['GET', 'POST', 'PUT', 'DELETE']


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=method_lt)
def place_page(city_id):
    """Retrieves the list of all Place objects of a City"""
    from models.city import City

    if storage.get(City, city_id) is None:
        abort(404)
    if request.method == "GET":
        ret = [obj.to_dict() for obj in storage.all(Place).values()]
        id_list = []
        for i in ret:
            if city_id == i.get('city_id'):
                id_list.append(i)
        if len(id_list) == 0:
            return jsonify([]), 200
        else:
            return jsonify(id_list), 200

    elif request.method == "POST":
        from models.user import User
        if not request.is_json:
            return 'Not a JSON', 400
        req_dict = request.get_json()
        if 'name' not in req_dict:
            return 'Missing name', 400
        if storage.get(User, req_dict.get('user_id')) is None:
            return 'Missing user_id', 400
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

        for k, v in request.get_json().items():
            if k in ["id", "user_id", "city_id", "created_at", "update_at"]:
                continue
            setattr(obj, k, v)
        storage.save()
        return jsonify(obj.to_dict()), 200
