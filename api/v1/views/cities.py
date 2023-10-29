#!/usr/bin/python3
from flask import jsonify, abort, request, make_response
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views

@app_views.route('states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def cities(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    lis = []
    for i in state.cities:
        lis.append(i.to_dict())
    return jsonify(lis)


@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=False)
def city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete(city_id):
    item = storage.get(City, city_id)
    if not item:
        abort(404)
    storage.delete(item)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def add_city(state_id):
    state = storage.get(State, state_id)
    if not state:
       abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({}), 400)
    city = request.get_json()
    city = City(**city)
    city.state_id = state.id
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    item = request.get_json()
    for k, v in item.items():
        if k not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, k, v)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
