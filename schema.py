from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Str(dump_only = True)
    email = fields.Str(required = True)
    username = fields.Str(required = True)
    password = fields.Str(required = True, load_only=True)
    first_name = fields.Str()
    last_name = fields.Str()

class UserLogin(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)

class ReviewSchema(Schema):
    id = fields.Str(dump_only=True)
    body = fields.Str(required=True)
    timestamp = fields.DateTime(dump_only=True)

class ResturantSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    address = fields.Str(required=True)
    tel = fields.Str(required=True)

# ask if done right????
class ReviewSchemaNested(ReviewSchema):
    user = fields.Nested(UserSchema, dump_only = True)
    resturant = fields.Nested(ResturantSchema, dump_only = True)

class UserSchemaNested(UserSchema):
    reviews = fields.List(fields.Nested(ReviewSchema), dump_only=True)
    resturant = fields.Nested(ResturantSchema, dump_only = True) 

class ResturantSchemaNested(ResturantSchema):
    reviews = fields.List(fields.Nested(ReviewSchema), dump_only=True) 
    user = fields.Nested(UserSchema, dump_only = True)