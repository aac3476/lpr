# -*- coding: utf-8 -*-  
"""
Create on 07-25 19:24 2019
@Author ywx 
@File common.py
"""

from app.Auth import Auth
from app.models import Users
from flask import request
import hashlib,os


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


__supported_hashfunc = {'md5':hashlib.md5, 'sha1':hashlib.sha1, 'sha224':hashlib.sha224, 'sha256':hashlib.sha256, 'sha384':hashlib.sha384, 'sha512':hashlib.sha512}
__FILE_SLIM = (100*1024*1024) # 100MB

def filehash(hfunc,filename):
    hobj = hfunc()
    fp = open(filename,"rb")
    f_size = os.stat(filename).st_size
    while(f_size > __FILE_SLIM):
        hobj.update(fp.read(__FILE_SLIM))
        f_size /= __FILE_SLIM
        #print("o.o")
    if(f_size>0) and (f_size <= __FILE_SLIM):
            hobj.update(fp.read())
    fp.close()
    return hobj.hexdigest()