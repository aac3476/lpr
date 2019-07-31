# -*- coding: utf-8 -*-  
"""
Create on 07-25 19:24 2019
@Author ywx 
@File common.py
"""

from app.Auth import Auth
from app.models import Users
from flask import request
def trueReturn(data, msg="请求成功"):
    return {
        "status": True,
        "data": data,
        "msg": msg
    }


def falseReturn(data, msg="请求失败"):
    return {
        "status": False,
        "data": data,
        "msg": msg
    }


def currentUser():
    result = Auth.identify(Auth, request)
    if (result['status'] and result['data']):
        user = Users.get(Users, result['data'])
        returnUser = {
            'id': user.id,
            'username': user.username,
            'login_time': user.login_time
        }
        return [True,returnUser]
    return [False,result]


def calmoney(upp,dowp):
    return 10
