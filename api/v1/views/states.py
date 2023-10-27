#!/usr/bin/python3
from flask import jsonify, abort
from models.base_model import BaseModel
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


@app_views.route('/statesi/<state_id>', methods=['GET'], strict_slashes=False)
def one_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())
