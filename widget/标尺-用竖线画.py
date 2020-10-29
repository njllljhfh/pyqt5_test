# -*- coding:utf-8 -*-
import math
import sys
from PyQt5.QtCore import Qt, QRectF, QPointF, QPoint, QSize, QLineF
from PyQt5.QtGui import QPaintEvent, QPainter, QPainterPath, QPen, QColor, QResizeEvent, QPixmap, QBrush, QFont
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout

import logging

# FORMAT = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
FORMAT = '%(asctime)s - [line:%(lineno)d] - %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ScalePlate(QWidget):
    """标尺"""

    def __init__(self, *args, parent=None):
        super().__init__(parent, *args)
        # 标尺方向（水平，竖直）
        self.direction = Qt.Horizontal

        # 标尺刻度的原始数据（算法报文中给的数据）[[x,y,w,h], ...]
        self.pos_ls_origin = None
        # 实际画在控件上的标尺刻度[[x,y,w,h], ...]
        self.pos_ls_shown = None

        # 标尺的文字列表[str, ...]
        self.font_ls_origin = None
        # 实际显示的标尺的文字列表[str, ...]
        self.font_ls_shown = None

        # 标尺厚度
        self.thickness = 18
        # 图像缩放比例
        self.img_ratio = 1.0

        # 原始标尺刻度个数
        self.scale_num_origin = 3
        # 实际显示的标尺刻度个数
        self.scale_num_shown = self.scale_num_origin
        # 每几个标尺显示为1个刻度
        self.per = 1
        # - - -

        self.background_color = QColor(27, 27, 27)
        self.line_color = QColor(151, 151, 151)
        self.font_color = QColor(255, 255, 255)
        self.font_size = 0.7 * self.thickness

    def set_direction(self, direction=Qt.Horizontal):
        """设置标尺方向"""
        self.direction = direction

    def set_thickness(self, thickness=18):
        """设置标尺厚度"""
        self.thickness = thickness

    def set_background_color(self, color: QColor = QColor(27, 27, 27)):
        """设置背景色"""
        self.background_color = color

    def set_line_color(self, color: QColor = QColor(151, 151, 151)):
        """设置背景色"""
        self.line_color = color

    def set_font_color(self, color: QColor = QColor(255, 255, 255)):
        """设置背景色"""
        self.font_color = color

    def set_font_size(self, size):
        self.font_size = size

    def set_scale_num_origin(self, scale_num_origin=3):
        """设置原始标尺刻度个数"""
        self.scale_num_origin = scale_num_origin  # 原始标尺刻度个数

    def set_per(self, per=1):
        """设置每几个标尺显示为1个刻度"""
        self.per = per  # 每几个标尺显示为1个刻度

    def set_img_ratio(self, ratio):
        """设置图像缩放比例"""
        # TODO(tip):设置图像的缩放比，请在resize之前调用该方法
        self.img_ratio = ratio

    def set_pos_ls_origin(self, pos_ls=None):
        """设置自定义标尺刻度的原始数据"""
        # TODO(tip):如果需要重新设置自定义的标签位置，请在resize之前调用该方法
        self.pos_ls_origin = pos_ls
        self.scale_num_shown = len(self.pos_ls_origin)

    def set_font_ls_origin(self, font_ls=None):
        """设置自定义的标尺文字"""
        # TODO(tip):如果需要重新设置自定义的标签位置，请在resize之前调用该方法
        self.font_ls_origin = font_ls

    def calculate_show_pos(self):
        """计算要显示的标尺的位置"""
        if self.pos_ls_origin is not None:
            self.calculate_custom_scale_pos()
        else:
            # TODO(tip): 根据scale_num_origin，per来计算
            self.calculate_adaptive_scale_pos()

        logger.debug(f"self.pos_ls_shown = {self.pos_ls_shown}")
        self.generate_font_ls_shown()
        logger.debug("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")

    def calculate_custom_scale_pos(self):
        """计算实际显示的标尺刻度pos(用户自定义的pos)"""
        if self.direction == Qt.Horizontal:
            logger.debug(f"============================= 水平标尺 =============================")
            # logger.debug(f"水平：self.img_ratio = {self.img_ratio}")
            self.pos_ls_shown = [
                [
                    pos[0] * self.img_ratio,
                    0,
                    (pos[2]) * self.img_ratio,
                    # self.thickness - 1
                    self.height() - 1
                ]
                for pos in self.pos_ls_origin
            ]
        else:
            logger.debug(f"============================= 竖直标尺 =============================")
            # logger.debug(f"竖直：self.img_ratio = {self.img_ratio}")
            self.pos_ls_shown = [
                [
                    0,
                    pos[1] * self.img_ratio,
                    # self.thickness - 1,
                    self.width() - 1,
                    (pos[3]) * self.img_ratio
                ]
                for pos in self.pos_ls_origin
            ]

    def calculate_adaptive_scale_pos(self):
        """计算实际显示的标尺刻度pos(自适应，不适用自定义的标尺pos)"""
        self.pos_ls_origin = None

        # 单位跨度
        if self.direction == Qt.Horizontal:
            logger.debug(f"============================= 水平标尺 =============================")
        else:
            logger.debug(f"============================= 竖直标尺 =============================")

        res = self.scale_num_origin / self.per
        logger.debug(f"self.scale_num_origin = {self.scale_num_origin}")
        logger.debug(f"self.per = {self.per}")
        logger.debug(f"res = {res}")

        scale_num_shown: int = math.ceil(res)  # 向上取整
        self.scale_num_shown = scale_num_shown
        logger.debug(f"self.scale_num_shown = {self.scale_num_shown}")

        remainder = self.scale_num_origin % self.per  # 余数
        logger.debug(f"remainder = {remainder}")
        if remainder == 0:
            big_factor = 1
            small_factor = 1
        else:
            big_factor = self.per
            small_factor = remainder

        logger.debug(f"big_factor = {big_factor}")
        logger.debug(f"small_factor = {small_factor}")

        # 标尺控件的总长度
        if self.direction == Qt.Horizontal:
            span_total = self.width()
        else:
            span_total = self.height()
        # 单位跨度
        span_unit = span_total / ((scale_num_shown - 1) * big_factor + small_factor)
        # span_unit = round(span_unit,1)
        # 大比例的标尺跨度
        span_big_scale = span_unit * big_factor
        # 小比例的标尺跨度
        span_small_scale = span_unit * small_factor
        # span_small_scale = span_total - (span_big_scale * (scale_num_shown - 1))

        logger.debug(f"span_unit = {span_unit}")
        logger.debug(f"span_big_scale = {span_big_scale}")
        logger.debug(f"span_small_scale = {span_small_scale}")

        # thickness = self.thickness - 1
        if self.direction == Qt.Horizontal:
            thickness = self.height() - 1
        else:
            thickness = self.width() - 1
        if self.direction == Qt.Horizontal:
            self.pos_ls_shown = [
                [
                    i * span_big_scale,
                    0,
                    span_big_scale,
                    thickness,
                ]
                for i in range(scale_num_shown - 1)
            ]
            self.pos_ls_shown.append([
                self.width() - span_small_scale,
                0,
                span_small_scale - 1,  # 这里不减1最后的标尺刻度绘制不全
                thickness,
            ])
        else:
            self.pos_ls_shown = [
                [
                    0,
                    i * span_big_scale,
                    thickness,
                    span_big_scale,
                ]
                for i in range(scale_num_shown - 1)
            ]
            self.pos_ls_shown.append([
                0,
                self.height() - span_small_scale,
                thickness,
                span_small_scale - 1,  # 这里不减1最后的标尺刻度绘制不全
            ])

    def generate_font_ls_shown(self):
        """生成显示的文字"""
        if self.font_ls_origin is None:
            if self.direction == Qt.Horizontal:
                self.font_ls_shown = [str(i) for i in range(1, self.scale_num_shown + 1)]
            else:
                self.font_ls_shown = [chr(65 + i) for i in range(self.scale_num_shown)]
        else:
            if len(self.font_ls_origin) == self.scale_num_shown:
                self.font_ls_shown = self.font_ls_origin
            else:
                raise ValueError(f"自定义标尺文字个数为{len(self.font_ls_origin)}，"
                                 f"标尺个数为{self.scale_num_shown}，二者必须相等。")

    def resizeEvent(self, event: QResizeEvent):
        """重新设canvas大小和位置，标尺大小和位置"""
        try:
            self.calculate_show_pos()
        except Exception as e:
            logger.error(f"e: {e}", exc_info=True)
            raise

    def paintEvent(self, event: QPaintEvent):

        painter = QPainter()
        try:
            painter.begin(self)
            # 以（0,0）点为坐标原点原点，图像画上去。
            painter.translate(QPoint(0, 0))  # 设置原点位置
            # - - -
            painter.save()
            # 背景色
            brush = QBrush(self.background_color, Qt.SolidPattern)
            painter.setPen(Qt.NoPen)
            painter.setBrush(brush)
            rect = QRectF(0, 0, self.width(), self.height())
            painter.drawRect(rect)
            painter.restore()

            # - - -
            for index, scale_pos in enumerate(self.pos_ls_shown):
                # 绘制标尺
                x, y, w, h = (scale_pos[0], scale_pos[1], scale_pos[2], scale_pos[3])
                pen = QPen(self.line_color)
                painter.setPen(pen)
                if self.pos_ls_origin is not None:
                    # 有自定义的标尺pos
                    rect = QRectF(x, y, w, h)
                    painter.drawRect(rect)
                else:
                    # 无自定义的标尺pos
                    if self.direction == Qt.Horizontal:
                        # 水平标尺
                        if index == len(self.pos_ls_shown) - 1:
                            # 上横线
                            painter.drawLine(QPointF(0, 0),
                                             QPointF(self.width(), 0))
                            # 下横线
                            painter.drawLine(QPointF(0, self.height() - 1),
                                             QPointF(self.width(), self.height() - 1))
                            # 左竖线
                            painter.drawLine(QPointF(self.width() - 1, 0),
                                             QPointF(self.width() - 1, self.height() - 1))
                        # 竖分割线
                        line = QLineF(QPointF(x, y), QPointF(x, y + h))
                        painter.drawLine(line)
                    else:
                        # 竖直标尺
                        if index == len(self.pos_ls_shown) - 1:
                            # 左竖线
                            painter.drawLine(QPointF(0, 0),
                                             QPointF(0, self.height()))
                            # 右竖线
                            painter.drawLine(QPointF(self.width() - 1, 0),
                                             QPointF(self.width() - 1, self.height()))
                            # 下横线
                            painter.drawLine(QPointF(0, self.height() - 1),
                                             QPointF(self.width() - 1, self.height() - 1))
                        # 横分割线
                        line = QLineF(QPointF(x, y), QPointF(x + w, y))
                        painter.drawLine(line)
                # - - -
                # 绘制标尺中文字
                pen = QPen(self.font_color)
                painter.setPen(pen)
                font = self.font_ls_shown[index]
                scale_font = QFont()
                scale_font.setFamily("Microsoft YaHei")
                scale_font.setPixelSize(self.font_size)
                painter.setFont(scale_font)
                painter.setPen(pen)
                font_rectangle = QRectF(*scale_pos)
                painter.drawText(font_rectangle, Qt.AlignCenter, font)
        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            raise
        finally:
            painter.end()


