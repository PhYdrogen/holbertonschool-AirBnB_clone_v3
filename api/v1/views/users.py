#!/usr/bin/python3
""" New view for User model """
from models import storage
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.user import User

method_lt = ['GET', 'POST', 'PUT', 'DELETE']


@app_views.route('/users', strict_slashes=False,  methods=method_lt)
@app_views.route('/users/<user_id>', strict_slashes=False,  methods=method_lt)
def user_page(user_id=None):
    if request.method == "GET":
        if user_id is None:
            ret = [obj.to_dict() for obj in storage.all(User).values()]
            return jsonify(ret), 200
        else:
            obj = storage.get(User, user_id)
            if obj is None:
                abort(404)
            return jsonify(obj.to_dict())
    elif request.method == "DELETE":
        UserObj = storage.get(User, user_id)
        if UserObj is None:
            abort(404)
        UserObj.delete()
        storage.save()
        return {}, 200
    elif request.method == "POST":
        if not request.is_json:
            return 'Not a JSON', 400
        req_dict = request.get_json()
        if 'email' not in req_dict:
            return 'Missing email', 400
        if 'password' not in req_dict:
            return 'Missing password', 400

        new_user = User(**req_dict)
        new_user.user_id = user_id
        storage.save()
        return jsonify(new_user.to_dict()), 201

    elif request.method == "PUT":
        if user_id is None:
            abort(404)
        obj = storage.get(User, user_id)
        if obj is None:
            abort(404)
        if not request.is_json:
            return 'Not a JSON', 400
        for k, v in request.get_json().items():
            setattr(obj, k, v)
        storage.save()
        return jsonify(obj.to_dict()), 200
