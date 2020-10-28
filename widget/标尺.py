# -*- coding:utf-8 -*-
import math
import sys

from PyQt5.QtCore import Qt, QRectF, QPointF, QPoint, QSize
from PyQt5.QtGui import QPaintEvent, QPainter, QPainterPath, QPen, QColor, QResizeEvent, QPixmap, QBrush, QFont
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QGridLayout
import logging

logger = logging.getLogger(__name__)


class ScalePlate(QWidget):
    """标尺"""

    def __init__(self, *args, parent=None):
        super().__init__(parent, *args)
        # 标尺方向（水平，竖直）
        self.direction = Qt.Horizontal
        # 标尺刻度的原始数据（算法报文中给的数据）[[x,y,w,h], ...]
        self.origin_pos_ls = None
        # 标尺的文字列表[str, ...]
        self.font_text_ls = None
        # 标尺厚度
        self.thickness = 18
        # 实际画在控件上的标尺刻度[[x,y,w,h], ...]
        self.show_pos_ls = None
        # 图像缩放比例
        self.img_ratio = 1.0

        # 根据标尺长度，进行评分时需要的参数
        self.origin_scale_num = 6  # 原始标尺刻度个数
        self.per = 1  # 每几个标尺显示为1个刻度
        # - - -

    def paintEvent(self, event: QPaintEvent):

        painter = QPainter()
        try:
            painter.begin(self)
            # 以（0,0）点为坐标原点原点，图像画上去。
            painter.translate(QPoint(0, 0))  # 设置原点位置
            # - - -
            painter.save()
            # 背景色
            background_color = QColor(243, 208, 143)
            brush = QBrush(background_color, Qt.SolidPattern)
            painter.setPen(Qt.NoPen)
            painter.setBrush(brush)
            rect = QRectF(0, 0, self.width(), self.height())
            painter.drawRect(rect)
            painter.restore()

            # - - -
            # pen = QPen(QColor(172, 9, 255))
            pen = QPen(QColor(255, 0, 0))
            painter.setPen(pen)

            for index, scale_pos in enumerate(self.show_pos_ls):
                # 绘制标尺
                rect = QRectF(*scale_pos)
                painter.drawRect(rect)

                # 绘制标尺中文字
                font_text = self.font_text_ls[index]
                font_size = 0.8 * self.thickness
                scale_font = QFont()
                scale_font.setFamily("Microsoft YaHei")
                scale_font.setPixelSize(font_size)
                painter.setFont(scale_font)
                painter.setPen(pen)
                font_rectangle = QRectF(*scale_pos)
                painter.drawText(font_rectangle, Qt.AlignCenter, font_text)
                # painter.restore()
        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            raise
        finally:
            painter.end()

    def resizeEvent(self, event: QResizeEvent):
        """重新设canvas大小和位置，标尺大小和位置"""
        try:
            self.calculate_show_pos()
        except Exception as e:
            logger.error(f"e: {e}", exc_info=True)
            raise

    def set_origin_scale_num(self, origin_scale_num=6):
        """设置原始标尺刻度个数"""

        self.origin_scale_num = origin_scale_num  # 原始标尺刻度个数

    def set_per(self, per=1):
        """设置每几个标尺显示为1个刻度"""
        self.per = per  # 每几个标尺显示为1个刻度

    def set_img_ratio(self, ratio):
        """设置图像缩放比例"""
        self.img_ratio = ratio

    def set_origin_pos(self, pos_ls=None, font_text_ls=None):
        """设置自定义的标尺刻度的原始数据"""
        # TODO:如果需要重新设置自定义的标签位置和文字内容，请在resize之前调用该方法
        if pos_ls is not None:
            self.origin_pos_ls = pos_ls
        if font_text_ls is not None:
            self.font_text_ls = font_text_ls

    def calculate_show_pos(self):
        """计算要显示的标尺的位置"""
        if self.origin_pos_ls is not None:
            if self.direction == Qt.Horizontal:
                # print(f"水平：self.img_ratio = {self.img_ratio}")
                # 水平
                self.show_pos_ls = [
                    [
                        pos[0] * self.img_ratio,
                        0,
                        (pos[2]) * self.img_ratio,
                        self.thickness - 1
                    ]
                    for pos in self.origin_pos_ls
                ]
            else:
                # 竖直
                # print(f"竖直：self.img_ratio = {self.img_ratio}")
                self.show_pos_ls = [
                    [
                        0,
                        pos[1] * self.img_ratio,
                        self.thickness - 1,
                        (pos[3]) * self.img_ratio
                    ]
                    for pos in self.origin_pos_ls
                ]
        else:
            # TODO: 根据row，column，per来计算
            self.calculate_adaptive_scale_pos_and_scale_text()

    def calculate_adaptive_scale_pos_and_scale_text(self):
        """计算实际显示的标尺刻度pos,以及标尺文字(自适应，不适用自定义的标尺pos)"""
        self.origin_pos_ls = None

        # 单位跨度
        if self.direction == Qt.Horizontal:
            print(f"==== 水平标尺 ====")
        else:
            print(f"==== 竖直标尺 ====")

        res = self.origin_scale_num / self.per
        print(f"self.origin_scale_num = {self.origin_scale_num}")
        print(f"self.per = {self.per}")
        print(f"res = {res}")

        scale_num_shown: int = math.ceil(res)  # 向上取整
        print(f"scale_num_shown = {scale_num_shown}")

        remainder = self.origin_scale_num % self.per  # 余数
        print(f"remainder = {remainder}")
        if remainder == 0:
            big_factor = 1
            small_factor = 1
        else:
            big_factor = self.per
            small_factor = remainder

        print(f"big_factor = {big_factor}")
        print(f"small_factor = {small_factor}")

        # 单位跨度
        if self.direction == Qt.Horizontal:
            span_total = self.width()
        else:
            span_total = self.height()
        span_unit = span_total / ((scale_num_shown - 1) * big_factor + small_factor)
        # 大比例的标尺跨度
        span_big_scale = span_unit * big_factor
        # 小比例的标尺跨度
        span_small_scale = span_unit * small_factor
        # span_small_scale = span_total - (span_big_scale * (scale_num_shown - 1))

        print(f"span_unit = {span_unit}")
        print(f"span_big_scale = {span_big_scale}")
        print(f"span_small_scale = {span_small_scale}")

        thickness = self.thickness - 1
        if self.direction == Qt.Horizontal:
            self.show_pos_ls = [
                [
                    i * span_big_scale,
                    0,
                    span_big_scale,
                    thickness,
                ]
                for i in range(scale_num_shown - 1)
            ]
            self.show_pos_ls.append([
                self.width() - span_small_scale,
                0,
                span_small_scale - 1,  # 这里不减1最后的标尺刻度绘制不全
                thickness,
            ])
            self.font_text_ls = [str(i) for i in range(1, scale_num_shown + 1)]
        else:
            self.show_pos_ls = [
                [
                    0,
                    i * span_big_scale,
                    thickness,
                    span_big_scale,
                ]
                for i in range(scale_num_shown - 1)
            ]
            self.show_pos_ls.append([
                0,
                self.height() - span_small_scale,
                thickness,
                span_small_scale - 1,  # 这里不减1最后的标尺刻度绘制不全
            ])
            self.font_text_ls = [chr(65 + i) for i in range(scale_num_shown)]

        print(f"self.show_pos_ls = {self.show_pos_ls}")
        print("- " * 30)
        # return scale_num_shown, big_factor, small_factor

    def set_direction(self, direction):
        """设置标尺方向"""
        self.direction = direction

    def set_thickness(self, thickness):
        """设置标尺厚度"""
        self.thickness = thickness

        # if self.direction == Qt.Horizontal:
        #     self.setFixedHeight(self.thickness)
        # else:
        #     self.setFixedWidth(self.thickness)


