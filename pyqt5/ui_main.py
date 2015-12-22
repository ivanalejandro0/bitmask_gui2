# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Fri Dec 18 12:49:39 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Main(object):
    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(361, 524)
        self.gridLayout_3 = QtWidgets.QGridLayout(Main)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox = QtWidgets.QGroupBox(Main)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.leUsername = QtWidgets.QLineEdit(self.groupBox)
        self.leUsername.setObjectName("leUsername")
        self.gridLayout_2.addWidget(self.leUsername, 0, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.lePassword = QtWidgets.QLineEdit(self.groupBox)
        self.lePassword.setObjectName("lePassword")
        self.gridLayout_2.addWidget(self.lePassword, 1, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 1, 2, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)
        self.gbEIP = QtWidgets.QGroupBox(Main)
        self.gbEIP.setObjectName("gbEIP")
        self.gridLayout = QtWidgets.QGridLayout(self.gbEIP)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pbStart = QtWidgets.QPushButton(self.gbEIP)
        self.pbStart.setObjectName("pbStart")
        self.horizontalLayout.addWidget(self.pbStart)
        self.pbStop = QtWidgets.QPushButton(self.gbEIP)
        self.pbStop.setObjectName("pbStop")
        self.horizontalLayout.addWidget(self.pbStop)
        self.pbStatus = QtWidgets.QPushButton(self.gbEIP)
        self.pbStatus.setObjectName("pbStatus")
        self.horizontalLayout.addWidget(self.pbStatus)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.lblStatus = QtWidgets.QLabel(self.gbEIP)
        self.lblStatus.setObjectName("lblStatus")
        self.gridLayout.addWidget(self.lblStatus, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.gbEIP, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 309, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 2, 0, 1, 1)

        self.retranslateUi(Main)
        QtCore.QMetaObject.connectSlotsByName(Main)

    def retranslateUi(self, Main):
        _translate = QtCore.QCoreApplication.translate
        Main.setWindowTitle(_translate("Main", "Bitmask"))
        self.groupBox.setTitle(_translate("Main", "Login"))
        self.label.setText(_translate("Main", "Username"))
        self.pushButton.setText(_translate("Main", "Login"))
        self.label_2.setText(_translate("Main", "Password"))
        self.pushButton_2.setText(_translate("Main", "Logout"))
        self.gbEIP.setTitle(_translate("Main", "EIP"))
        self.pbStart.setText(_translate("Main", "Start"))
        self.pbStop.setText(_translate("Main", "Stop"))
        self.pbStatus.setText(_translate("Main", "Status"))
        self.lblStatus.setText(_translate("Main", "Status:"))