# ==================== 测试代码 ====================
class MyWidget(QWidget):

    def __init__(self, *args):
        super().__init__(*args)

        scale_thickness = 18
        gg = [6, 66]
        per_h = 1
        per_v = 1

        line_color = QColor(255, 0, 0)

        # 假设原图像的宽高
        # self.img_w = 5150
        # self.img_h = 3150

        # 模拟画布
        self.image_canvas = Canvas(parent=self)
        self.image_canvas.setObjectName("image_canvas")

        # 水平标尺-上
        self.scale_plate_h_top = ScalePlate(parent=self)
        self.scale_plate_h_top.set_direction(direction=Qt.Horizontal)
        self.scale_plate_h_top.set_line_color(line_color)
        self.scale_plate_h_top.set_thickness(thickness=scale_thickness)
        self.scale_plate_h_top.set_scale_num_origin(scale_num_origin=gg[1])
        self.scale_plate_h_top.set_per(per=per_h)
        # 水平标尺-下
        self.scale_plate_h_bottom = ScalePlate(parent=self)
        self.scale_plate_h_bottom.set_direction(direction=Qt.Horizontal)
        self.scale_plate_h_bottom.set_line_color(line_color)
        self.scale_plate_h_bottom.set_thickness(thickness=scale_thickness)
        self.scale_plate_h_bottom.set_scale_num_origin(scale_num_origin=gg[1])
        self.scale_plate_h_bottom.set_per(per=per_h)

        # 竖直标尺-左
        self.scale_plate_v_left = ScalePlate(parent=self)
        self.scale_plate_v_left.set_direction(direction=Qt.Vertical)
        self.scale_plate_v_left.set_line_color(line_color)
        self.scale_plate_v_left.set_thickness(thickness=scale_thickness)
        self.scale_plate_v_left.set_scale_num_origin(scale_num_origin=gg[0])
        self.scale_plate_v_left.set_per(per=per_v)
        # 竖直标尺-右
        self.scale_plate_v_right = ScalePlate(parent=self)
        self.scale_plate_v_right.set_direction(direction=Qt.Vertical)
        self.scale_plate_v_right.set_line_color(line_color)
        self.scale_plate_v_right.set_thickness(thickness=scale_thickness)
        self.scale_plate_v_right.set_scale_num_origin(scale_num_origin=gg[0])
        self.scale_plate_v_right.set_per(per=per_v)

        #
        self.resize(850, 550)

    def init_data(self):
        scale_pos_ls_h = [
            [75, 10, 500, 250],
            [575, 10, 500, 250],
            [1075, 10, 500, 250],
            [1575, 10, 500, 250],
            [2075, 10, 500, 250],
            [2575, 10, 500, 250],
            [3075, 10, 500, 250],
            [3575, 10, 500, 250],
            [4075, 10, 500, 250],
            [4575, 10, 500, 250],
        ]
        font_ls_h = ["X" + str(i) for i in range(1, len(scale_pos_ls_h) + 1)]
        logger.debug(f"font_ls_h = {font_ls_h}")
        self.scale_plate_h_top.set_pos_ls_origin(pos_ls=scale_pos_ls_h)
        self.scale_plate_h_top.set_font_ls_origin(font_ls=font_ls_h)
        # self.scale_plate_h_top.set_scale_num_origin(scale_num_origin=5)
        # - - -
        self.scale_plate_h_bottom.set_pos_ls_origin(pos_ls=scale_pos_ls_h)
        self.scale_plate_h_bottom.set_font_ls_origin(font_ls=font_ls_h)

        scale_pos_ls_v = [
            [10, 75, 100, 500],
            [10, 575, 100, 500],
            [10, 1075, 100, 500],
            [10, 1575, 100, 500],
            [10, 2075, 100, 500],
            [10, 2575, 100, 500],
        ]
        font_ls_v = ["X" + chr(65 + i) for i in range(len(scale_pos_ls_v))]
        logger.debug(f"font_ls_v = {font_ls_v}")
        self.scale_plate_v_left.set_pos_ls_origin(pos_ls=scale_pos_ls_v)
        self.scale_plate_v_left.set_font_ls_origin(font_ls=font_ls_v)
        # - - -
        self.scale_plate_v_right.set_pos_ls_origin(pos_ls=scale_pos_ls_v)
        self.scale_plate_v_right.set_font_ls_origin(font_ls=font_ls_v)

    def resizeEvent(self, event: QResizeEvent):
        """重新设canvas大小和位置，标尺大小和位置"""
        try:
            img_w = self.image_canvas.original_pix.width()
            img_h = self.image_canvas.original_pix.height()
            ratio = self.calculate_scale_ratio(img_w, img_h)
            logger.debug(f"MyWidget---resizeEvent---ratio = {ratio}")
            new_w_h = int(img_w * ratio), int(img_h * ratio)
            self.image_canvas.resize(*new_w_h)
            # - - -
            # self.image_canvas.resize(
            #     self.width() - (self.scale_plate_v_left.thickness + self.scale_plate_v_right.thickness),
            #     self.height() - (self.scale_plate_h_top.thickness + self.scale_plate_h_bottom.thickness)
            # )

            self.set_img_ratio(ratio)
            self.move_canvas_and_scale()
            # self.update()
        except Exception as e:
            logger.error(f"e: {e}", exc_info=True)
            raise

    def set_img_ratio(self, ratio):
        """设置标尺的图像缩放比"""
        try:
            self.scale_plate_h_top.set_img_ratio(ratio)
            self.scale_plate_h_bottom.set_img_ratio(ratio)
            self.scale_plate_v_left.set_img_ratio(ratio)
            self.scale_plate_v_right.set_img_ratio(ratio)
        except Exception as e:
            logger.error(f"e: {e}", exc_info=True)
            raise

    def calculate_scale_ratio(self, img_w, img_h):
        """
        计算缩放比例
        :param img_w: 原图像宽
        :param img_h: 原图像高
        :return:
        """
        try:
            # 当前widget去掉标尺的宽高
            win_w, win_h = (
                self.width() - (self.scale_plate_v_left.thickness + self.scale_plate_v_right.thickness),
                self.height() - (self.scale_plate_h_top.thickness + self.scale_plate_h_bottom.thickness)
            )
            # - -
            # parent = self.parentWidget()
            # # 原始图像宽，高
            # win_w, win_h = parent.width() - 2 * self.scale_thickness, parent.height() - 2 * self.scale_thickness
            # - -
            radio_x = win_w / img_w
            radio_y = win_h / img_h
            radio = radio_x if radio_x < radio_y else radio_y
            return radio
        except Exception as e:
            logger.error(f"e: {e}", exc_info=True)
            raise

    def move_canvas_and_scale(self):
        """重新设置canvas、标尺的位置和大小"""
        try:
            # canvas
            self.image_canvas.move(self.scale_plate_h_top.thickness, self.scale_plate_v_left.thickness)

            # 标尺-上
            self.scale_plate_h_top.setGeometry(self.scale_plate_h_top.thickness,
                                               0,
                                               self.image_canvas.width(),
                                               self.scale_plate_h_top.thickness)
            logger.debug(f"self.scale_plate_h_top.width() = {self.scale_plate_h_top.width()}")
            logger.debug(f"self.scale_plate_h_top.height() = {self.scale_plate_h_top.height()}")
            # 标尺-下
            self.scale_plate_h_bottom.setGeometry(self.scale_plate_h_bottom.thickness,
                                                  self.image_canvas.height() + self.scale_plate_h_bottom.thickness,
                                                  self.image_canvas.width(),
                                                  self.scale_plate_h_bottom.thickness)

            # 标尺-左
            self.scale_plate_v_left.setGeometry(0,
                                                self.scale_plate_v_left.thickness,
                                                self.scale_plate_v_left.thickness,
                                                self.image_canvas.height())
            logger.debug(f"self.scale_plate_v_left.width() = {self.scale_plate_v_left.width()}")
            logger.debug(f"self.scale_plate_v_left.height() = {self.scale_plate_v_left.height()}")
            # 标尺-右
            self.scale_plate_v_right.setGeometry(self.image_canvas.width() + self.scale_plate_v_left.thickness,
                                                 self.scale_plate_v_right.thickness,
                                                 self.scale_plate_v_right.thickness,
                                                 self.image_canvas.height())
        except Exception as e:
            logger.error(f"e: {e}", exc_info=True)
            raise