# ==================== 测试代码 ====================
class MyWidget(QWidget):

    def __init__(self, *args):
        super().__init__(*args)
        self.scale_thickness = 18

        gg = [6, 66]
        per_h = 4
        per_v = 1

        # 假设原图像的宽高为800*600
        self.img_w = 5150
        self.img_h = 3150

        #
        self.image_canvas = Canvas(parent=self)
        self.image_canvas.setObjectName("image_canvas")

        # 水平标尺-上
        self.scale_plate_h_top = ScalePlate(parent=self)
        self.scale_plate_h_top.set_direction(Qt.Horizontal)
        self.scale_plate_h_top.set_thickness(self.scale_thickness)
        self.scale_plate_h_top.set_origin_scale_num(origin_scale_num=gg[1])
        self.scale_plate_h_top.set_per(per=per_h)
        # 水平标尺-下
        self.scale_plate_h_bottom = ScalePlate(parent=self)
        self.scale_plate_h_bottom.set_direction(Qt.Horizontal)
        self.scale_plate_h_bottom.set_thickness(self.scale_thickness)
        self.scale_plate_h_bottom.set_origin_scale_num(origin_scale_num=gg[1])
        self.scale_plate_h_bottom.set_per(per=per_h)

        # 竖直标尺-左
        self.scale_plate_v_left = ScalePlate(parent=self)
        self.scale_plate_v_left.set_direction(Qt.Vertical)
        self.scale_plate_v_left.set_thickness(self.scale_thickness)
        self.scale_plate_v_left.set_origin_scale_num(origin_scale_num=gg[0])
        self.scale_plate_v_left.set_per(per=per_v)
        # 竖直标尺-右
        self.scale_plate_v_right = ScalePlate(parent=self)
        self.scale_plate_v_right.set_direction(Qt.Vertical)
        self.scale_plate_v_right.set_thickness(self.scale_thickness)
        self.scale_plate_v_right.set_origin_scale_num(origin_scale_num=gg[0])
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
        font_text_ls_h = [str(i) for i in range(1, len(scale_pos_ls_h) + 1)]
        # print(f"font_text_ls_h = {font_text_ls_h}")
        # self.scale_plate_h_top.set_origin_pos(pos_ls=scale_pos_ls_h, font_text_ls=font_text_ls_h)
        # self.scale_plate_h_bottom.set_origin_pos(pos_ls=scale_pos_ls_h, font_text_ls=font_text_ls_h)

        scale_pos_ls_v = [
            [10, 75, 100, 500],
            [10, 575, 100, 500],
            [10, 1075, 100, 500],
            [10, 1575, 100, 500],
            [10, 2075, 100, 500],
            [10, 2575, 100, 500],
        ]
        font_text_ls_v = [chr(65 + i) for i in range(len(scale_pos_ls_v))]
        # print(f"font_text_ls_v = {font_text_ls_v}")
        # self.scale_plate_v_left.set_origin_pos(pos_ls=scale_pos_ls_v, font_text_ls=font_text_ls_v)
        # self.scale_plate_v_right.set_origin_pos(pos_ls=scale_pos_ls_v, font_text_ls=font_text_ls_v)

    def resizeEvent(self, event: QResizeEvent):
        """重新设canvas大小和位置，标尺大小和位置"""
        try:
            img_w = self.image_canvas.original_pix.width()
            img_h = self.image_canvas.original_pix.height()
            ratio = self.calculate_scale_ratio(self.img_w, self.img_h)
            print(f"MyWidget---resizeEvent---ratio = {ratio}")
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
            # self.image_canvas.setGeometry(
            #     self.scale_plate_h_top.thickness,
            #     self.scale_plate_v_left.thickness,
            #     self.width() - (self.scale_plate_v_left.thickness + self.scale_plate_v_right.thickness),
            #     self.height() - (self.scale_plate_h_top.thickness + self.scale_plate_h_bottom.thickness)
            # )

            # 标尺-上
            self.scale_plate_h_top.setGeometry(self.scale_plate_h_top.thickness,
                                               0,
                                               self.image_canvas.width(),
                                               self.scale_plate_h_top.thickness)
            print(f"self.scale_plate_h_top.width() = {self.scale_plate_h_top.width()}")
            print(f"self.scale_plate_h_top.height() = {self.scale_plate_h_top.height()}")
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
            print(f"self.scale_plate_v_left.width() = {self.scale_plate_v_left.width()}")
            print(f"self.scale_plate_v_left.height() = {self.scale_plate_v_left.height()}")
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
        # print(f"pix_wh = {self.pix.width(),self.pix.height()}")
        #
        # x_wh = (66, 88)
        # yyy = self.pix.scaled(*x_wh)
        # print(f"pix_wh = {self.pix.width(),self.pix.height()}")
        # print(f"yyy_wh = {yyy.width(),yyy.height()}")

    def paintEvent(self, event: QPaintEvent):

        # print(f'Canvas---paintEvent---{self.parentWidget()}')
        # print(f'Canvas---paintEvent---{self.width(), self.height()}')
        try:
            super().paintEvent(event)

            p = QPainter()
            p.begin(self)
            # 以（100,100）点为坐标原点原点，图像画上去。
            p.translate(QPoint(0, 0))  # 设置原点位置
            p.drawPixmap(0, 0, self.current_pix)  # 相对于原点位置，画图像
            a = QPointF(2, 5)
            b = QPointF(3, 15)
            c = (a + b) / 2
            # print(f"c = {c.x(),c.y()}")

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
            print(f"Canvas----resizeEvent")
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
        """
        计算缩放比例
        :param img_w: 原始图像宽
        :param img_h: 原始图像高
        :return:
        """
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
        print(f"load_pix")
        self.current_pix = pix  # 有图像的时候才绘制网格
        # self.repaint()
        # self.update()


class Yyy(QWidget):
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
        Yyy {
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
    my_widget = Yyy()

    my_widget.show()
    sys.exit(app.exec_())
