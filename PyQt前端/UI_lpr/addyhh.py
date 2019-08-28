from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import json
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from UI_lpr.testt import *
import UI_lpr.gl_headers

class Ui_addyh(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(552, 419)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        Dialog.setFont(font)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(200, 40, 191, 71))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(120, 120, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(230, 160, 131, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(120, 210, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(230, 260, 131, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(140, 330, 91, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(320, 330, 91, 31))
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton.clicked.connect(lambda :self.gettxtadd())   #获得用户输入内容
        self.pushButton_2.clicked.connect(QCoreApplication.instance().quit)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "添加用户"))
        self.label.setText(_translate("Dialog", "添加用户  +"))
        self.label_2.setText(_translate("Dialog", "请输入用户名："))
        self.label_3.setText(_translate("Dialog", "请设置初始密码："))
        self.pushButton.setText(_translate("Dialog", "确定"))
        self.pushButton_2.setText(_translate("Dialog", "取消"))


    def gettxtadd(self):
        add_name=str(self.lineEdit.text())
        add_password=str(self.lineEdit_2.text())
        s = {'username': add_name, 'password':
            add_password}
        url = 'http://lpr1.ywxisky.cn/register'
        r = requests.post(url, headers=UI_lpr.gl_headers.HEADERS,data=s)
        cr = json.loads(r.content.decode())
        
        state = cr['status']
        print(state)
        if state==True:
            msgbox1 = QMessageBox()
            QMessageBox.information(msgbox1, '提示', '成功添加用户', QMessageBox.Yes)
        else:
            msgbox2 = QMessageBox()
            QMessageBox.information(msgbox2, '提示', '用户名已存在', QMessageBox.Yes)

