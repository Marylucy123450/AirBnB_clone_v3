#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states_no_id():
    """
        states route to handle http method for requested states no id provided
    """
    if request.method == 'GET':
        all_states = storage.all('State').values()
        list_states = []
        for state in all_states:
            list_states.append(state.to_dict())
        return jsonify(list_states)

    if request.method == 'POST':
        if request.headers.get('Content-Type') != 'application/json':
            abort(400, 'Not a JSON')

        req_json = request.get_json()

        if req_json.get("name") is None:
            abort(400, 'Missing name')

        new_object = State(**req_json)
        storage.new(new_object)
        storage.save()
        return make_response(jsonify(new_object.to_dict()), 201)


@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def states_with_id(state_id=None):
    """
        states route to handle http method for requested state by id
    """
    state_obj = storage.get('State', state_id)

    if state_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(state_obj.to_dict())

    if request.method == 'DELETE':
        storage.delete(state_obj)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if request.headers.get('Content-Type') != 'application/json':
            abort(400, 'Not a JSON')

        req_json = request.get_json()

        ignore = ['id', 'created_at', 'updated_at']
        for key, value in req_json.items():
            if key not in ignore:
                setattr(state_obj, key, value)
        storage.save()
        return make_response(jsonify(state_obj.to_dict()), 200)
