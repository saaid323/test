#!/usr/bin/python3
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def place(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    li = []
    for i in city.places:
        li.append(i.to_dict())
    return jsonify(li)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    place = request.get_json()
    user = storage.get(User, place['user_id'])
    if not user:
        abort(404)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    place = Place(**place)
    place.city_id = city.id
    place.save()
    return make_response(jsonify(place.to_dict()), 201)
