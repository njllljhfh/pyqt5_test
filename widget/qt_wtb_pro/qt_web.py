# -*- coding:utf-8 -*-

import sys
from threading import Timer
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import pyqtSlot, Qt, QUrl, QFileInfo
from PyQt5.QtCore import pyqtProperty, pyqtSignal

source = "https://blog.csdn.net/qianshuyuankk/article/details/103960985"


class MyShared(QWidget):

    def __init__(self):
        super().__init__()

    def PyQt52WebValue(self):
        return "666"

    def Web2PyQt5Value(self, str):
        QMessageBox.information(self, "网页来的信息", str)

    value = pyqtProperty(str, fget=PyQt52WebValue, fset=Web2PyQt5Value)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Javascript call PyQt5')
        self.setGeometry(5, 30, 1355, 730)
        self.browser = QWebEngineView()
        # 加载外部的web界面
        url = QUrl(QFileInfo("./web_file1.html").absoluteFilePath())
        self.browser.load(url)
        self.setCentralWidget(self.browser)

    def calljs(self):
        # jscode = "PyQt52WebValue('你好web');"
        d = {"xxx":"97"}
        jscode = f'PyQt52WebValue({d});'
        # jscode = "PyQt52WebValue();"
        self.browser.page().runJavaScript(jscode)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    channel = QWebChannel()
    shared = MyShared()
    # channel.registerObject("con", shared)
    channel.registerObjects({
        "con": shared
    })
    win.browser.page().setWebChannel(channel)
    t = Timer(5, win.calljs)
    t.start()

    win.show()
    sys.exit(app.exec_())
