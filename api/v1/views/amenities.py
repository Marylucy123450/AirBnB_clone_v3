#!/usr/bin/python3
"""
    Flask route that returns json respone
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET', 'POST'], strict_slashes=False)
def amenities_no_id(amenity_id=None):
    """
        amenities route that handles http requests no ID given
    """
    if request.method == 'GET':
        all_amenities = storage.all('Amenity').values()
        all_amenities = [obj.to_dict() for obj in all_amenities]
        return jsonify(all_amenities)

    if request.method == 'POST':
        if request.headers.get('Content-Type') != 'application/json':
            abort(400, 'Not a JSON')

        req_json = request.get_json()

        if req_json.get('name') is None:
            abort(400, 'Missing name')

        new_object = Amenity(**req_json)
        storage.new(new_object)
        storage.save()
        return make_response(jsonify(new_object.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def amenities_with_id(amenity_id=None):
    """
        amenities route that handles http requests with ID given
    """
    amenity_obj = storage.get('Amenity', amenity_id)

    if amenity_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(amenity_obj.to_dict())

    if request.method == 'DELETE':
        storage.delete(amenity_obj)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if request.headers.get('Content-Type') != 'application/json':
            abort(400, 'Not a JSON')

        req_json = request.get_json()

        ignore = ['id', 'created_at', 'updated_at']
        for key, value in req_json.items():
            if key not in ignore:
                setattr(amenity_obj, key, value)
        storage.save()
        return make_response(jsonify(amenity_obj.to_dict()), 200)
