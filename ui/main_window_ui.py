# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(988, 565)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pic/images/python.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 20, 901, 481))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.multiHtml = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.multiHtml.setContentsMargins(0, 0, 0, 0)
        self.multiHtml.setObjectName("multiHtml")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 988, 23))
        self.menubar.setObjectName("menubar")
        self.file = QtWidgets.QMenu(self.menubar)
        self.file.setObjectName("file")
        self.edit = QtWidgets.QMenu(self.menubar)
        self.edit.setObjectName("edit")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setIconSize(QtCore.QSize(20, 20))
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.fileOpenAction = QtWidgets.QAction(MainWindow)
        self.fileOpenAction.setObjectName("fileOpenAction")
        self.editFindAction = QtWidgets.QAction(MainWindow)
        self.editFindAction.setObjectName("editFindAction")
        self.fileNewAction = QtWidgets.QAction(MainWindow)
        self.fileNewAction.setObjectName("fileNewAction")
        self.fileCloseAction = QtWidgets.QAction(MainWindow)
        self.fileCloseAction.setObjectName("fileCloseAction")
        self.addWinAction = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/pic/icons/cartoon1.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addWinAction.setIcon(icon1)
        self.addWinAction.setObjectName("addWinAction")
        self.file.addAction(self.fileOpenAction)
        self.file.addAction(self.fileNewAction)
        self.file.addAction(self.fileCloseAction)
        self.edit.addAction(self.editFindAction)
        self.menubar.addAction(self.file.menuAction())
        self.menubar.addAction(self.edit.menuAction())
        self.toolBar.addAction(self.addWinAction)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.file.setTitle(_translate("MainWindow", "文件(&F)"))
        self.edit.setTitle(_translate("MainWindow", "编辑(&E)"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.fileOpenAction.setText(_translate("MainWindow", "打开"))
        self.fileOpenAction.setToolTip(_translate("MainWindow", "打开"))
        self.fileOpenAction.setShortcut(_translate("MainWindow", "Alt+O"))
        self.editFindAction.setText(_translate("MainWindow", "查找"))
        self.editFindAction.setToolTip(_translate("MainWindow", "查找"))
        self.editFindAction.setShortcut(_translate("MainWindow", "Ctrl+F"))
        self.fileNewAction.setText(_translate("MainWindow", "新建"))
        self.fileNewAction.setToolTip(_translate("MainWindow", "新建"))
        self.fileNewAction.setShortcut(_translate("MainWindow", "Alt+N"))
        self.fileCloseAction.setText(_translate("MainWindow", "关闭"))
        self.fileCloseAction.setToolTip(_translate("MainWindow", "关闭"))
        self.fileCloseAction.setShortcut(_translate("MainWindow", "Alt+C"))
        self.addWinAction.setText(_translate("MainWindow", "添加窗体"))
        self.addWinAction.setIconText(_translate("MainWindow", "添加窗体"))
        self.addWinAction.setToolTip(_translate("MainWindow", "添加窗体"))

import apprcc_rc
