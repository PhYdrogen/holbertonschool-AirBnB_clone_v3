#!/usr/bin/python3
""" New view for Review model """
from models import storage
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.review import Review

method_lt = ['GET', 'POST', 'PUT', 'DELETE']


@app_views.route('places/<place_id>/reviews', strict_slashes=False,
                 methods=method_lt)
def review_page(place_id=None):
    """Retrieves the list of all Place objects of a Review"""
    from models.place import Place

    if storage.get(Place, place_id) is None:
        abort(404)
    if request.method == "GET":
        ret = [obj.to_dict() for obj in storage.all(Review).values()]
        id_list = []
        print(ret)
        for i in ret:
            if place_id == i.get('place_id'):
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

        if req_dict.get('user_id') is None:
            return 'Missing user_id', 400
        if 'text' not in req_dict:
            return 'Missing text', 400
        if storage.get(User, req_dict.get('user_id')) is None:
            abort(404)
        new_place = Place(**req_dict)
        new_place.place_id = place_id
        storage.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('reviews/<review_id>', strict_slashes=False,
                 methods=method_lt)
def review_get_id(review_id=None):
    if request.method == "GET":
        ReviewObj = storage.get(Review, review_id)
        if ReviewObj is None:
            abort(404)
        return jsonify(ReviewObj.to_dict()), 200
    elif request.method == "DELETE":
        ReviewObj = storage.get(Review, review_id)
        if ReviewObj is None:
            abort(404)
        ReviewObj.delete()
        storage.save()
        return {}, 200
    elif request.method == "PUT":
        if review_id is None:
            abort(404)
        obj = storage.get(Review, review_id)
        if obj is None:
            abort(404)
        if not request.is_json:
            return 'Not a JSON', 400

        for k, v in request.get_json().items():
            if k in ["id", "user_id", "place_id", "created_at", "update_at"]:
                continue
            setattr(obj, k, v)
        storage.save()
        return jsonify(obj.to_dict()), 200
