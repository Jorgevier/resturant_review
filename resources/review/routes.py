from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from uuid import uuid4
from flask.views import MethodView
from flask_smorest import abort

from models import ReviewModel

from schema import ReviewSchema, ReviewSchemaNested

from . import bp

# create
@bp.route('/')
class ReviewList(MethodView):

    @bp.response(200, ReviewSchema(many = True))
    def get(self):
        return ReviewModel.query.all()
    
    @jwt_required()
    @bp.arguments(ReviewSchema)
    def review(self, review_data):
        try:
            review = ReviewModel()
            review.user_id = get_jwt_identity()
            review.body = review_data['body']
            review.commit()
            return{'message': "Review created"}, 201
        except:
            return{'message':"Invalid User"}, 401
# retrieve, update & delete
@bp.route('/<post_id>')
class Review(MethodView):

    @bp.response(200, ReviewSchemaNested)
    def get(self, review_id):
        review =  ReviewModel.query.get(review_id)
        if review:
            return review
        abort(400, message='Invalid review')

    @bp.arguments(ReviewSchema)
    def put(self, review_data, review_id):
        review = ReviewModel.query.get(review_id)
        if review:
            review.body = review_data['body']
            review.commit()
            return {'message': 'review has been updated'}, 201
        return{'message':'Invalid review ID'}, 400
        
    def delete(self, review_id):
        review = ReviewModel.query.get(review_id)
        if review:
            review.delete()
            return{'message':'review has been deleted'}, 202
        return{'message':'Invalid review'}, 400
