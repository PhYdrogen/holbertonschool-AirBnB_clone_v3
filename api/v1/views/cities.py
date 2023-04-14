#!/usr/bin/python3
""" New view for city model """
from models import storage
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City

method_lt = ['GET', 'POST', 'PUT', 'DELETE']


@app_views.route('/states/<state_id>/cities', strict_slashes=False,  methods=["GET", "POST"])
def city_page(state_id):
    from models.state import State
    # Check valid state_id
    doexist = False
    st_list = [obj.to_dict() for obj in storage.all(State).values()]
    for state_dict in st_list:
        if state_id == state_dict.get('id'):
            doexist = True
    if not doexist:
        abort(404)
    #
    if request.method == "GET":
        ret = [ obj.to_dict() for obj in storage.all(City).values()]
        id_list = []
        for i in ret:
            if state_id == i.get('state_id'):
                id_list.append(i)
        return jsonify(id_list), 200
    
    elif request.method == "POST":
        if not request.is_json:
            return 'Not a JSON', 400
        req_dict = request.get_json()
        if 'name' not in req_dict:
            return 'Missing name', 400
        new_city = City(**req_dict)
        new_city.state_id = state_id
        new_city.save()
        storage.save()
        return jsonify(new_city.to_dict()), 201

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
