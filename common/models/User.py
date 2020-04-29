# coding: utf-8
from sqlalchemy import BigInteger, Column, String
from sqlalchemy.schema import FetchedValue
from flask_sqlalchemy import SQLAlchemy
from application import db



class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    phone_number = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    first_name = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    middle_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    mail_address = db.Column(db.String(200))
    occupation = db.Column(db.String(2000))
    user_name = db.Column(db.String(200), nullable=False, unique=True, server_default=db.FetchedValue())
    password = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
