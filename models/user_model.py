from datetime import datetime

from app import db

from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(db.Model):
    
    __tablename__="users"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable = False, unique = True)
    email = db.Column(db.String(75), nullable = False, unique = True)
    password_hash = db.Column(db.String(250), nullable = False)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))

# !!!!!!questions to tutor, whats "lazy"? back_popluate done correctly????
    review = db.relationship('ReviewModel', back_populates = 'user, resturant', lazy="dynamic", cascade="all, delete")

    def __repr__(self):
        return f'<User: {self.username}>'
    
    def commit(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def from_dict(self, user_dict):
        for k, v in user_dict.items():
            if k != "password":
                setattr(self, k, v)
            else:
                setattr(self, "password_hash", generate_password_hash(v))
            
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
   


class ReviewModel(db.Model):

    __tablename__="reviews"

    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String, nullable = False)
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    user = db.relationship('UserModel', back_populates = 'reviews')
    resturant_id = db.Column(db.Integer, db.ForeignKey('resturant.id'), nullable = False)
    resturant = db.relationship('ResturantModel', back_populates = 'reviews')

    def __repr__(self):
        return f'<Review: {self.body}>'
    
    def commit(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class ResturantModel(db.Model):

    __tablename__="resturants"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    address = db.Column(db.String(100))
    tel = db.Column(db.String(10))

    def __repr__(self):
        return f'<Resturant: {self.name}'
    

    def is_following(resturant, user):
        return user in resturant.followed
  
    def follow(resturant, user):
        if resturant.is_following(user):
            return
        resturant.followed.append(user)

    def unfollow(resturant,user):
        if not resturant.is_following(user):
            return
        resturant.followed.remove(user)



    def commit(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


