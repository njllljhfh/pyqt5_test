# -*- coding:utf-8 -*-
import sys

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QResizeEvent, QMovie, QPaintEvent, QPainter, QColor, QBrush, QPen
from PyQt5.QtWidgets import QLabel, QWidget, QApplication, QPushButton, QVBoxLayout


class LoadingWidget(QWidget):
    """ 等待加载的界面 """

    def __init__(self, icon, parent=None):
        """
        :param icon: icons 路径
        """
        super().__init__(parent=parent)
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 设置为透明

        self.icon_waiting = QMovie(icon)
        self.label = QLabel(self)
        self.setStyleSheet("background-color: rgba(0,0,0,0)")
        # self.label.resize(80, 80)
        self.label.setFixedSize(80, 80)
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)
        self.label.setMovie(self.icon_waiting)
        self.close()  # 一开始不要显示

        # 定义属性
        self.is_loading = False  # 是否在加载数据，用于判断状态，限制界面操作

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        label_w = self.label.width()
        label_h = self.label.height()
        w, h = self.width(), self.height()
        self.label.move((w - label_w) / 2, (h - label_h) / 2)
        print(f"LoadingWidget ====  resizeEvent")

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        try:
            # 绘制背景
            pen = QPen()
            pen.setColor(QColor(0, 0, 0, 0))
            brush = QBrush()
            brush.setColor(QColor(0, 0, 255, 0))
            brush.setStyle(Qt.SolidPattern)
            painter.setPen(pen)
            painter.setBrush(brush)
            painter.drawRect(QRectF(0, 0, self.width(), self.height()))
        except Exception as e:
            print(f"e = {e}")
        finally:
            painter.end()

    def start(self):
        print(f"start")
        self.is_loading = True
        self.icon_waiting.start()
        self.show()

    def stop(self):
        self.is_loading = False
        self.icon_waiting.stop()
        self.close()


# 测试代码
class MyWidget(QWidget):

    def __init__(self, *args):
        super().__init__(*args)

        layout = QVBoxLayout(self)
        self.btn = QPushButton(self)
        self.btn.setText("btn")
        layout.addWidget(self.btn)
        self.wd = QWidget(self)
        self.wd.setStyleSheet("background-color: rgba(207,43,255)")
        # self.wd.setStyleSheet("background-color: rgba(75,130,255)")
        layout.addWidget(self.wd)

        self.loading_widget = LoadingWidget("../icons/loading.gif", parent=self.wd)

        self.setStyleSheet("background-color: rgba(180,180,180)")
        self.resize(400, 400)
        self.btn.clicked.connect(self.event_btn_click)

    def event_btn_click(self):
        if self.loading_widget.is_loading:
            self.loading_widget.stop()
        else:
            self.loading_widget.start()

    def resizeEvent(self, event: QResizeEvent):
        """ 调整大小事件 """
        super().resizeEvent(event)
        self.loading_widget.resize(self.wd.size())
        # self.loading_widget.move(self.wd.pos())
        self.loading_widget.move(0, 0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # - - -
    win = MyWidget()
    # - - -
    # win = LoadingWidget("../icons/loading.gif", parent=None)
    # win.start()
    # - - -

    win.show()
    sys.exit(app.exec_())
