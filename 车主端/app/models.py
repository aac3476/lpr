# -*- coding: utf-8 -*-  
"""
Create on 07-22 16:51 2019
@Author ywx 
@File models.py
"""

from app import db
from . import login_manger
from flask_login import UserMixin


@login_manger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'carowner'
    id = db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    car = db.Column(db.VARCHAR(255),nullable=False)
    password = db.Column(db.VARCHAR(255),nullable=False)
    def __repr__(self):
        return self.id


class breakr(db.Model):
    __tablename__ = 'breakr'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    car = db.Column(db.VARCHAR(10))
    type = db.Column(db.VARCHAR(255))
    position = db.Column(db.VARCHAR(255))
    evidence = db.Column(db.VARCHAR(255))
    time = db.Column(db.DateTime)
    uploadtime = db.Column(db.DateTime)
    ispunish = db.Column(db.Integer)
    def __repr__(self):
        return self.id


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
        return self.car

