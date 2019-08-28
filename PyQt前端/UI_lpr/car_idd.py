from PyQt5 import QtCore, QtGui, QtWidgets
import UI_lpr.gl_headers
from UI_lpr.lpr import *
from PyQt5.QtWidgets import *
import requests
import sys
import json



class Ui_carid(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(516, 424)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(150, 40, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(210, 130, 141, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(90, 120, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(60, 190, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(210, 270, 141, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(100, 260, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(70, 340, 71, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(180, 340, 71, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(400, 340, 71, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(210, 200, 141, 22))
        self.comboBox.setEditable(False)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(290, 340, 71, 31))
        self.pushButton_4.setObjectName("pushButton_4")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.pushButton.clicked.connect(lambda: self.updata())
        self.pushButton_2.clicked.connect(lambda: self.sendinf())
        self.pushButton_3.clicked.connect(lambda: self.pay())
        self.pushButton_4.clicked.connect(lambda: self.sendpic())

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "车辆信息"))
        self.label.setText(_translate("Dialog", "当前通过车辆信息"))
        self.label_2.setText(_translate("Dialog", "车牌号："))
        self.label_3.setText(_translate("Dialog", "选择行车方向："))
        self.label_4.setText(_translate("Dialog", "地点："))
        self.pushButton.setText(_translate("Dialog", "获取车牌号"))
        self.pushButton_2.setText(_translate("Dialog", "上传信息"))
        self.pushButton_3.setText(_translate("Dialog", "付款"))
        self.comboBox.setCurrentText(_translate("Dialog", "上道口"))
        self.comboBox.setItemText(0, _translate("Dialog", "上道口"))
        self.comboBox.setItemText(1, _translate("Dialog", "下道口"))
        self.pushButton_4.setText(_translate("Dialog", "截图保存"))

    def updata(self):
        self.lineEdit.setText(UI_lpr.gl_headers.CNUM)

    def sendinf(self):
        text=self.comboBox.currentText()
        car = UI_lpr.gl_headers.CNUM
        pos = self.lineEdit_2.text()
        s = {'car': car, 'pos':
            pos}
        if text=="下道口":
            url = 'http://lpr1.ywxisky.cn/godown'
            r = requests.post(url, data=s,headers=UI_lpr.gl_headers.HEADERS)
            cr = json.loads(r.content.decode())
            print(r.content.decode())
            msgd=cr['msg']
            state=cr['status']
            msgbox1 = QMessageBox()
            QMessageBox.information(msgbox1, '提示',str(msgd), QMessageBox.Yes)
            data=cr['data']
            id_go=data['id']
            UI_lpr.gl_headers.TYPE=1
            print("下道")
        else:
            url = 'http://lpr1.ywxisky.cn/goup'
            r = requests.post(url, data=s, headers=UI_lpr.gl_headers.HEADERS)
            cr = json.loads(r.content.decode())
            print(r.content.decode())
            msgu = cr['msg']
            state = cr['status']
            msgbox2 = QMessageBox()
            QMessageBox.information(msgbox2, '提示', str(msgu), QMessageBox.Yes)
            data = cr['data']
            id_go= data['id']
            UI_lpr.gl_headers.TYPE=0
            print("上道")
        UI_lpr.gl_headers.ID=id_go

    def sendpic(self):
        self.timer = QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(lpr)



    def pay(self):
        url = 'http://lpr1.ywxisky.cn/pay'
        car = UI_lpr.gl_headers.CNUM
        s = {'car': car}
        r = requests.post(url, data=s, headers=UI_lpr.gl_headers.HEADERS)
        cr = json.loads(r.content.decode())
        msgp = cr['msg']
        msgbox3 = QMessageBox()
        QMessageBox.information(msgbox3, '提示', str(msgp), QMessageBox.Yes)


    '''
    self.pushButton.clicked.connect(lambda:self.updata())
            self.pushButton_2.clicked.connect(lambda:self.sendinf())
            self.pushButton_3.clicked.connect(lambda:self.pay())
            '''