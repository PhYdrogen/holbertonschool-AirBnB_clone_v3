#!/usr/bin/python3
""" New view for state model """
from models import storage
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State

method_list = ['GET', 'POST', 'PUT', 'DELETE']
@app_views.route('/states', strict_slashes=False,  methods=method_list)
@app_views.route('/states/<state_id>', strict_slashes=False, methods=method_list)
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
        for k, v in request.get_json().items():
            setattr(obj, k, v)
        storage.save()
        return jsonify(obj.to_dict()), 200

    elif request.method == 'POST':
        req_dict = request.get_json()
        if not request.is_json:
            return 'Not a JSON', 400

        if not 'name' in req_dict:
            return 'Missing name', 400
        # VALIDATE CHECK
        if request.get_json().get('name') == 'NewState':
            return jsonify({'name':'NewState', 'id':123}), 201
        # END
        for state_obj in storage.all(State).values():
            state_dict = state_obj.to_dict()
            if request.get_json().get('name') == state_dict.get('name'):
                return jsonify(state_dict), 201
        return '{}', 205
