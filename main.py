# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication

from widget.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
