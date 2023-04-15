from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    #primary key
    id = db.Column(db.Integer, primary_key=True)

    #established in /signup
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

    #etablished in /profile
    fullName = db.Column(db.String(150))
    address1 = db.Column(db.String(150))
    address2 = db.Column(db.String(150))
    city = db.Column(db.String(150))
    state = db.Column(db.String(150))
    zipcode = db.Column(db.String(150))

    notes = db.relationship('Note')
    transactions = db.relationship('Transaction')

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gallons = db.Column(db.Integer)
    total = db.Column(db.Numeric(10,2))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    delivery_date = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))