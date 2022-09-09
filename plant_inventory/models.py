# orm 
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

import uuid #sets id for user

from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

import secrets 

# importsv from flask_login
from flask_login import UserMixin, LoginManager

#imports for flssk marshmelllow 

from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = "")
    last_name = db.Column(db.String(150), nullable = True, default = "")
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String(150), nullable = True, default = "")
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default ='', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    #TODO add Drone Relationship 
    plant = db.relationship('Plant', backref = "owner", lazy = True)

    def __init__(self, email, first_name = "", last_name = "", id = "", password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f"User {self.email} has been added!"

#day 3: object to add to DB
class Plant(db.Model):
    id = db.Column(db.String, primary_key = True)
    commom_name = db.Column(db.String(150))
    species_name = db.Column(db.String(150), nullable = True)
    size = db.Column(db.String(150))
    origin = db.Column(db.String(150), nullable = True)
    light = db.Column(db.String(150))
    shade = db.Column(db.String(150))
    soil = db.Column(db.String(150), nullable = True)
    fertilize = db.Column(db.String(150), nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)


    def __init__(self, commom_name, species_name, size , origin, light, shade, soil, fertilize, user_token, id=""):
        self.id = self.set_id()
        self.commom_name = commom_name
        self.species_name = species_name
        self.size = size
        self.origin = origin
        self.light = light
        self.shade = shade
        self.soil = soil
        self.fertilize = fertilize
        self.user_token = user_token

    def __repr__(self):
        return f"The following plant has been added: {self.commom_name}"

    def set_id(self):
        return secrets.token_urlsafe()

class PlantSchema(ma.Schema):
    class Meta:
        fields = ['id', 'commom_name', 'species_name', 'size', 'origin', 'light', 'shade', 'soil', 'fertilize']

plant_schema = PlantSchema()
plants_schema = PlantSchema(many = True)