class Canvas(QWidget):
    def __init__(self, *args, parent=None):
        super().__init__(parent, *args)
        # self.setMinimumSize(1000, 600)

        self.original_pix = QPixmap()
        with open('../images/EL_TP3.jpg', 'rb') as f:
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
        except Exception as e:
            logger.error(f"e: {e}", exc_info=True)
            raise

    def resizeEvent(self, event: QResizeEvent):
        """ 改变大小事件 """
        super().resizeEvent(event)
        try:
            logger.debug(f"Canvas----resizeEvent")
            logger.debug(f"Canvas----resizeEvent")
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
        # self.repaint()
        # self.update()


class Stack(QWidget):
    """模拟放带标尺的canvas的stack"""

    def __init__(self, *args, parent=None):
        super().__init__(parent, *args)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.my_widget = MyWidget(self)
        self.my_widget.init_data()
        layout.addWidget(self.my_widget)

        self.qss = """
        Stack {
            background-color: rgb(0, 0, 0);
        }
        """
        self.setStyleSheet(self.qss)

        self.resize(800, 600)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # - - -
    # my_widget = MyWidget()
    # my_widget.init_data()
    # - - -
    # my_widget = Canvas()
    # - - -
    # my_widget = Stack()
    # - - -
    my_widget = ScalePlate()
    my_widget.set_line_color(QColor(255, 0, 0))
    # - - -
    # scale_thickness = 18
    # gg = [6, 66]
    # per_h = 1
    # per_v = 1
    # my_widget = ScalePlate()
    # my_widget.set_line_color(QColor(255, 0, 0))
    # my_widget.set_direction(direction=Qt.Horizontal)
    # my_widget.set_thickness(thickness=scale_thickness)
    # my_widget.set_scale_num_origin(scale_num_origin=gg[1])
    # my_widget.set_per(per=per_h)
    # my_widget.resize(1200, 100)

    my_widget.show()
    sys.exit(app.exec_())
