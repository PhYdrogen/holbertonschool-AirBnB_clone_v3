#!/usr/bin/python3
""" New view for state model """
from models import storage
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City

method_lt = ['GET', 'POST', 'PUT', 'DELETE']


@app_views.route('/states/<state_id>/cities', strict_slashes=False,  methods=["GET", "POST"])
def city_page(state_id):
    if request.method == "GET":
        ret = [ obj.to_dict() for obj in storage.all(City).values()]
        id_list = []
        for i in ret:
            if state_id == i.get('state_id'):
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
        for CityObj in storage.all(City).values() :
            CiD = CityObj.to_dict()
            if req_dict.get('name') == CiD.get('name'):
                return jsonify(CiD), 201
        abort(404)

@app_views.route('/cities/<city_id>', strict_slashes=False,  methods=method_lt)
def city_get_id(city_id):
    if request.method == "GET":
        CityObj = storage.get(City, city_id)
        if CityObj is None:
            abort(404)
        return jsonify(CityObj.to_dict()), 200
    elif request.method == "DELETE":
        CityObj = storage.get(City, city_id)
        if CityObj is None:
            abort(404)
        CityObj.delete()
        storage.save()
        return {}, 200
    elif request.method == "PUT":
        if city_id is None:
            abort(404)
        obj = storage.get(City, city_id)
        if obj is None:
            abort(404)
        if not request.is_json:
            return 'Not a JSON', 400

        setattr(obj, 'name', request.get_json().get('name'))
        return jsonify(obj.to_dict()), 200
