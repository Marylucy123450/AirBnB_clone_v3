#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET', 'POST'], strict_slashes=False)
def reviews_per_place(place_id=None):
    """
        reviews route to handle http method for requested reviews by place
    """
    place_obj = storage.get('Place', place_id)

    if place_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        all_reviews = storage.all('Review').values()
        place_reviews = [obj.to_dict() for obj in all_reviews
                         if obj.place_id == place_id]
        return jsonify(place_reviews)

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

        if req_json.get('text') is None:
            abort(400, 'Missing text')

        req_json['place_id'] = place_id

        new_object = Review(**req_json)
        storage.new(new_object)
        storage.save()
        return make_response(jsonify(new_object.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def reviews_with_id(review_id=None):
    """
        reviews route to handle http methods for given review by ID
    """
    review_obj = storage.get('Review', review_id)

    if review_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(review_obj.to_dict())

    if request.method == 'DELETE':
        storage.delete(review_obj)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if request.headers.get('Content-Type') != 'application/json':
            abort(400, 'Not a JSON')

        req_json = request.get_json()

        ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in req_json.items():
            if key not in ignore:
                setattr(review_obj, key, value)
        storage.save()
        return make_response(jsonify(review_obj.to_dict()), 200)
