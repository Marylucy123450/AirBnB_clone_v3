#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'], strict_slashes=False)
def cities_per_state(state_id=None):
    """
        cities route to handle http method for requested cities by state
    """
    state_obj = storage.get('State', state_id)

    if state_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        all_cities = storage.all('City').values()
        state_cities = [obj.to_dict() for obj in all_cities
                        if obj.state_id == state_id]
        return jsonify(state_cities)

    if request.method == 'POST':
        if request.headers.get('Content-Type') != 'application/json':
            abort(400, 'Not a JSON')

        req_json = request.get_json()

        if req_json.get("name") is None:
            abort(400, 'Missing name')

        req_json['state_id'] = state_id

        new_object = City(**req_json)
        storage.new(new_object)
        storage.save()
        return make_response(jsonify(new_object.to_dict()), 201)


@app_views.route('/cities/<city_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def cities_with_id(city_id=None):
    """
        cities route to handle http methods for given city
    """
    city_obj = storage.get('City', city_id)

    if city_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(city_obj.to_dict())

    if request.method == 'DELETE':
        storage.delete(city_obj)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if request.headers.get('Content-Type') != 'application/json':
            abort(400, 'Not a JSON')

        req_json = request.get_json()

        ignore = ['id', 'created_at', 'updated_at']
        for key, value in req_json.items():
            if key not in ignore:
                setattr(city_obj, key, value)
        storage.save()
        return make_response(jsonify(city_obj.to_dict()), 200)
