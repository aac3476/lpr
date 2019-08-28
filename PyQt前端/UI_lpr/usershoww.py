from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import json
import UI_lpr.gl_headers

class Ui_showusers(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(545, 443)
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(220, 20, 301, 391))
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 161, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(60, 300, 75, 31))
        self.pushButton.setObjectName("pushButton")

        self.pushButton.clicked.connect(lambda: self.postusers())

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "全部用户信息"))
        self.label.setText(_translate("Dialog", "当前全部用户信息"))
        self.pushButton.setText(_translate("Dialog", "刷新"))


    def postusers(self):
        url = 'http://lpr1.ywxisky.cn/user'
        r = requests.get(url, headers=UI_lpr.gl_headers.HEADERS)
        cr = json.loads(r.content.decode())

        data=cr['data']
        s = "用户信息:"
        for i in data:
            s += '\n'
            for k, v in i.items():
                s += str(k) + ": " + str(v) + "    "

        self.textEdit.setText(s)






