#!/usr/bin/python3
""" New view for state model """
from models import storage
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State

@app_views.route('/states', strict_slashes=False)
@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET', 'DELETE', 'PUT', 'POST'])
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
        obj = storage.get(State, state_id)
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        pass
    elif request.method == 'POST':
        pass