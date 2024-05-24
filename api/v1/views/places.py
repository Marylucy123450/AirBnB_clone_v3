#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from os import environ
from models.place import Place


STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def places_per_city(city_id=None):
    """
        places route to handle http method for requested places by city
    """
    city_obj = storage.get('City', city_id)

    if city_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        all_places = storage.all('Place').values()
        city_places = [obj.to_dict() for obj in all_places
                       if obj.city_id == city_id]
        return jsonify(city_places)

    if request.method == 'POST':
        if request.headers.get('Content-Type') != 'application/json':
            abort(400, 'Not a JSON')

        req_json = request.get_json()

        user_id = req_json.get("user_id")
        if user_id is None:
            abort(400, 'Missing user_id')

        user_obj = storage.get('User', user_id)
        if user_obj is None:
            abort(404, 'Not found')

        if req_json.get("name") is None:
            abort(400, 'Missing name')

        req_json['city_id'] = city_id

        new_object = Place(**req_json)
        storage.new(new_object)
        storage.save()
        return make_response(jsonify(new_object.to_dict()), 201)


@app_views.route('/places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def places_with_id(place_id=None):
    """
        places route to handle http methods for given place
    """
    place_obj = storage.get('Place', place_id)

    if place_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(place_obj.to_dict())

    if request.method == 'DELETE':
        storage.delete(place_obj)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if request.headers.get('Content-Type') != 'application/json':
            abort(400, 'Not a JSON')

        req_json = request.get_json()

        ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in req_json.items():
            if key not in ignore:
                setattr(place_obj, key, value)
        storage.save()
        return make_response(jsonify(place_obj.to_dict()), 200)
