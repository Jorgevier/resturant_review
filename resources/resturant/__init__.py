from flask_smorest import Blueprint

bp = Blueprint('resturant', __name__, description="operations for resturant")

from . import routes
