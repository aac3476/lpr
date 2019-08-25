# -*- coding: utf-8 -*-  
"""
Create on 07-22 10:25 2019
@Author ywx 
@File index.py
"""

from flask import render_template,redirect,url_for,request,Response
from flask_login import login_required,current_user,login_user,logout_user
from app import app,db
from ..models import User,Toll
from ..forms import LoginForm
from ..common import create_md5,filehash,paicheck
from app import csrf
import hashlib,os,cv2,datetime,shutil,json,time
from hyperlpr import HyperLPR_PlateRecogntion

@app.route('/')
@app.route('/index')
@login_required
def index():
    sqla = "SELECT COUNT(*) FROM toll where car = '%s'" % current_user.car
    sqlb = "SELECT sum(fee) from toll where car = '%s'" % current_user.car
    total = db.session.execute(sqla).fetchall()
    money = db.session.execute(sqlb).fetchall()
    return render_template('index.html',total=total[0][0],money=money[0][0])


@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        pai = form.name.data
        usr = User.query.filter_by(car=pai).first()
        passwd = form.passw.data
        print(pai,paicheck(pai))
        if usr is None:
            if paicheck(pai) == False:
                return render_template('login.html', form=form,notice=1, text="当前登录账号未注册且不符合车牌格式")
            if passwd == '123456':
                usr = User(car=pai,password=create_md5(passwd))
                db.session.add(usr)
                db.session.commit()
                login_user(usr, True)
                return (redirect(url_for('index')))
            else:
                return render_template('login.html', form=form,notice=1, text="当前帐号未登陆过系统，请使用默认密码123456")

        passwd = create_md5(passwd)
        if passwd == usr.password:
            login_user(usr, True)
            return (redirect(url_for('index')))
        else:
            return render_template('login.html', form=form,notice=1, text="密码错误")

    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return (redirect(url_for('login')))


@app.route('/detail')
@login_required
def detail():
    res = Toll.query.filter_by(car=current_user.car).all()
    result = []
    for resulta in res:
        ths = {'car':resulta.car,'downp':resulta.downp,'downpic':resulta.downpic,'upp':resulta.upp,'uppic':resulta.uppic,'fee':resulta.fee,'downt':resulta.downt,'upt':resulta.upt}
        result.append(ths)
    return render_template("detail.html",lst=result)
    pass



@app.route('/cp',methods=['POST'])
@login_required
def cp():
    password = request.form['password']
    print(password)
    usr = User.query.filter_by(car=current_user.car).first()
    usr.password=create_md5(password)
    db.session.add(usr)
    db.session.commit()
    rtn={'code':1,'msg':'success'}
    return json.dumps(rtn)