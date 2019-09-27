
from PyQt5 import QtCore, QtGui, QtWidgets
from UI_lpr.addyhh import *
from UI_lpr.delyhh import *
from UI_lpr.usershoww import *
from UI_lpr.car_idd import *
from UI_lpr.lpr import *
import UI_lpr.gl_headers


class Ui_addia1(object):                  #改变类名为Ui_addia1
    def setupUi_addia1(self, Dialog):      #改变函数名为setupUi_addia1
        Dialog.setObjectName("Dialog")
        Dialog.resize(447, 342)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(100, 100, 101, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(250, 100, 101, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(100, 170, 101, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(250, 170, 101, 41))
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton.clicked.connect(lambda: self.addyh())     #进入添加用户界面 信号与槽
        self.pushButton_3.clicked.connect(lambda:self.delyh())
        self.pushButton_4.clicked.connect(lambda:self.usershow())
        self.pushButton_2.clicked.connect(lambda:self.lpr_carid())


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "管理员界面"))    #改对话框名字
        self.pushButton.setText(_translate("Dialog", "添加用户"))
        self.pushButton_2.setText(_translate("Dialog", "使用界面"))
        self.pushButton_3.setText(_translate("Dialog", "删除用户"))
        self.pushButton_4.setText(_translate("Dialog", "用户信息"))


    def addyh(self):
        ui_addyh=Ui_addyh()
        dialog2=QtWidgets.QDialog()
        ui_addyh.setupUi(dialog2)
        dialog2.exec_()

    def delyh(self):
        ui_delyh=Ui_delyh()
        dialog3=QtWidgets.QDialog()
        ui_delyh.setupUi(dialog3)
        dialog3.exec_()


    def usershow(self):
        ui_usershow=Ui_showusers()
        dialog4=QtWidgets.QDialog()
        ui_usershow.setupUi(dialog4)
        dialog4.exec_()


     def lpr_carid(self):
        ctl = lprclass()
        thr = threading.Thread(target=ctl.carp)
        thr.start()
        ui_id = Ui_carid()
        dialog5 = QtWidgets.QDialog()
        ui_id.setupUi(dialog5)
        dialog5.exec_()
