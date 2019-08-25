# -*- coding: utf-8 -*-  
"""
Create on 07-22 10:14 2019
@Author ywx 
@File __init__.py.py
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_dropzone import Dropzone

import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config.from_object('config')
dropzone = Dropzone(app)
csrf = CSRFProtect(app)

login_manger=LoginManager()
login_manger.login_view='login'
login_manger.login_message = ""
login_manger.init_app(app)



db = SQLAlchemy(app)
db.create_all()

from .views import index
from app import models



