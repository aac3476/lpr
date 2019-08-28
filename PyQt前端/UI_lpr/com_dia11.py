from PyQt5 import QtCore, QtGui, QtWidgets

from UI_lpr.car_idd import *
from UI_lpr.lpr import *
import UI_lpr.gl_headers


class Ui_comdia1(object):      ####
    def setupUi_com(self, Dialog):     ####
        Dialog.setObjectName("Dialog")
        Dialog.resize(411, 328)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(150, 90, 101, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 180, 101, 41))
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton.clicked.connect(lambda :self.lpr_carid())
        self.pushButton_2.clicked.connect(lambda :self.close())

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "普通用户界面"))      #####
        self.pushButton.setText(_translate("Dialog", "开始识别"))
        self.pushButton_2.setText(_translate("Dialog", "退出"))


    def lpr_carid(self):
        ctl = lprclass()
        thr = threading.Thread(target=ctl.carp)
        thr.start()
        ui_id = Ui_carid()
        dialog5 = QtWidgets.QDialog()
        ui_id.setupUi(dialog5)
        dialog5.exec_()