#!/usr/bin/python3
from flask import jsonify
from models.base_model import BaseModel
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    all_items = storage.all(State)
    return all_items.to_dict()
