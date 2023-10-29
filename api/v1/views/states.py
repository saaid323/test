#!/usr/bin/python3
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    all_items = storage.all(State)
    lis = []
    for i in all_items.values():
        lis.append(i.to_dict())
    return jsonify(lis)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def one_state(state_id):
    s = storage.get(State, state_id)
    return jsonify(s.to_dict())


@app_views.route('states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    s = storage.get(State, state_id)
    storage.delete(s)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_states():
    item = request.get_json()
    add = State(**item)
    add.save()
    return make_response(jsonify(add.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    s = storage.get(State, state_id)
    item = request.get_json()
    for k, v in item.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(s, k, v)
    storage.save()
    return make_response(jsonify(s.to_dict()), 200)
