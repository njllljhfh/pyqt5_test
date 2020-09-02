# -*- coding:utf-8 -*-
import sys

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QApplication

"""测试信号连接信号"""


class XXX(QWidget):
    sig_1 = pyqtSignal(str, int)
    sig_3 = pyqtSignal(bool)

    def __init__(self, *args, parent=None):
        super().__init__(parent, *args)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.btn = MyButton()
        self.btn.setText("按钮1")
        layout.addWidget(self.btn)
        self.btn.signal_2.connect(self.sig_1)  # 一个信号连接另一个信号
        self.sig_1.connect(self.sig_1_handler)

        self.btn2 = MyButton()
        self.btn2.setText("按钮2")
        layout.addWidget(self.btn2)
        self.btn2.clicked.connect(self.sig_3)  # 一个信号连接另一个信号
        self.sig_3.connect(self.sig_3_handler)

    @pyqtSlot(str, int)
    def sig_1_handler(self, a, b):
        print(f"sig_1_handler: a={a},b={b}")

    @pyqtSlot(bool)
    def sig_3_handler(self, clicked):
        print(f"sig_3_handler: clicked={clicked}")


class MyButton(QPushButton):
    signal_2 = pyqtSignal(str, int)

    def __init__(self, *args, parent=None):
        super().__init__(parent, *args)

        self.clicked.connect(self.clicked_event)

    def clicked_event(self):
        print("发送signal_2")
        self.signal_2.emit("1", 2)


if __name__ == '__main__':
    # sys.path.append("..")
    # from log_config import settings

    app = QApplication(sys.argv)
    win = XXX()
    win.show()
    sys.exit(app.exec_())
