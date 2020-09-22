# -*- coding:utf-8 -*-
import logging
import sys

from PyQt5.QtCore import QRectF, Qt, QPointF, QSize, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPaintEvent, QPainter, QBrush, QColor, QPen, QRadialGradient, QPainterPath, QMouseEvent, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QGridLayout

logger = logging.getLogger(__name__)


class PieData(object):
    """饼状图数据"""

    def __init__(self, name, percent, color: tuple, *args):
        super().__init__(*args)
        self.percent = percent
        self.name = name
        self.data = None  # TODO: 数据库统计数据

        self.pie_color = QColor(*color)
        self.pie_span_angle = self.percent * 360  # (单位：度)
        self.pie_path = QPainterPath()  # 扇形的path

        self.category_point_color = QColor(*color)
        self.category_point_path = QPainterPath()  # 原点path
        self.category_text_rectangle: QRectF = None  # 标签文字的矩形框
        self.category_text_space = 5  # 文字框和圆点的间距
        self.category_width = 0  # 圆点+文字+间距
        self.category_font = QFont()

    def paint(self, painter: QPainter,
              pie_start_angle, pie_rectangle,
              point_r, point_rectangle: QRectF):

        try:
            painter.save()
            # 绘制扇形
            brush = QBrush(self.pie_color, Qt.SolidPattern)
            painter.setPen(Qt.NoPen)
            painter.setBrush(brush)
            self.pie_path.clear()
            self.pie_path.moveTo(pie_rectangle.center())
            self.pie_path.arcTo(pie_rectangle, pie_start_angle, self.pie_span_angle)
            self.pie_path.lineTo(pie_rectangle.center())
            painter.drawPath(self.pie_path)

            # TODO: 绘制引出线(未完待续)
            # pen = QPen()
            # pen.setColor(QColor(255, 255, 255))
            # painter.setPen(pen)
            # line_path = QPainterPath()
            # line_angle = pie_start_angle + self.pie_span_angle / 2
            # line_length = pie_rectangle.width() / 10
            # line_path.arcMoveTo(pie_rectangle, line_angle)
            # line_first_point = line_path.currentPosition()
            # logger.debug("line_angle = {}".format(line_angle))
            # if int(line_angle / 90) == 0 or int(line_angle / 90) == 4:
            #     line_second_point = QPointF(line_first_point.x() + line_length,
            #                                 line_first_point.y() - line_length)
            # elif int(line_angle / 90) == 1:
            #     line_second_point = QPointF(line_first_point.x() - line_length,
            #                                 line_first_point.y() - line_length)
            # elif int(line_angle / 90) == 2:
            #     line_second_point = QPointF(line_first_point.x() - line_length,
            #                                 line_first_point.y() + line_length)
            # elif int(line_angle / 90) == 3:
            #     line_second_point = QPointF(line_first_point.x() + line_length,
            #                                 line_first_point.y() + line_length)
            # line_path.lineTo(line_second_point)
            # painter.drawPath(line_path)

            # 绘制标签-圆点
            brush = QBrush(self.category_point_color, Qt.SolidPattern)
            painter.setPen(Qt.NoPen)
            painter.setBrush(brush)
            self.category_point_path.clear()
            self.category_point_path.moveTo(point_rectangle.center().x(),
                                            point_rectangle.center().y() - point_r)
            self.category_point_path.arcTo(point_rectangle, 90, 360)
            painter.drawPath(self.category_point_path)

            # 绘制标签-文字
            font_size = 0.8 * point_rectangle.width()
            # self.category_font.setFamily("Microsoft YaHei")
            self.category_font.setPixelSize(font_size)
            painter.setFont(self.category_font)
            pen = QPen()
            pen.setColor(self.category_point_color)
            painter.setPen(pen)
            self.category_text_rectangle = QRectF(
                point_rectangle.x() + point_rectangle.width() + self.category_text_space,
                point_rectangle.y(),
                font_size * len(self.name),
                point_rectangle.height()
            )
            painter.drawText(self.category_text_rectangle, Qt.AlignCenter, self.name)
            self.category_width = point_rectangle.width() + self.category_text_space + self.category_text_rectangle.width()
            painter.restore()

        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            message_box = QMessageBox(self)
            message_box.warning(self, "警告", str(e), QMessageBox.Yes, QMessageBox.Yes)

    def set_transparency(self, alpha: int):
        """
        设置透明度
        :param alpha:  0 =< alpha <= 255
        :return:
        """
        if alpha < 0:
            alpha = 0
        elif alpha > 255:
            alpha = 255

        self.pie_color.setAlpha(alpha)

    def mouse_on(self, mouse_x, mouse_y):
        """判断鼠标位置在不在pie上"""
        return self.pie_path.contains(QPointF(mouse_x, mouse_y))


