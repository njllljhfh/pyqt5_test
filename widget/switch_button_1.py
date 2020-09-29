# -*- coding:utf-8 -*-
import sys

from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QTimer, QSize
from PyQt5.QtGui import QColor, QPaintEvent, QPainter, QPainterPath, QMouseEvent, QResizeEvent, QBrush
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication

import logging

logger = logging.Logger(__name__)


class SwitchControl(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.m_nHeight = 16  # 高度
        self.m_bChecked = False  # 是否选中
        self.m_radius = 8.0  # 圆角
        self.m_nMargin = 3  # 外边距
        self.m_checkedColor = QColor(0, 150, 136)  # 选中颜色
        self.m_thumbColor = QColor(255, 255, 255)  # 拇指颜色
        self.m_disabledColor = QColor(190, 190, 190)  # 不可用颜色
        self.m_background = QColor(0, 0, 0)  # 背景颜色
        self.setCursor(Qt.PointingHandCursor)
        # - -
        self.m_nX = 0  # x点坐标
        self.m_nY = 0  # y点坐标

        self.m_timer = QTimer()  # 定时器

        # - - -
        self.m_timer.timeout.connect(self.onTimeout)

    # 绘制开关
    def paintEvent(self, event: QPaintEvent):
        try:

            painter = QPainter(self)
            painter.setPen(Qt.NoPen)
            painter.setRenderHint(QPainter.Antialiasing)

            painter.begin(self)

            path = QPainterPath()
            # background :QColor
            # thumbColor:QColor
            # dOpacity:float
            if self.isEnabled():  # 可用状态
                if self.m_bChecked:  # 打开状态
                    background = self.m_checkedColor
                    thumbColor = self.m_checkedColor
                    dOpacity = 0.600
                else:  # 关闭状态
                    background = self.m_background
                    thumbColor = self.m_thumbColor
                    dOpacity = 0.800
            else:  # 不可用状态
                background = self.m_background
                dOpacity = 0.260
                thumbColor = self.m_disabledColor

            # 绘制大椭圆
            print(f"background = {background}")
            print(f"type(background) = {type(background)}")
            # brush = QBrush(background, Qt.SolidPattern)

            brush = QBrush(background)
            # painter.setBrush(background)
            painter.setBrush(brush)
            painter.setOpacity(dOpacity)
            path.addRoundedRect(QRectF(0,
                                       0,
                                       self.width(),
                                       self.height()),
                                self.height() / 2,
                                self.height() / 2)
            painter.drawPath(path.simplified())

            # 绘制小椭圆
            painter.setBrush(thumbColor)
            painter.setOpacity(1.0)
            painter.drawEllipse(QRectF(self.m_nX + self.height() / 2,
                                       self.m_nY + self.height() / 2,
                                       self.height(),
                                       self.height())
                                )
            painter.end()
        except Exception as e:
            logger.error(f"error:{e}", exc_info=True)

    # 鼠标按下事件
    def mousePressEvent(self, event: QMouseEvent):
        try:
            if self.isEnabled():
                if event.buttons() == Qt.LeftButton:
                    event.accept()
                else:
                    event.ignore()
        except Exception as e:
            print(e)

    # 鼠标释放事件 - 切换开关状态、发射toggled()信号
    def mouseReleaseEvent(self, event: QMouseEvent):
        try:
            if self.isEnabled():
                if (event.type() == QMouseEvent.MouseButtonRelease) and (event.button() == Qt.LeftButton):
                    event.accept()
                    self.m_bChecked = not self.m_bChecked
                    self.toggled.emit(self.m_bChecked)
                    self.m_timer.start(1)
                else:
                    event.ignore()
        except Exception as e:
            print(e)

    # 大小改变事件
    def resizeEvent(self, event: QResizeEvent):

        self.m_nX = self.m_nHeight / 2
        self.m_nY = self.m_nHeight / 2
        super().resizeEvent(event)

    # 默认大小
    def sizeHint(self):
        return self.minimumSizeHint()

    # 最小大小
    def minimumSizeHint(self):
        return QSize(2 * (self.m_nHeight + self.m_nMargin), self.m_nHeight + 2 * self.m_nMargin)

    # 切换状态 - 滑动
    def onTimeout(self):
        try:
            if self.m_bChecked:
                self.m_nX += 1
                if self.m_nX >= self.width() - self.m_nHeight / 2:
                    self.m_timer.stop()
            else:
                self.m_nX -= 1
                if self.m_nX <= self.m_nHeight / 2:
                    self.m_timer.stop()
            self.update()
        except Exception as e:
            print(e)

    # 返回开关状态 - 打开：true 关闭：false
    def isToggled(self):

        return self.m_bChecked

    # 设置开关状态
    def setToggle(self, checked):
        self.m_bChecked = checked
        self.m_timer.start(10)

    # 设置背景颜色
    def setBackgroundColor(self, color: QColor):
        self.m_background = color

    # 设置选中颜色
    def setCheckedColor(self, color: QColor):
        self.m_checkedColor = color

    # 设置不可用颜色
    def setDisbaledColor(self, color: QColor):
        self.m_disabledColor = color


# 自定义的QWidget例子
class ExampleWidget(QWidget):
    """例子"""

    def __init__(self, parent=None, *args):
        super().__init__(parent, *args)
        try:
            layout = QVBoxLayout(self)

            self.switch_btn = SwitchControl(parent=self)
            # self.switch_btn.setFixedSize(100, 20)
            layout.addWidget(self.switch_btn)
        except Exception as e:
            print(e)

    def init_data(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_widget = ExampleWidget()
    my_widget.init_data()
    my_widget.show()
    sys.exit(app.exec_())
