# -*- coding:utf-8 -*-
import sys
import logging
import time
from pprint import pprint

from PyQt5.QtCore import QRectF, QPoint, QSize, Qt, pyqtSignal, pyqtSlot, QPointF

# QtCore.Signal()
from qtpy import QtWidgets

logger = logging.getLogger(__name__)

from PyQt5 import QtGui
from PyQt5.QtGui import QPaintEvent, QPixmap, QResizeEvent, QPainterPath, QCursor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QApplication, QSizePolicy, QMessageBox, \
    QCheckBox

QSS = """
ImageCanvas {
    color: rgb(255, 255, 255);
    background-color: rgb(20, 20, 20);
}
"""


class MainWidget(QWidget):
    """主界面"""

    def __init__(self, *args, parent=None):
        super().__init__(parent, *args)
        """GUI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label_layer_control_panel = LabelLayerControlPanel()
        self.label_layer_control_panel.setFixedHeight(30)
        layout.addWidget(self.label_layer_control_panel)

        self.el_img_canvas = ImageCanvas()
        layout.addWidget(self.el_img_canvas)

        """根据当前状态显示图层"""
        self.bbox_checkbox_state_changed_event()
        self.mask_checkbox_state_changed_event()

        self.binding_event_and_signal()

    def binding_event_and_signal(self):
        self.label_layer_control_panel.bbox_checkbox.stateChanged.connect(self.bbox_checkbox_state_changed_event)
        self.label_layer_control_panel.mask_checkbox.stateChanged.connect(self.mask_checkbox_state_changed_event)

    def bbox_checkbox_state_changed_event(self):
        """"""
        if self.label_layer_control_panel.bbox_checkbox.isChecked():
            self.el_img_canvas.bbox_label_layer.show()
        else:
            self.el_img_canvas.bbox_label_layer.hide()

    def mask_checkbox_state_changed_event(self):
        """"""
        if self.label_layer_control_panel.mask_checkbox.isChecked():
            self.el_img_canvas.mask_label_layer.show()
        else:
            self.el_img_canvas.mask_label_layer.hide()


class LabelLayerControlPanel(QWidget):
    """图层显示控制面板"""

    def __init__(self, *args, parent=None):
        super().__init__(parent, *args)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        # layout.setSpacing(100)
        self.bbox_checkbox = QCheckBox(self)
        self.bbox_checkbox.setObjectName("bbox_checkbox")
        self.bbox_checkbox.setText("正框")
        layout.addWidget(self.bbox_checkbox)
        layout.setAlignment(self.bbox_checkbox, Qt.AlignHCenter)

        self.mask_checkbox = QCheckBox(self)
        self.mask_checkbox.setObjectName("mask_checkbox")
        self.mask_checkbox.setText("分割")
        layout.addWidget(self.mask_checkbox)
        layout.setAlignment(self.mask_checkbox, Qt.AlignHCenter)


class ImageCanvas(QWidget):
    """画布-用于加载图片"""
    # 图像缩放比变化
    change_img_ratio_signal = pyqtSignal(float)

    def __init__(self, *args):
        super().__init__(*args)
        """GUI"""
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setMinimumSize(500, 350)
        self.setStyleSheet(QSS)

        # 正框标注图层
        self.bbox_label_layer = BBoxLabelLayer(parent=self)
        self.bbox_label_layer.setObjectName("bbox_label_layer")
        layout.addWidget(self.bbox_label_layer, 0, 0, 1, 1)
        # self.bbox_label_layer.show()

        # 分割标注图层
        self.mask_label_layer = MaskLabelLayer(parent=self)
        self.mask_label_layer.setObjectName("mask_label_layer")
        # self.mask_label_layer.setMinimumSize(300, 300)
        layout.addWidget(self.mask_label_layer, 0, 0, 1, 1)
        # self.mask_label_layer.show()
        # self.mask_label_layer.hide()

        # self.magnifying_glass = MagnifyingGlass(parent=self)

        """属性"""
        self.scale_w = 1
        self.scale_h = 1
        self._painter = QtGui.QPainter()
        self.original_pix = QPixmap()
        self.current_pix = None
        self.mouse_x = 0
        self.mouse_y = 0

        """绑定事件/信号"""
        self.binding_event_and_signal()

        self.init_data()

    def init_data(self):
        with open("../images/EL_TP3.jpg", "rb") as f:
            image_bytes = f.read()
        self.load_image(image_bytes=image_bytes)

    def binding_event_and_signal(self):
        self.change_img_ratio_signal.connect(self.bbox_label_layer.set_ratio)
        self.change_img_ratio_signal.connect(self.mask_label_layer.set_ratio)

        self.bbox_label_layer.update_current_mouse_position_signal.connect(self.mask_label_layer.set_mouse_position)

        self.mask_label_layer.update_current_mouse_position_signal.connect(self.bbox_label_layer.set_mouse_position)

    def load_image(self, image_bytes=None):
        """ 加载背景图的方法 """
        try:
            if image_bytes:
                # logger.info(f"加载背景图")
                self.original_pix.loadFromData(image_bytes)
                # self.origin_pixmap=self.pixmap.copy()

            img_w, img_h = self.original_pix.width(), self.original_pix.height()
            # logger.info(f"该阶段原图像的:w_h = {img_w, img_h}")
            if not self.original_pix.isNull():
                ratio = self.calculate_scale_ratio(img_w, img_h)
                self.change_img_ratio_signal.emit(ratio)
                new_w_h = int(img_w * ratio), int(img_h * ratio)
                # logger.info(f"new_w_h={new_w_h}")

                scaled_pixmap = self.original_pix.scaled(QSize(*new_w_h), Qt.IgnoreAspectRatio, Qt.FastTransformation)
                self.load_pix(scaled_pixmap)

                # 发信号，调整标尺大小（参数：图像的新宽高）
                # self.reload_image_signal.emit(*new_w_h)
        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            message_box = QMessageBox(self)
            message_box.warning(self, "警告", str(e), QMessageBox.Yes, QMessageBox.Yes)

    def load_pix(self, pix):
        """设置缩放后的图像pix"""
        self.current_pix = pix  # 有图像的时候才绘制网格
        # self.repaint()
        # self.update()

    def calculate_scale_ratio(self, img_w, img_h):
        """
        计算缩放比例
        :param img_w: 原始图像宽
        :param img_h: 原始图像高
        :return:
        """
        try:
            win_w, win_h = self.width(), self.height()
            radio_x = win_w / img_w
            radio_y = win_h / img_h
            radio = radio_x if radio_x < radio_y else radio_y
            return radio
        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            message_box = QMessageBox(self)
            message_box.warning(self, "警告", str(e), QMessageBox.Yes, QMessageBox.Yes)

    def paintEvent(self, event: QPaintEvent):
        """在画布上画图像，检测结果"""
        if not self.current_pix:
            return super().paintEvent(event)

        try:
            self._painter.begin(self)
            self._painter.setRenderHint(QtGui.QPainter.Antialiasing)
            self._painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
            self._painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
            self._painter.scale(self.scale_w, self.scale_h)  # (1.0, 1.0)
            # 绘制图片
            self._painter.translate(QPoint(0, 0))  # 设置原点位置(0, 0)
            self._painter.drawPixmap(0, 0, self.current_pix)  # 绘制图形的区域
            self._painter.end()
        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            message_box = QMessageBox(self)
            message_box.warning(self, "警告", str(e), QMessageBox.Yes, QMessageBox.Yes)

    def resizeEvent(self, event: QResizeEvent):
        """ 改变大小事件 """
        super().resizeEvent(event)
        try:
            self.load_image()
        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            message_box = QMessageBox(self)
            message_box.warning(self, "警告", str(e), QMessageBox.Yes, QMessageBox.Yes)

    def mouseMoveEvent(self, ev):
        # super().mouseMoveEvent(ev)
        try:
            pos = ev.pos()
            self.mouse_x = pos.x()
            self.mouse_y = pos.y()
            # logger.info(f"{self.objectName()}---mouse_x_y = {(self.mouse_x,self.mouse_y)}")
        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            message_box = QMessageBox(self)
            message_box.warning(self, "警告", str(e), QMessageBox.Yes, QMessageBox.Yes)


class BaseLabelLayer(QWidget):
    """标注图层-基类"""

    # 鼠标位置变化
    update_current_mouse_position_signal = pyqtSignal(int, int)

    def __init__(self, *args, parent=None):
        super().__init__(parent, *args)
        self.setMouseTracking(True)
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.scale_w = 1
        self.scale_h = 1
        self._painter = QtGui.QPainter()
        self._ratio = 1  # 窗口变化时，图像缩放比例
        self.mouse_x = 0
        self.mouse_y = 0

        self.shape_original_data = [[1500, 1500, 100, 100]]

    @pyqtSlot(float)
    def set_ratio(self, ratio):
        """设置缩放比"""
        # logger.info(f"set_ratio----{self.objectName()}")
        self._ratio = ratio

    def paintEvent(self, event: QPaintEvent):
        """在图层上画标注，检测结果"""

        try:
            self._painter.begin(self)
            self._painter.setRenderHint(QtGui.QPainter.Antialiasing)
            self._painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
            self._painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
            self._painter.scale(self.scale_w, self.scale_h)  # (1.0, 1.0)
            self._painter.translate(QPoint(0, 0))  # 设置原点位置(0, 0)

            # 绘制标注数据
            self.draw_shapes()

            # TODO: 放大镜
            # if self._show_magnifying_glass and (not self.magnifying_glass_pix.isNull()):
            #     start_x = self.mouse_position_x - (self.zoom_width * self.zoom_ratio / 2)
            #     start_y = self.mouse_position_y - (self.zoom_height * self.zoom_ratio / 2)
            #
            #     # 图像宽、高 减去 放大镜宽、高
            #     max_x = self.original_pix.width() - (self.zoom_width * self.zoom_ratio)
            #     max_y = self.original_pix.height() - (self.zoom_height * self.zoom_ratio)
            #
            #     if start_x < 0:
            #         start_x = 0
            #     elif start_x > max_x:
            #         start_x = max_x
            #     if start_y < 0:
            #         start_y = 0
            #     elif start_y > max_y:
            #         start_y = max_y
            #
            #     logger.info(f"self.magnifying_glass_pix.width() = {self.magnifying_glass_pix.width() }")
            #     logger.info(f"self.magnifying_glass_pix.height() = {self.magnifying_glass_pix.height() }")
            #     logger.info(f"放大镜【鼠标中心位置】:x={self.mouse_position_x}, y={self.mouse_position_y}")
            #     logger.info(f"放大镜【左上角顶点位置】:x={start_x}, y={start_y}")
            #     p.drawPixmap(start_x, start_y, self.magnifying_glass_pix)
            pass
            self._painter.end()
        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            message_box = QMessageBox(self)
            message_box.warning(self, "警告", str(e), QMessageBox.Yes, QMessageBox.Yes)

    def draw_shapes(self):
        """绘制标注"""
        pass

    def mouseMoveEvent(self, ev):
        # super().mouseMoveEvent(ev)
        try:
            pos = ev.pos()
            self.mouse_x = pos.x()
            self.mouse_y = pos.y()
            self.update_current_mouse_position_signal.emit(self.mouse_x, self.mouse_y)
            # logger.info(f"{self.objectName()}---mouse_x_y = {(self.mouse_x,self.mouse_y)}")
        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            message_box = QMessageBox(self)
            message_box.warning(self, "警告", str(e), QMessageBox.Yes, QMessageBox.Yes)

    @pyqtSlot(int, int)
    def set_mouse_position(self, x, y):
        """设置鼠标位置"""
        self.mouse_x = x
        self.mouse_y = y
        self.update()


class BBoxLabelLayer(BaseLabelLayer):
    """正框标注图层"""

    def __init__(self, *args, parent=None):
        super().__init__(*args, parent=parent)
        self.shape_original_data = [[1500, 1500, 50, 50]]

    def draw_shapes(self):
        """绘制标注"""
        pen = QtGui.QPen()
        for rect in self.shape_original_data:
            x = rect[0] * self._ratio
            y = rect[1] * self._ratio
            w = rect[2] * self._ratio
            h = rect[3] * self._ratio

            rect_f = QRectF(x, y, w, h)
            if rect_f.contains(QPointF(self.mouse_x, self.mouse_y)):
                pen.setWidth(1)
            else:
                pen.setWidth(2)

            pen.setColor(QtGui.QColor(0, 0, 255))
            self._painter.setPen(pen)
            self._painter.drawRect(rect_f)


class MaskLabelLayer(BaseLabelLayer):
    """斜框标注图层"""

    def __init__(self, *args, parent=None):
        super().__init__(*args, parent=parent)
        self.shape_original_data = [[[1600, 1600], [1400, 1700], [1500, 1800], [1700, 1800], [1800, 1700]], ]

    def draw_shapes(self):
        """绘制路径"""

        # logger.info(f"{self.objectName()}---draw_shapes")
        try:
            pen = QtGui.QPen()
            pen.setColor(QtGui.QColor(0, 255, 0))

            # my_grandient = QLinearGradient() # 填充色
            # p.setBrush(my_grandient)

            for path_points in self.shape_original_data:
                path = QPainterPath()
                for i, point in enumerate(path_points):
                    # point是list
                    x = point[0]
                    y = point[1]
                    if i == 0:
                        path.moveTo(x * self._ratio, y * self._ratio)
                    else:
                        path.lineTo(x * self._ratio, y * self._ratio)
                path.closeSubpath()

                logger.info(f"{self.objectName()}---鼠标位置{(self.mouse_x, self.mouse_y)}")
                logger.info(f"判断鼠标当前位置是否在路径内={path.contains(QPointF(self.mouse_x, self.mouse_x))}")
                logger.info(f"-----------------------------------------------------------")
                # 判断鼠标当前位置是否在路径内
                if path.contains(QPointF(self.mouse_x, self.mouse_y)):
                    pen.setWidth(1)
                else:
                    pen.setWidth(2)
                self._painter.setPen(pen)
                self._painter.drawPath(path)
        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            message_box = QMessageBox(self)
            message_box.warning(self, "警告", str(e), QMessageBox.Yes, QMessageBox.Yes)


class MagnifyingGlass(QWidget):
    """放大镜"""

    def __init__(self, *args, parent=None):
        super().__init__(parent, *args)


if __name__ == '__main__':
    sys.path.append("..")
    from log_config import settings

    app = QApplication(sys.argv)
    # win = ImageCanvas()
    win = MainWidget()
    win.show()
    # time.sleep(2)
    # win.setCursor(QCursor(Qt.BusyCursor))
    QtWidgets.QApplication.setOverrideCursor(Qt.BusyCursor)
    # time.sleep(2)
    # win.unsetCursor()
    # pprint(win.cursor())

    sys.exit(app.exec_())