class PieGraph(QWidget):
    """饼图"""
    # 点击饼图中的某一块(参数：被点击的饼图数据)
    pie_data_clicked_signal = pyqtSignal(PieData)

    def __init__(self, *args, parent=None):
        super().__init__(parent, *args)
        self.setMinimumSize(QSize(200, 200))
        self.setMouseTracking(True)

        # 饼状图的path数据
        self.data: [PieData, ...] = list()

        # self._margins = [20, 20, 20, 20]  # [left,top,right,bottom]
        self._margins = [0, 0, 0, 0]  # [left,top,right,bottom]

        self.mouse_x = 0
        self.mouse_y = 0

    def init_data(self, data):
        total_persent = 0
        for pie_data in data:
            pie_data: PieData
            total_persent += pie_data.percent
        if total_persent != 1:
            msg = "饼状图数据的百分比总和为{},不等于1".format(total_persent)
            raise ValueError(msg)
        else:
            self.data = data

    def paintEvent(self, paint_event: QPaintEvent):
        super().paintEvent(paint_event)
        try:
            # logger.debug("- - - - - - - - - - - - - - - - 重绘开始 - - - - - - - - - - - - - - - - - - - - - ")
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing, True)  # 反锯齿

            # 去掉margin后的内部的宽高
            w_minus_margins = self.width() - self._margins[0] - self._margins[2]
            h_minus_margins = self.height() - self._margins[1] - self._margins[3]
            min_side = min([w_minus_margins, h_minus_margins])

            label_margins = [
                10,
                0.05 * self.height(),
                10,
                0.1 * self.height()
            ]
            # 圆点半径
            point_r = 0.012 * min_side
            logger.debug("min_side = {}".format(min_side))

            # 饼图半径
            # pie_r = 0.4 * (min_side - 2 * point_r - label_margins[1] - label_margins[3])
            pie_r = 0.33 * (min_side - 2 * point_r)
            logger.debug("pie_r = {}".format(pie_r))

            # 中心位置
            # widget_center = QPointF(self.width() / 2, self.height() / 2)

            # 标签的间距
            label_space = 0.03 * self.width()

            # 扇形外接正方形
            pie_rectangle = QRectF(
                # self._margins[0] + 0.1 * self.width(),  # x
                # self._margins[1] + 0.1 * self.height(),  # y
                w_minus_margins / 2 + self._margins[0] - pie_r,  # x
                h_minus_margins / 2 + self._margins[1] - pie_r,  # y
                2 * pie_r,  # w
                2 * pie_r,  # h
            )

            painter.begin(self)

            # 绘制矩形
            painter.drawRect(pie_rectangle)

            pie_start_angle: int = 90  # 度
            total_angle = 0
            label_offset = 0  # 标签偏移量

            # 左边第一个圆点的中心坐标
            first_point_center_x = self._margins[0] + 0.05 * self.width()
            first_point_center_y = self._margins[1] + label_margins[1]

            painter.save()
            for pie_data in self.data:
                pie_data: PieData
                # 圆点数据
                point_rectangle = QRectF(first_point_center_x - point_r + label_offset,
                                         first_point_center_y - point_r,
                                         2 * point_r,
                                         2 * point_r)
                # 绘制扇形、点
                pie_data.paint(painter,
                               pie_start_angle, pie_rectangle,
                               point_r, point_rectangle)

                # 下一个圆弧的起始角度
                pie_start_angle += pie_data.pie_span_angle

                # 下一个圆点的x坐标相对于第一个圆点的偏移量
                label_offset += pie_data.category_width + label_space

                # 角度和
                total_angle += pie_data.pie_span_angle
                # - - -

            painter.restore()
            # logger.debug("total_angle = {}".format(total_angle))
            painter.end()
            # logger.debug("- - - - - - - - - - - - - - - - 重绘结束 - - - - - - - - - - - - - - - - - - - - - ")
        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            message_box = QMessageBox(self)
            message_box.warning(self, "警告", str(e), QMessageBox.Yes, QMessageBox.Yes)

    def mouseMoveEvent(self, event: QMouseEvent):
        pos = event.pos()
        self.mouse_x = pos.x()
        self.mouse_y = pos.y()

        try:
            for pie_data in self.data:
                pie_data: PieData
                if pie_data.mouse_on(self.mouse_x, self.mouse_y):
                    pie_data.set_transparency(110)
                else:
                    pie_data.set_transparency(255)
            # logger.debug("鼠标移动事件")
            # self.repaint()
            self.update()
        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            message_box = QMessageBox(self)
            message_box.warning(self, "警告", str(e), QMessageBox.Yes, QMessageBox.Yes)

    def mousePressEvent(self, event: QMouseEvent):
        pos = event.pos()
        self.mouse_x = pos.x()
        self.mouse_y = pos.y()

        try:
            if event.button() == Qt.LeftButton:
                for pie_data in self.data:
                    pie_data: PieData
                    if pie_data.mouse_on(self.mouse_x, self.mouse_y):
                        logger.debug("当前点击的pie是：{}".format(pie_data.name))
                        # TODO: 弹出某个统计界面
                        self.pie_data_clicked_signal.emit(pie_data)
                        break
                else:
                    logger.debug("当前点击的位置不在饼图上")
        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            message_box = QMessageBox(self)
            message_box.warning(self, "警告", str(e), QMessageBox.Yes, QMessageBox.Yes)


