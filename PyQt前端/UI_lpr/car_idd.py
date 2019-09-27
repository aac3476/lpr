from PyQt5 import QtCore, QtGui, QtWidgets
from UI_lpr.gl_headers import *
from UI_lpr.lpr import *
import requests
import sys
import json
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from .lpr import datalist
state=''



class Ui_carid(object):
    def __init__(self):
        self.timer = QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.findcarid)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(777, 436)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(260, 20, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(210, 100, 141, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(90, 100, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(60, 170, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(210, 240, 141, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(100, 240, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 320, 91, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(160, 320, 91, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(210, 170, 141, 22))
        self.comboBox.setEditable(False)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(430, 80, 311, 201))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(430, 325, 291, 61))
        self.label_6.setObjectName("label_6")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(290, 320, 91, 41))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pushButton.clicked.connect(lambda: self.clear())
        self.pushButton_2.clicked.connect(lambda: self.sendinf())
        self.pushButton_3.clicked.connect(lambda: self.pay())
        

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "使用界面"))
        self.label.setText(_translate("Dialog", "当前通过车辆信息"))
        self.label_2.setText(_translate("Dialog", "车牌号："))
        self.label_3.setText(_translate("Dialog", "选择行车方向："))
        self.label_4.setText(_translate("Dialog", "地点："))
        self.pushButton_2.setText(_translate("Dialog", "上传信息及图片"))
        self.pushButton_3.setText(_translate("Dialog", "下道付款"))
        self.comboBox.setCurrentText(_translate("Dialog", "上道口"))
        self.comboBox.setItemText(0, _translate("Dialog", "上道口"))
        self.comboBox.setItemText(1, _translate("Dialog", "下道口"))
        self.label_5.setText(_translate("Dialog", "未有车牌图片传入"))
        self.label_6.setText(_translate("Dialog", "未上传信息"))
        self.pushButton.setText(_translate("Dialog", "清空"))

    def clear(self):
        self.label_5.setPixmap(QPixmap(""))
        self.lineEdit.setText("")

    def sendinf(self):
        global state
        text=self.comboBox.currentText()
        car = str(self.lineEdit.text() )     # 读取当前文本框中车牌号（可能有人为改动）
        pos = self.lineEdit_2.text()
        s = {'car': car, 'pos':
            pos}
        if text=="下道口":
            url = 'http://lpr1.ywxisky.cn/godown'
            r = requests.post(url, data=s,headers=UI_lpr.gl_headers.HEADERS)
            cr = json.loads(r.content.decode())
            msgd=cr['msg']
            state=cr['status']
            if state==False:
                self.label_6.setText(str(msgd))
            data=cr['data']
            id_go=data['id']
            UI_lpr.gl_headers.TYPE=1
        else:
            url = 'http://lpr1.ywxisky.cn/goup'
            r = requests.post(url, data=s, headers=UI_lpr.gl_headers.HEADERS)
            cr = json.loads(r.content.decode())
            msgu = cr['msg']
            state = cr['status']
            if state == False:
                self.label_6.setText(str(msgu))
            data = cr['data']
            id_go= data['id']
            UI_lpr.gl_headers.TYPE=0
        UI_lpr.gl_headers.ID = id_go
        if state == True:
        
            if datalist.empty():
                # 没有数据进入，处理别的事情
                pass
            else:
                data = datalist.get(block=True, timeout=None)
                pic_id = str(data['id'])
                # 这里接收数据，图片从pic/data['id'].jpg读取，用完之后记得删除
                # os.unlink('pic/'+str(data ['id']+'.jpg')

                f1 = open(r'./pic/' + pic_id + '.jpg', 'rb')
                s = {'id': UI_lpr.gl_headers.ID, 'type': UI_lpr.gl_headers.TYPE}
                
                files = {'file': (pic_id + '.jpg', f1, 'image/jpeg', {})}
                url = 'http://lpr1.ywxisky.cn/uppic'
                r = requests.post(url, headers=UI_lpr.gl_headers.HEADERS, data=s, files=files)
                f1.close()
                cr = json.loads(r.content.decode())
                
                msgp = str(cr['msg'])
                statee=cr['status']
                if statee == True:
                    msgpp = str(car)+"信息及图片上传" + msgp
                    self.label_6.setText(str(msgpp))
                    if text=="上道口":         #上道后上传信息成功 清空文本框 标签
                        self.label_5.setPixmap(QPixmap(""))
                        self.lineEdit.setText("")
                        self.lineEdit_2.setText("")

                else:
                    self.label_6.setText(str(msgp))
                
                os.unlink(r'./pic/' + pic_id + '.jpg')
    


    def pay(self):
        url = 'http://lpr1.ywxisky.cn/pay'
        car = str(self.lineEdit.text() )                              #UI_lpr.gl_headers.CNUM
        s = {'car': car}
        r = requests.post(url, data=s, headers=UI_lpr.gl_headers.HEADERS)
        cr = json.loads(r.content.decode())
        msgp = cr['msg']
        statep= cr['status']
        self.label_6.setText(str(msgp))
        if statep == True:    #付费成功 清除图片和文本框
            self.label_5.setPixmap(QPixmap(""))
            self.lineEdit.setText("")
            self.lineEdit_2.setText("")



    def findcarid(self):
        if UI_lpr.gl_headers.CNUM == 0:
            pass
        else:
            self.lineEdit.setText(UI_lpr.gl_headers.CNUM)      #车牌号自动出现
            pix = QtGui.QPixmap('./pic/'+str(UI_lpr.gl_headers.PICNUM)+'.jpg')  #加str()
            self.label_5.setPixmap(pix)                   #在标签中显示车牌的截图
            self.label_5.setScaledContents(True)
            UI_lpr.gl_headers.CNUM = 0

