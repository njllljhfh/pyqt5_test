# -*- coding:utf-8 -*-
import math
import sys
import threading

from PyQt5.QtCore import Qt, QRectF, QPointF, QPoint, QSize, QLineF, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPaintEvent, QPainter, QPainterPath, QPen, QColor, QResizeEvent, QPixmap, QBrush, QFont
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QPushButton

import logging

# FORMAT = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
FORMAT = '%(asctime)s - [line:%(lineno)d] - %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)

TIMES=0

class Canvas(QWidget):
    def __init__(self, *args, parent=None, file_path=None):
        super().__init__(parent, *args)
        # self.setMinimumSize(1000, 600)

        self.original_pix = QPixmap()
        if file_path is None:
            file_path = '../images/EL_TP3.jpg'
        with open(file_path, 'rb') as f:
            el_image_bytes = f.read()

        self.original_pix.loadFromData(el_image_bytes)
        self.current_pix = QPixmap()

    def paintEvent(self, event: QPaintEvent):

        try:
            super().paintEvent(event)

            p = QPainter()
            p.begin(self)
            # 以（100,100）点为坐标原点原点，图像画上去。
            p.translate(QPoint(0, 0))  # 设置原点位置
            p.drawPixmap(0, 0, self.current_pix)  # 相对于原点位置，画图像

            # 用给定的画笔画路径
            pen = QPen(QColor(255, 0, 0, 128))
            p.setPen(pen)
            polygonPath = QPainterPath()
            polygonPath.moveTo(10.0, 80.0)
            polygonPath.lineTo(20.0, 10.0)
            polygonPath.lineTo(80.0, 30.0)
            polygonPath.lineTo(90.0, 70.0)
            polygonPath.closeSubpath()
            p.drawPath(polygonPath)
            # -
            pen = QPen(QColor(0, 255, 0, 128))

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
            logger.debug(f"canvas ==== paintEvent === {id(self)}")
        except Exception as e:
            logger.error(f"e: {e}", exc_info=True)
            raise

    def resizeEvent(self, event: QResizeEvent):
        """ 改变大小事件 """
        super().resizeEvent(event)
        try:
            logger.debug(f"Canvas----resizeEvent----{id(self)}")
            self.load_image()
        except Exception as e:
            logger.error(f"e: {e}", exc_info=True)
            raise

    def load_image(self, image_bytes=None):
        """ 加载背景图的方法 """
        try:
            if image_bytes:
                # logger.info(f"加载背景图")
                self.original_pix.loadFromData(image_bytes)
                # self.origin_pixmap=self.pixmap.copy()

            # logger.info(f"该阶段原图像的:w_h = {img_w, img_h}")
            logger.debug(f"self.original_pix.isNull()= {self.original_pix.isNull()}")
            if not self.original_pix.isNull():
                img_w, img_h = self.original_pix.width(), self.original_pix.height()
                # ratio = self.calculate_scale_ratio(img_w, img_h)
                ratio = self.calculate_scale_ratio()
                # self.change_img_ratio_signal.emit(ratio)
                new_w_h = int(img_w * ratio), int(img_h * ratio)
                # logger.info(f"new_w_h={new_w_h}")

                scaled_pixmap = self.original_pix.scaled(QSize(*new_w_h), Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.load_pix(scaled_pixmap)

                # 发信号，调整标尺大小（参数：图像的新宽高）
                # self.reload_image_signal.emit(*new_w_h)
        except Exception as e:
            logger.error(f"e: {e}", exc_info=True)
            raise

    def calculate_scale_ratio(self):
        """计算缩放比例"""
        try:
            win_w, win_h = self.width(), self.height()
            radio_x = win_w / self.original_pix.width()
            radio_y = win_h / self.original_pix.height()
            radio = radio_x if radio_x < radio_y else radio_y
            return radio
        except Exception as e:
            logger.error(f"e: {e}", exc_info=True)
            raise

    def load_pix(self, pix):
        """设置缩放后的图像pix"""
        logger.debug(f"load_pix")
        self.current_pix = pix  # 有图像的时候才绘制网格
        self.repaint()
        self.update()


class Stack(QWidget):
    """模拟放带标尺的canvas的stack"""

    def __init__(self, *args, parent=None):
        super().__init__(parent, *args)

        # layout = QVBoxLayout(self)
        # layout.setContentsMargins(0, 0, 0, 0)
        # layout.setSpacing(0)

        # self.my_widget = MyWidget(self)
        # self.my_widget.init_data()
        # layout.addWidget(self.my_widget)
        #
        # self.qss = """
        # Stack {
        #     background-color: rgb(0, 0, 0);
        # }
        # """
        # self.setStyleSheet(self.qss)
        self.btn = QPushButton(self)
        self.btn.setText("加载图像")
        self.btn.setFixedSize(100, 30)
        self.btn.setGeometry(0, 0, self.btn.width(), self.btn.height())

        self.container = QWidget(self)
        self.layout_container = QHBoxLayout(self.container)

        self.canvas = Canvas()
        self.layout_container.addWidget(self.canvas)
        self.container.setGeometry(0, self.btn.height(), 300, 300)

        # self.load_img_th = LoadImgThread(parent=self)
        # self.load_img_th.update_image_signal.connect(self.update_canvas)
        # self.load_img_th.err_signal.connect(self.thread_err_handler)

        self.btn.clicked.connect(self.load_image)

        self.resize(800, 600)

    @pyqtSlot(Exception)
    def thread_err_handler(self, e):
        logger.error(f"e = {e}")

    def load_image(self):
        try:
            self.load_img_th = LoadImgThread(parent=self)
            self.load_img_th.update_image_signal.connect(self.update_canvas)
            self.load_img_th.err_signal.connect(self.thread_err_handler)
            self.load_img_th.start()
        except Exception as e:
            logger.error(f"e: {e}", exc_info=True)

    @pyqtSlot(dict)
    def update_canvas(self, data):
        try:
            print(f"id111==={id(self.canvas)}")
            # a = self.canvas
            self.layout_container.removeWidget(self.canvas)
            # xxx = self.layout_container.itemAt(0).widget()
            # print(f"xxx = {xxx}")
            # self.canvas.deleteLater()

            self.canvas: Canvas = data.get("canvas")
            print(f"id222==={id(self.canvas)}")
            # self.canvas.show()
            # canvas.setParent(self.container)
            self.layout_container.addWidget(self.canvas)
            # a.deleteLater()
            # del_th=DeleteThread(th=self.load_img_th)
            # del_th.start()
            print(f" - - - - ")

            # self.layout_container.removeWidget(self.canvas)
            # self.canvas.deleteLater()
            # self.canvas = Canvas(file_path='../images/VI_TP3.jpg')
            # print(f"2 update_canvas = {self.canvas}")
            # self.layout_container.addWidget(self.canvas)

        except Exception as e:
            logger.error(f"e: {e}", exc_info=True)

    # def resizeEvent(self, e: QResizeEvent) -> None:


class LoadImgThread(QThread):
    """"""
    update_image_signal = pyqtSignal(dict)
    err_signal = pyqtSignal(Exception)

    def __init__(self, parent=None):
        """
        :param parent:
        """
        super().__init__(parent=parent)
        self.parent = parent
        global TIMES
        if TIMES %2 ==0:
            self.canvas = Canvas(file_path='../images/VI_TP3.jpg')
        else:
            self.canvas = Canvas(file_path='../images/EL_TP3.jpg')
        TIMES+=1

    def run(self):
        try:
            self.update_image_signal.emit({"canvas": self.canvas})
        except Exception as e:
            logger.error(f"e: {e}", exc_info=True)
            self.err_signal.emit(e)


class DeleteThread(QThread):
    """"""
    def __init__(self, parent=None,th:QThread=None):
        """
        :param parent:
        """
        super().__init__(parent=parent)
        self.th=th

    def run(self):
        self.th.quit()
        self.th.wait()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # my_widget = Canvas()
    my_widget = Stack()

    my_widget.show()
    sys.exit(app.exec_())
