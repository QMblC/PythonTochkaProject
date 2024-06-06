from App import db, app
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin

class UserDb(db.Model, UserMixin):
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String(200))

    def set_password(self, password):
        self.password = generate_password_hash(password, salt_length = 30)

    def is_password_correct(self, password):
         return check_password_hash(self.password, password)

    def __repr__(self):
	    return '<UserDb %r>' % self.id
    
class MasterDb(db.Model):
    
    master_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, nullable = False)
    location_id = db.Column(db.Integer, nullable = False)  
    
    def __repr__(self):
        return '<MasterDb %r>' % self.user_id
    
class AdminDb(db.Model):

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = user_id = db.Column(db.Integer, nullable = False)

    def __repr__(self):
         return '<AdminDb %r>' % self.id
    

    
with app.app_context():
    db.create_all()