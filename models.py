from flask_login import UserMixin
from __init__ import db


class User(UserMixin, db.Model):
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000), primary_key=True)


class Admin(UserMixin, db.Model):
    password = db.Column(db.String(100))
    username = db.Column(db.String(1000), primary_key=True)

