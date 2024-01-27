from flask import request
from flask.views import MethodView
from flask_smorest import abort
from . import bp 
from schema import ResturantSchema, ResturantSchemaNested
from models.user_model import ResturantModel

@bp.route('/resturant/<resturant_id>')
class Resturant(MethodView):

    @bp.response(200, ResturantSchemaNested)
    def get(self, resturant_id):
        resturant = ResturantModel.query.get(resturant_id)
        if resturant:
            print(resturant.reviews.all())
            return resturant
        else:
            abort(400, message="Resturant not found")

    @bp.arguments(ResturantSchema)
    def put(self, resturant_data, resturant_id):
        resturant = ResturantModel.query.get()
        if resturant and resturant_id == resturant_id:
            # resturant.from_dict(resturant_data)
            resturant.commit()
            return{'message': f'{resturant.name} review update'}, 202
        abort(400, message ="invalid user")
        
    def delete(self, resturant_id):
        resturant = ResturantModel.query.get()
        if resturant == resturant_id:
            resturant.delete()
            return {'message': f'Resturant: {resturant.name} resturant deleted'}, 202
        return {'message': "invalid resturant"}, 400
        
@bp.route('/resturant')
class ResturantList(MethodView):

    @bp.response(200, ResturantSchema(many = True))
    def get(self):
        return ResturantModel.query.all()
    
    @bp.arguments(ResturantSchema)
    def review(self, resturant_data):
        try:
            resturant = ResturantModel()
            # resturant.from_dict(resturant_data)
            resturant.commit()
            return{'message': f'{resturant_data["name"]} created'}, 201
        except:
            abort(400, message = "Resturant name taken")


# ask if the follow is done right here and models?????

@bp.route('/resturant/follow/<followed_id>')
class FollowResturant(MethodView):

    def post(self, followed_id):
        followed = ResturantModel.query.get(followed_id)
        follower =ResturantModel.query.get()
        if follower and followed:
            follower.follow(followed)
            followed.commit()
            return {'message':'user followed'}
        else:
            return {'message':'invalid user'}, 400
         
    def put(self, followed_id):
        followed = ResturantModel.query.get(followed_id)
        follower = ResturantModel.query.get()
        if follower and followed:
            follower.unfollow(followed)
            followed.commit()
            return {'message':'user unfollowed'}
        else:
            return {'message':'invalid user'}, 400


    