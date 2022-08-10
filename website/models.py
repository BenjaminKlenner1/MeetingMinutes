from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Minute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(32))
    person = db.Column(db.String(32))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    info = db.Column(db.String(10000))
    act_by = db.Column(db.String(32))
    act_req = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    minutes = db.relationship('Minute')