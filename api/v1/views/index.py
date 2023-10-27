#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity 
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def index():
    return jsonify({"status": "OK"})



@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    static = {}
    for k, v in classes.items():
        static[k] = storage.count(v)
    return jsonify(static)
