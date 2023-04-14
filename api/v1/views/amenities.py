#!/usr/bin/python3
""" New view for amenities model """

from flask import abort, jsonify, request
from models import storage
from api.v1.views import app_views 
from models.amenity import Amenity


def recup_all_amenities():
    all_amenities = []
    for value in storage.all(Amenity).values():
        all_amenities.append(value.to_dict())
    return all_amenities

@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def retrieve_all_amenities():
    all_amenities = recup_all_amenities()
    return jsonify(all_amenities)


@app_views.route('/amenities/<amenity_id>', methods=["GET"])
def retrieve_one_amenities(amenity_id=None):
    all_amenities = recup_all_amenities()
    one_amenity = {}
    for data in all_amenities:
        if data["id"] == amenity_id:
            for key, value in data.items():
                one_amenity[key] = value
    if bool(one_amenity) is False: # If dict is empty abort 404
        abort(404)
    else:
        return jsonify(one_amenity)

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_one_amenities(amenity_id=None):
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    else:
        obj.delete()
        storage.save()
        return jsonify({}), 200
    

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenities():
    request_dict = request.get_json()
    if not request.is_json:
            return 'Not a JSON', 400
    if 'name' not in request_dict:
            return 'Missing name', 400
    New_amenity = Amenity(**request_dict)
    New_amenity.save()
    return jsonify(New_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id=None):
    request_dict = request.get_json()
    if not request.is_json:
            return 'Not a JSON', 400
    all_amenity = recup_all_amenities()
    id_check = []
    for data in all_amenity:
        if data["id"] == amenity_id:
             id_check.append(amenity_id)
    if len(id_check) == 0:
        abort(404)
    data = retrieve_one_amenities()
    data["name"] = request.get_json().get('name')
    storage.save()
    return jsonify(data.to_dict()), 200
