from flask_smorest import Blueprint

bp = Blueprint('review', __name__, "description of review", url_prefix='/review')

from . import routes