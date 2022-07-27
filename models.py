from dataclasses import dataclass
import email
from enum import unique
from re import U
from sqlalchemy import LABEL_STYLE_TABLENAME_PLUS_COL, PrimaryKeyConstraint
from .import db # importing from the __init__ file!
from flask_login import UserMixin # special class...helps users login
from sqlalchemy.sql import func


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True) # user id is primary_key
    email = db.Column(db.String(160), unique=True) 
    password = db.Column(db.String(255))
    firstName = db.Column(db.String(255))
    lastName = db.Column(db.String(255))
    phone_number = db.Column(db.Integer)

class Dependents(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    dependents = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Employment_status(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    work_status = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Income(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    income = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class LoanAmount(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    amount = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class LoanTerm(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    duration = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))       

class CreditScore(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    credit_score = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Documents(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    document = db.Column(db.Text, unique=True, nullable=False) # stores the document metadata
    name = db.Column(db.Text, nullable=False) 
    mimetype = db.Column(db.Text, nullable=False) # type of doc (word, pdf, etc.)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 


