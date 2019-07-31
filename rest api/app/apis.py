# -*- coding: utf-8 -*-  
"""
Create on 07-25 19:20 2019
@Author ywx 
@File apis.py
"""

from app import app,db
from flask import request
from flask import jsonify
from app.models import Users,Toll
from app.common import trueReturn,falseReturn,currentUser,calmoney
from app.Auth import Auth
import datetime


@app.route('/login', methods=['POST'])
def login():
    """
    用户登录
    :param username:用户名
    :param password:密码
    :return: json
    """
    username = request.form.get('username')
    password = request.form.get('password')
    if (not username or not password):
        return jsonify(falseReturn('', '用户名和密码不能为空'))
    else:
        return Auth.authenticate(Auth, username, password)


@app.route('/register', methods=['POST'])
def register():
    """
    用户注册
    :param username:用户名
    :param password:密码
    :return: json
    """
    User = currentUser()
    if User[0] == False or User[1]['username']!='admin':
        rtn={
            'code':-1
        }
        return falseReturn(rtn,'没有权限，访问被拒绝')
    username = request.form.get('username')
    password = request.form.get('password')
    print(username,password)
    user = Users(username=username, password=Users.set_password(username, password))
    result = Users.add(username, user)
    if user.id is not None:
        returnUser = {
            'id': user.id,
            'username': user.username,
            'login_time': user.login_time
        }
        return jsonify(trueReturn(returnUser, "用户注册成功"))
    else:
        return jsonify(falseReturn('', '用户注册失败'))


@app.route('/deleteu',methods=['POST'])
def deleteu():
    """
    删除用户
    :param:username:用户名
    :return:json
    """
    User = currentUser()
    if User[0] == False or User[1]['username'] != 'admin':
        rtn = {
            'code': -1
        }
        return falseReturn(rtn, '没有权限，访问被拒绝')
    username = request.form.get('username')
    if username == 'admin':
        return falseReturn(-1,'不能删除自己')
    usr = Users.query.filter_by(username = username).first()
    if usr is None:
        return falseReturn(-2,'找不到用户')
    db.session.delete(usr)
    db.session.commit()
    return trueReturn("success")


@app.route('/user', methods=['GET'])
def get():
    """
    获取用户信息
    :return: json
    """
    User = currentUser()
    if User[0] == False or User[1]['username'] != 'admin':
        rtn = {
            'code': -1
        }
        return falseReturn(rtn, '没有权限，访问被拒绝')
    usrs = db.session.query(Users).all()
    returnUser = []
    for usr in usrs:
        urd ={
            'id':usr.id,
            'name':usr.username
        }
        returnUser.append(urd)
    return trueReturn(returnUser, "请求成功")



@app.route('/test')
def test():
    User = currentUser()
    if User[0]:
        return trueReturn(User[1])
    else:
        return falseReturn(User[1])



@app.route('/goup',methods=['POST'])
def goup():
    '''
    车辆进入高速
    :param car:车牌号
    :param pos:上道口
    :return:json
    '''
    User = currentUser()
    if User[0] == False:
        return falseReturn(User[1])
    car = request.form.get("car")
    pos = request.form.get("pos")
    if car is None or pos is None:
        rtn = {
            'code': -1,
        }
        return falseReturn(rtn,"参数不完整")
    checkhistory = Toll.query.filter_by(car=car,status=0).first()
    rtn={}
    if checkhistory is not None:
        rtn={
            'code':-5,
            'time':checkhistory.upt.strftime("%Y-%m-%d %H:%M:%S"),
            'pos':checkhistory.upp,
            'id':checkhistory.id
        }
        return falseReturn(rtn,"车辆有未驶出的记录")

    column = Toll(car=car,upu=[User[1]['id']],upt=datetime.datetime.now(),upp=pos,status=0)
    db.session.add(column)
    db.session.commit()
    return trueReturn('success')


@app.route('/godown',methods=['POST'])
def godown():
    '''
    车辆离开高速
    :param car:车牌号
    :param pos:下道口
    :return:json
    '''
    User = currentUser()
    if User[0] == False:
        return falseReturn(User[1])
    car = request.form.get("car")
    pos = request.form.get("pos")
    if car is None or pos is None:
        rtn = {
            'code': -1,
        }
        return falseReturn(rtn, "参数不完整")
    toll = Toll.query.filter_by(car=car, status=0).first()
    rtn = {}
    if toll is  None:
        rtn = {
            'code': -4,
        }
        return falseReturn(rtn, "车辆没有上道记录")
    if toll.downp is not None:
        rtn = {
            'code': 2,
            'fee': toll.fee,
            'upp': toll.upp,
            'upt': toll.upt.strftime("%Y-%m-%d %H:%M:%S"),
            'id':toll.id
        }
        return falseReturn(rtn,"车辆当前已在下道口但未付费")
    toll.downp = pos
    toll.downt = datetime.datetime.now()
    toll.downu = User[1]['id']
    toll.fee = calmoney(toll.upp,pos)
    rtn={
        'code':1,
        'fee':toll.fee,
        'upp':toll.upp,
        'upt':toll.upt.strftime("%Y-%m-%d %H:%M:%S"),
    }
    db.session.add(toll)
    db.session.commit()
    return trueReturn(rtn)


@app.route('/pay',methods=['POST'])
def pay():
    '''
    车辆支付过路费
    :param: car:下道车辆
    :return:json
    '''
    User = currentUser()
    if User[0] == False:
        return falseReturn(User[1])
    car = request.form.get("car")
    if car is None:
        rtn = {
            'code': -1,
        }
        return falseReturn(rtn, "参数不完整")
    toll = Toll.query.filter_by(car=car, status=0).first()
    rtn = {}
    if toll is  None:
        rtn = {
            'code': -4,
        }
        return falseReturn(rtn, "车辆没有上道记录")
    if toll.fee is not None:
        toll.status=1
        db.session.add(toll)
        db.session.commit()
        return falseReturn("success", "支付成功")
    rtn = {
        'code': -3,
    }
    return falseReturn(rtn, "车辆没有下道记录")