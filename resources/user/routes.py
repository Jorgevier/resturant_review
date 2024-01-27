from flask import request

from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import abort
from . import bp
from schema import UserSchema, UserSchemaNested
from models.user_model import UserModel

# create
@bp.route('/user')
class UserList(MethodView):

    @bp.response(200, UserSchema(many = True))
    def get(self):
        return UserModel.query.all()
    
    @bp.arguments(UserSchema)
    def post(self, user_data):
        try:
            user = UserModel()
            user.from_dict(user_data)
            user.commit()
            return {'message': f'{user_data["username"]} created'}, 201
        except:
            abort(400, message= "Username and/or email is taken")
# retrieve

@bp.route('/user/<user_id>')
class User(MethodView):

    @bp.response(200, UserSchemaNested)
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        if user:
            print(user.reviews.all())
            return user
        else:
            abort(400, message="user not found")

    @jwt_required()
    @bp.arguments(UserSchema)
    def put(self, user_data, user_id):
        user = UserModel.query.get(get_jwt_identity())
        if user and user.id == user_id:
            user.from_dict(user_data)
            user.commit()
            return {'message': f'{user.username} your review has been update'}, 202
        abort(400, messgae = 'invalid user')

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.query.get(get_jwt_identity())
        if user == user_id:
            user.delete()
            return {'message': f'User: {user.username} user deleted'}, 202
        return{'message': "invalid user"},400


