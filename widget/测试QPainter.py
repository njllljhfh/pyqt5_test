# -*- coding:utf-8 -*-
import logging
import log_config.settings
import sys

from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, QPointF, QRectF
from PyQt5.QtGui import QPixmap, QPaintEvent, QPainter, QPainterPath
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication

logger = logging.getLogger(__name__)


class Xxx(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setMinimumSize(1000, 600)

        self.pix = QPixmap()
        with open('../images/EL_TP3.jpg', 'rb') as f:
            el_image_bytes = f.read()

        self.pix.loadFromData(el_image_bytes)
        logger.info(f"pix_wh = {self.pix.width(),self.pix.height()}")

        x_wh = (66, 88)
        yyy = self.pix.scaled(*x_wh)
        logger.info(f"pix_wh = {self.pix.width(),self.pix.height()}")
        logger.info(f"yyy_wh = {yyy.width(),yyy.height()}")

    def paintEvent(self, event: QPaintEvent):

        try:
            logger.info(f"paintEvent")
            super().paintEvent(event)

            p = QPainter()
            p.begin(self)
            # 以（100,100）点为坐标原点原点，图像画上去。
            p.translate(QPoint(100, 100))  # 设置原点位置
            p.drawPixmap(0, 0, self.pix)  # 相对于原点位置，画图像
            a = QPointF(2, 5)
            b = QPointF(3, 15)
            c = (a + b) / 2
            logger.info(f"c = {c.x(),c.y()}")

            # 用给定的画笔画路径
            pen = QtGui.QPen(QtGui.QColor(255, 0, 0, 128))
            p.setPen(pen)
            polygonPath = QPainterPath()
            polygonPath.moveTo(10.0, 80.0)
            polygonPath.lineTo(20.0, 10.0)
            polygonPath.lineTo(80.0, 30.0)
            polygonPath.lineTo(90.0, 70.0)
            polygonPath.closeSubpath()
            p.drawPath(polygonPath)
            # -
            pen = QtGui.QPen(QtGui.QColor(0, 255, 0, 128))

            # my_grandient = QLinearGradient() # 填充色
            # p.setBrush(my_grandient)
            p.setPen(pen)
            groupPath = QPainterPath()
            groupPath.moveTo(60.0, 40.0)
            groupPath.arcTo(20.0, 20.0, 40.0, 40.0, 0.0, 360.0)
            groupPath.moveTo(40.0, 40.0)
            groupPath.lineTo(40.0, 80.0)
            groupPath.lineTo(80.0, 80.0)
            groupPath.lineTo(80.0, 40.0)
            groupPath.closeSubpath()
            p.drawPath(groupPath)
            # 画矩形
            rect = QRectF(200, 100, 150, 50)
            p.drawRect(rect)
            # -
            rect1 = QRectF(200, 200, 50, 50)
            rect2 = QRectF(300, 200, 50, 50)
            p.drawRects([rect1, rect2])
            # -
            p.end()
        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            qMessageBox = QMessageBox(self)
            qMessageBox.warning(self, "警告", str(e), QMessageBox.Yes, QMessageBox.Yes)


if __name__ == '__main__':
    sys.path.append("..")

    # print(Xxx.mro())
    a = [
        {"x": 8},
        {"x": 1},
        {"x": 3},
        {"x": 5},
    ]
    print(a)
    a.sort(key=lambda data: data["x"])
    print(a)

    app = QApplication(sys.argv)
    myWin = Xxx()
    myWin.show()
    sys.exit(app.exec_())
