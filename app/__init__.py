from flask import Flask
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from Config import Config

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

from models import UserModel, ReviewModel, ResturantModel

from resources.user import bp as user_bp
api.register_blueprint(user_bp)

from resources.review import bp as review_bp
api.register_blueprint(review_bp)

from resources.resturant import bp as resturant_bp
api.register_blueprint(resturant_bp)