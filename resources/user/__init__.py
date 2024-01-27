from flask_smorest import Blueprint

bp = Blueprint('user', __name__, description='operations for a user')

from . import routes, auth_routes