#!/usr/bin/python3
""" New view for amenities model """

from flask import jsonify
from models import storage
from api.v1.views import app_views 
from models.amenity import Amenity


def recup_all_amenities():
    all_amenities = []
    for value in storage.all(Amenity).values():
        all_amenities.append(value.to_dict())


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
    return jsonify(one_amenity)


@app_views.route('/amenities/<amenity_id>', methods=["DELETE"])
def delete_one_amenities(amenity_id=None):
    all_amenities = recup_all_amenities()
    for data in all_amenities:
        if data["id"] == amenity_id:
            del data
    return {}, 200



       