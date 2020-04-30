# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/dragon_test.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dragonTest(object):
    def setupUi(self, dragonTest):
        dragonTest.setObjectName("dragonTest")
        dragonTest.setWindowModality(QtCore.Qt.ApplicationModal)
        dragonTest.resize(399, 275)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(25)
        sizePolicy.setHeightForWidth(dragonTest.sizePolicy().hasHeightForWidth())
        dragonTest.setSizePolicy(sizePolicy)
        dragonTest.setMaximumSize(QtCore.QSize(16777192, 16777215))
        dragonTest.setSizeIncrement(QtCore.QSize(30, 27))
        dragonTest.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        dragonTest.setFont(font)
        dragonTest.setToolTipDuration(-12)
        self.checkBox = QtWidgets.QCheckBox(dragonTest)
        self.checkBox.setGeometry(QtCore.QRect(270, 210, 71, 16))
        self.checkBox.setObjectName("checkBox")
        self.label = QtWidgets.QLabel(dragonTest)
        self.label.setGeometry(QtCore.QRect(130, 40, 54, 12))
        self.label.setObjectName("label")

        self.retranslateUi(dragonTest)
        QtCore.QMetaObject.connectSlotsByName(dragonTest)

    def retranslateUi(self, dragonTest):
        _translate = QtCore.QCoreApplication.translate
        dragonTest.setWindowTitle(_translate("dragonTest", "Form"))
        self.checkBox.setText(_translate("dragonTest", "确定"))
        self.label.setText(_translate("dragonTest", "相机组配置"))

