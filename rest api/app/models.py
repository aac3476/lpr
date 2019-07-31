# -*- coding: utf-8 -*-  
"""
Create on 07-22 16:51 2019
@Author ywx 
@File models.py
"""

from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(250),  unique=True, nullable=False)
    password = db.Column(db.String(250))
    login_time = db.Column(db.Integer)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
        return "Users(id='%s')" % self.id

    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, hash, password):
        return check_password_hash(hash, password)

    def get(self, id):
        return self.query.filter_by(id=id).first()

    def add(self, user):
        db.session.add(user)
        return session_commit()

    def update(self):
        return session_commit()

    def delete(self, id):
        self.query.filter_by(id=id).delete()
        return session_commit()


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason




class Toll(db.Model):
    __tablename__ = 'toll'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    car = db.Column(db.VARCHAR(10))
    status = db.Column(db.Boolean())
    upp = db.Column(db.VARCHAR(255))
    upt = db.Column(db.DateTime)
    downp = db.Column(db.VARCHAR(255))
    downt = db.Column(db.DateTime)
    fee = db.Column(db.Integer)
    upu = db.Column(db.Integer)
    downu = db.Column(db.Integer)
    uppic = db.Column(db.VARCHAR(255))
    downpic = db.Column(db.VARCHAR(255))
    def __repr__(self):
        return self.id