class MyUI(object):
    """测试用UI"""

    def __init__(self, parent):
        layout = QGridLayout(parent)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.pie_graph = PieGraph(parent=parent)
        self.pie_graph.setMinimumSize(QSize(1190, 577))
        self.pie_graph.setObjectName("pie_graph")
        layout.addWidget(self.pie_graph)


class MyWidget(QWidget):
    """测试用Widget"""

    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.ui = MyUI(self)
        # self.show()  # 这里不show()会导致某些qss设置不成功,原因不详
        # qss =
        self.setStyleSheet(
            """
                background: rgb(54, 54, 54);
                color : white;
            """)
        self.bind_event()

    def bind_event(self):
        self.ui.pie_graph.pie_data_clicked_signal.connect(self.pie_data_clicked_handler)

    def init_data(self, pie_data: list):
        """"""
        try:
            self.ui.pie_graph.init_data(pie_data)
        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            message_box = QMessageBox(self)
            message_box.warning(self, "警告", str(e), QMessageBox.Yes, QMessageBox.Yes)

    @pyqtSlot(PieData)
    def pie_data_clicked_handler(self, pie_data):
        try:
            logger.debug("接到信号了: {}".format(pie_data.name))
            message_box = QMessageBox(self)
            msg = "当前点击的是：{}".format(pie_data.name)
            message_box.information(self, "信息", str(msg), QMessageBox.Yes, QMessageBox.Yes)
        except Exception as e:
            logger.error(f"Error:{e}", exc_info=True)
            message_box = QMessageBox(self)
            message_box.warning(self, "警告", str(e), QMessageBox.Yes, QMessageBox.Yes)


if __name__ == '__main__':
    # sys.path.append("..")
    # from log_config import settings

    app = QApplication(sys.argv)
    win = MyWidget()
    pie_data: [PieData, ...] = [
        PieData("虚汗", 0.22, (254, 182, 78)),
        PieData("黑斑", 0.2, (165, 165, 165)),
        PieData("破片", 0.12, (92, 196, 159)),
        PieData("分叉隐焊", 0.08, (52, 210, 235)),
        PieData("过焊", 0.1, (96, 172, 252)),
        PieData("短路", 0.1, (145, 136, 231)),
        PieData("单条隐裂", 0.18, (255, 124, 124)),
    ]
    win.init_data(pie_data)
    win.show()
    sys.exit(app.exec_())
