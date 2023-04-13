#!/usr/bin/python3
""" New view for state model """
from models import storage
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State

@app_views.route('/states', strict_slashes=False, methods=['GET','POST'])
@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET', 'DELETE', 'PUT'])
def state_page(state_id=None):
    print(request.method)
    if request.method == 'GET':
        if state_id is None:
            arr = []
            for values in storage.all(State).values():
                arr.append(values.to_dict())
            return jsonify(arr)
        else:
            try:
                return jsonify(storage.get(State, state_id).to_dict())
            except AttributeError:
                abort(404)

    elif request.method == 'DELETE':
        try:
            obj = storage.get(State, state_id)
            obj.delete()
            storage.save()
            return jsonify({}), 200
        except AttributeError:
            abort(404)

    elif request.method == 'PUT':
        obj = storage.get(State, state_id)
        for k, v in request.get_json().items():
            setattr(obj, k, v)
        storage.save()
        return jsonify(obj.to_dict()), 200

    elif request.method == 'POST':
        req_dict = request.get_json().items()
        if not request.is_json:
            return 'Not a JSON', 400

        for key in req_dict:
            if key[0] != 'name':
                return 'Missing name', 400

        for req_key, req_value in request.get_json().items():
            for state_obj in storage.all(State).values():
                state_dict = state_obj.to_dict()
                if req_value == state_dict.get(req_key):
                    return jsonify(state_dict), 201
        return '{}', 201