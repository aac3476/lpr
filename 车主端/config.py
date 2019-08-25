# -*- coding: utf-8 -*-  
"""
Create on 07-22 10:22 2019
@Author ywx 
@File config.py
"""


import os
SQLALCHEMY_DATABASE_URI = 'mysql://lpr:L4hfT6aDw5NXFD7e@152.32.134.49:8310/lpr?charset=utf8'
SQLALCHEMY_MIGRATE_REPO = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_TEARDOWN = True

CSRF_ENABLED = True
SECRET_KEY = 'ae18daeasi0djwrq5162cbe1ee07f1fa8'

DROPZONE_MAX_FILE_SIZE = 16*1024*1024
DROPZONE_ALLOWED_FILE_TYPE = 'image'
DROPZONE_ENABLE_CSRF=True