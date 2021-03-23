# -*- coding:utf-8 -*-
import sys

from PyQt5.QtCore import Qt, QRectF, QPointF, QPoint, QSize, pyqtSignal
from PyQt5.QtGui import QPaintEvent, QPainter, QPainterPath, QPen, QColor, QResizeEvent, QPixmap, QBrush, QFont
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QGridLayout, QVBoxLayout, QPushButton


class MyWidget(QWidget):
    def __init__(self, parent=None, *args):
        super().__init__(parent, *args)
        layout = QVBoxLayout(self)

        self.aaa = Aaa(self)
        layout.addWidget(self.aaa)

        self.disconnect_signal_btn = QPushButton(self)
        self.disconnect_signal_btn.setText("断开Aaa实例的click连接")
        layout.addWidget(self.disconnect_signal_btn)

        self.aaa.btn.clicked.connect(self.aaa_btn_clicked_handler)

        self.disconnect_signal_btn.clicked.connect(self.disconnect_signal_btn_clicked_handler)

    def aaa_btn_clicked_handler(self):
        print("aaa")

    def disconnect_signal_btn_clicked_handler(self):
        try:
            self.aaa.btn.clicked.disconnect(self.aaa_btn_clicked_handler)
        except Exception as e:
            print(e)
            print(type(e))


class Aaa(QWidget):

    def __init__(self, parent=None, *args):
        super().__init__(parent, *args)
        layout = QVBoxLayout(self)

        self.btn = QPushButton(self)
        self.btn.setText("Aaa")


class Bbb(QWidget):

    def __init__(self, parent=None, *args):
        super().__init__(parent, *args)
        layout = QVBoxLayout(self)

        self.btn = QPushButton(self)
        self.btn.setText("Bbb")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_widget = MyWidget()
    my_widget.show()
    sys.exit(app.exec_())

