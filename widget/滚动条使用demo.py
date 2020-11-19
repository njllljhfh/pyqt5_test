# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self, ):
        super(QMainWindow, self).__init__()
        self.number = 0

        w = QWidget()
        self.setCentralWidget(w)

        self.topFiller = QWidget()
        self.topFiller.setMinimumSize(250, 2000)  #######设置滚动条的尺寸
        for filename in range(20):
            MapButton = QPushButton(self.topFiller)
            MapButton.setText(str(filename))
            MapButton.move(10, filename * 40)

        ##创建一个滚动条
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.topFiller)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.scroll)
        w.setLayout(self.vbox)

        self.statusBar().showMessage("底部信息栏")
        # self.resize(300, 500)
        # self.scroll.verticalScrollBar().hide()
        print(self.scroll.horizontalScrollBar().height())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())
