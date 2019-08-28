from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import UI_lpr.gl_headers
import json
import requests


class Ui_delyh(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(404, 321)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(120, 40, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(90, 110, 241, 61))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(130, 180, 171, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(100, 250, 61, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(250, 252, 61, 31))
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton.clicked.connect(lambda: self.getxtdel())  # 获得用户输入内容
        self.pushButton_2.clicked.connect(QCoreApplication.instance().quit)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "删除用户"))
        self.label.setText(_translate("Dialog", "删除用户    -"))
        self.label_2.setText(_translate("Dialog", "请输入要删除的用户名："))
        self.pushButton.setText(_translate("Dialog", "确定"))
        self.pushButton_2.setText(_translate("Dialog", "取消"))


    def getxtdel(self):
        del_name=str(self.lineEdit.text())
        s = {'username': del_name}
        url = 'http://lpr1.ywxisky.cn/deleteu'
        print(del_name)
        print(UI_lpr.gl_headers.HEADERS)

        r = requests.post(url, headers=UI_lpr.gl_headers.HEADERS, data=s)
        cr = json.loads(r.content.decode())
        state=cr['status']
        if state=='True':
            msgbox1 = QMessageBox()
            QMessageBox.information(msgbox1, '提示', '删除成功', QMessageBox.Yes)

        else:
            msgbox2 = QMessageBox()
            QMessageBox.information(msgbox2, '提示', '找不到用户', QMessageBox.Yes)
