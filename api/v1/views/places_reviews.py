#!/usr/bin/python3
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    li = []
    for review in place.reviews:
        li.append(review.to_dict())
    return jsonify(review)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    review = request.get_json()
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if 'text' not in request.get_json():
        return make_response(jsonify({'error': 'Missing text'}), 400)
    review = Review(**review)
    review.place_id = place.id
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    items = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    update = request.get_json()
    for k, v in update.items():
        if key not in items:
            setattr(review, k, v)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
