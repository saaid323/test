from flask import Blueprint
# import the storage engine needed
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place
from models.review import Review

# import the views used
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.places import *
from api.v1.views.amenity import *
