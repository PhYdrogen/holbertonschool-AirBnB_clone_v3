#!/usr/bin/python3
""" New view for state model """
from models import storage
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State

method_lt = ['GET', 'POST', 'PUT', 'DELETE']


@app_views.route('/states', strict_slashes=False,  methods=method_lt)
@app_views.route('/states/<state_id>', strict_slashes=False, methods=method_lt)
def state_page(state_id=None):
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
        if state_id is None:
            abort(404)
        try:
            obj = storage.get(State, state_id)
            obj.delete()
            storage.save()
            return jsonify({}), 200
        except AttributeError:
            abort(404)

    elif request.method == 'PUT':
        if state_id is None:
            abort(404)
        obj = storage.get(State, state_id)
        if obj is None:
            abort(404)
        if not request.is_json:
            return 'Not a JSON', 400
        for k, v in request.get_json().items():
            setattr(obj, k, v)
        storage.save()
        return jsonify(obj.to_dict()), 200

    elif request.method == 'POST':
        req_dict = request.get_json()
        if not request.is_json:
            return 'Not a JSON', 400

        if 'name' not in req_dict:
            return 'Missing name', 400
        
        new_state = State(**req_dict)
        new_state.state_id = state_id
        new_state.save()
        storage.save()
        return jsonify(new_state.to_dict()), 201
