# -*- coding: utf-8 -*-  
"""
Create on 07-25 19:20 2019
@Author ywx 
@File apis.py
"""

from app import app,db
from flask import request,jsonify,Response
from app.models import Users,Toll
from app.common import trueReturn,falseReturn,currentUser,calmoney,filehash
from app.Auth import Auth
from hyperlpr import *
import datetime,os,hashlib,shutil,re,cv2


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
    usr = Users.query.filter_by(username=username).first()
    if usr is not None:
        return falseReturn(-2, '用户名已被注册')
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
    return trueReturn({"id":column.id})


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
        if toll.status is not None:
            if toll.status == 1:
                rtn = {
                    'code': 3,
                    'fee': toll.fee,
                    'upp': toll.upp,
                    'upt': toll.upt.strftime("%Y-%m-%d %H:%M:%S"),
                    'id': toll.id
                }
                return falseReturn(rtn, "车辆已下道且完成付费")
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
    db.session.add(toll)
    db.session.commit()
    rtn={
        'code':1,
        'fee':toll.fee,
        'upp':toll.upp,
        'upt':toll.upt.strftime("%Y-%m-%d %H:%M:%S"),
        'id':toll.id
    }
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


@app.route('/uppic',methods=['POST'])
def uppic():
    '''
    上传照片证据
    :param: id:goup或godown接口中返回的id
    :param: type:指明是上道还是下道，整数类型，0为上道照片，1为下道照片
    :param: file:照片 png，jepg，jpg，gif 其中的一种格式
    :return:json
    '''
    User = currentUser()
    if User[0] == False:
        return falseReturn(User[1])
    id = request.form.get("id")
    type = int(request.form.get("type"))
    f = request.files["file"]

    if id is None or type is None or f  is None:
        rtn = {
            'code': -1,
        }
        return falseReturn(rtn, "参数不完整")
    file = ['png', 'jpg', 'gif', 'jpeg']
    ffilename = f.filename
    hou = f.filename.split('.')[1].lower()
    if hou not in file:
        return falseReturn({'code':-1},'不合法的图片格式')
    fpath = os.path.join('app/upload', ffilename)
    f.save(fpath)
    nfilename = filehash(hashlib.md5, fpath) + filehash(hashlib.sha1, fpath) + "." + hou
    nfilepath = os.path.join('app/pic', nfilename)
    check = os.path.exists(nfilepath)
    if check:
        os.unlink(fpath)
        return falseReturn({'code': -2}, '图片已经存在')


    data = Toll.query.filter_by(id=id).first()
    if type == 0:
        if data.uppic is not None:
            if data.uppic == nfilename:
                os.unlink(fpath)
                return falseReturn({'code': -2}, '重复上传')
            else:
                os.unlink(os.path.join('app/pic', data.uppic))
        data.uppic=nfilename
        shutil.copy(fpath, nfilepath)
        os.unlink(fpath)
        db.session.add(data)
        db.session.commit()
        return trueReturn({'code':1})
    else:
        if data.downpic is not None:
            if data.downpic == nfilename:
                os.unlink(fpath)
                return falseReturn({'code': -2}, '重复上传')
            else:
                os.unlink(os.path.join('app/pic', data.downpic))
        data.downpic=nfilename
        shutil.copy(fpath, nfilepath)
        os.unlink(fpath)
        db.session.add(data)
        db.session.commit()
        return trueReturn({'code':1})


@app.route("/getimg/<imageid>")
def image(imageid):
    '''
    取得照片证据
    :return:pic
    '''
    path = os.path.join('app/pic', imageid)
    mdict = {
        'jpeg': 'image/jpeg',
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif'
    }
    if len(imageid.split('.'))>1:
        mime = mdict[imageid.split('.')[1].lower()]

        f =  open(os.path.join('app/pic', imageid),'rb')
        imgstream=f.read()
        f.close()
        return Response(imgstream,mimetype=mime)
    else:
        return "error",404


@app.route('/identify',methods=['POST','GET'])
def identify():
    '''
        c++预留接口，车牌识别
        :return:车牌
    '''
    carre = "^(京[A-HJ-NPQY]|沪[A-HJ-N]|津[A-HJ-NPQR]|渝[A-DFGHN]|冀[A-HJRST]|晋[A-FHJ-M]|蒙[A-HJKLM]|辽[A-HJ-NP]|吉[A-HJK]|黑[A-HJ-NPR]|苏[A-HJ-N]|浙[A-HJKL]|皖[A-HJ-NP-S]|闽[A-HJK]|赣[A-HJKLMS]|鲁[A-HJ-NP-SUVWY]|豫[A-HJ-NP-SU]|鄂[A-HJ-NP-S]|湘[A-HJ-NSU]|粤[A-HJ-NP-Y]|桂[A-HJ-NPR]|琼[A-F]|川[A-HJ-MQ-Z]|贵[A-HJ]|云[AC-HJ-NP-SV]|藏[A-HJ]|陕[A-HJKV]|甘[A-HJ-NP]|青[A-H]|宁[A-E]|新[A-HJ-NP-S])([0-9A-HJ-NP-Z]{4}[0-9A-HJ-NP-Z挂试]|[0-9]{4}学|[A-D0-9][0-9]{3}警|[DF][0-9A-HJ-NP-Z][0-9]{4}|[0-9]{5}[DF])$|^WJ[京沪津渝冀晋蒙辽吉黑苏浙皖闽赣鲁豫鄂湘粤桂琼川贵云藏陕甘青宁新]?[0-9]{4}[0-9JBXTHSD]$|^(V[A-GKMORTV]|K[A-HJ-NORUZ]|H[A-GLOR]|[BCGJLNS][A-DKMNORVY]|G[JS])[0-9]{5}$|^[0-9]{6}使$|^([沪粤川渝辽云桂鄂湘陕藏黑]A|闽D|鲁B|蒙[AEH])[0-9]{4}领$|^粤Z[0-9A-HJ-NP-Z][0-9]{3}[港澳]$"
    u = request.values.get('u')
    p = request.values.get('p')
    sql = "SELECT * FROM cppuser where name = '%s' and apikey='%s'" % (u, p)
    userres = db.session.execute(sql).fetchall()
    print(userres)
    if len(userres) == 0:
        res = 'api_username或api_key错误，为了接口安全使用本接口需要申请apikey'
        return res.encode("gb2312")
    print(userres[0][0])
    f = request.files['picurl']
    file = ['png', 'jpg', 'gif', 'jpeg']
    ffilename = f.filename
    hou = f.filename.split('.')[1].lower()
    if hou not in file:
        return falseReturn({'code': -1}, '不合法的图片格式')
    fpath = os.path.join('app/upload', ffilename)
    f.save(fpath)
    image = cv2.imread(fpath)
    ress = HyperLPR_PlateRecogntion(image)
    res = ""
    for x in ress:
        if re.match(carre, x[0]):
            res = x[0]
    if res == "":
        res = "no result"

    os.unlink(fpath)
    sql = "INSERT INTO apihistory (name,time,picname,result) VALUES ('%s',now(),'%s','%s')"%(userres[0][1],ffilename,res)
    db.session.execute(sql)
    db.session.commit()
    return   res.encode("gb2312")