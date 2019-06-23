from app import db
from app import login

from hashlib import sha256, sha1
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    username = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    @staticmethod
    def generate_hash(password):
        return sha1(password.encode('utf-8')).hexdigest()

    @staticmethod
    def verify_hash(password, hash):
        return sha1(password.encode('utf-8')).hexdigest() == hash

    def serialize(self):
        return {
            'id': self.id, 
            'email': self.email,
            'username': self.username,
            'password': self.password
        }

class Device(db.Model):
    __tablename__ = 'devices'

    id = db.Column(db.Integer, primary_key=True) 
    device_id = db.Column(db.String())
    device_type = db.Column(db.String())
    description = db.Column(db.String())
    status = db.Column(db.Boolean())

    def __init__(self, device_id, device_type, description, status):
        self.device_id = device_id
        self.device_type = device_type
        self.description = description
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id, 
            'device_id': self.device_id,
            'device_type': self.device_type, 
            'description': self.description,
            'status' : self.status
        }