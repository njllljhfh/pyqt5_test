# -*- coding:utf-8 -*-
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QMainWindow, QFileDialog

from ui.main_window_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # 菜单的点击事件，当点击关闭菜单时连接槽函数 close()
        self.fileCloseAction.triggered.connect(self.close)

        # 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()
        self.fileOpenAction.triggered.connect(self.openMsg)

        self.addWinAction.triggered.connect(self.addWebWin)

    def openMsg(self):
        file, ok = QFileDialog.getOpenFileName(self, "打开", "C:/", "All Files (*);;Text Files (*.txt)")
        print(f"file={file}, ok={ok}")
        # 在状态栏显示文件地址
        self.statusbar.showMessage(file)

    def addWebWin(self):
        view = QWebEngineView()
        view.load(QUrl('http://www.baidu.com'))
        self.multiHtml.addWidget(view)
        view.show()
