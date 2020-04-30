# -*- coding:utf-8 -*-
import sys

from PyQt5.QtCore import pyqtSlot, QObject, QFileInfo
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5 import QtQml
import os

from PyQt5.QtQml import qmlRegisterType
import logging


class Dealer(QObject):
    @pyqtSlot(str, result=bool)
    def isDir(self, url):
        # fileInfo = QFileInfo(url)
        # return fileInfo.isDir()
        pass


if __name__ == '__main__':
    filePath = 'a.qml'
    # fileName = 'a.qml'
    # filePath = os.path.join(sys.path[0], fileName)
    app = QGuiApplication([])
    # QGuiApplication.setWindowIcon(QIcon("../icons/cartoon1.ico"))
    app.setWindowIcon(QIcon("../icons/cartoon1.ico"))

    qmlRegisterType(Dealer, "a.qt.Dealer", 1, 3, "Dealer")  # 将Dealer注册到Qt

    engine = QtQml.QQmlApplicationEngine()
    engine.load(filePath)
    app.exec_()
