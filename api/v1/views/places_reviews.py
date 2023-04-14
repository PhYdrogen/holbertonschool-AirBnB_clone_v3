#!/usr/bin/python3
""" New view for Review model """
from models import storage
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.review import Review

method_lt = ['GET', 'POST', 'PUT', 'DELETE']


@app_views.route('places/<place_id>/reviews', strict_slashes=False, methods=method_lt)
def review_page(place_id=None):
    """Retrieves the list of all Place objects of a Review"""
    if request.method == "GET":
        ret = [ obj.to_dict() for obj in storage.all(Review).values()]
        id_list = []
        for i in ret:
            if place_id == i.get('place_id'):
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
        for ReviewObj in storage.all(Review).values() :
            ReD = ReviewObj.to_dict()
            if req_dict.get('name') == ReD.get('name'):
                return jsonify(ReD), 201
        abort(404)

@app_views.route('reviews/<review_id>', strict_slashes=False, methods=method_lt)
def review_get_id(review_id=None):
    """ Retrieves a review object. """
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

        setattr(obj, 'name', request.get_json().get('name'))
        return jsonify(obj.to_dict()), 200

