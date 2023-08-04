import sys
from typing import List

from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QWidget, QVBoxLayout, \
    QHBoxLayout, QPushButton, QGridLayout, QFrame, QGraphicsLineItem
from PyQt5.QtGui import QPixmap, QPen, QPainter, QMouseEvent, QColor, QKeyEvent
from PyQt5.QtCore import Qt, QRectF, QPointF, QLineF

"""
拖拽，移动事件在画布类中实现
绘制顶点
"""


class DraggableRectItem(QGraphicsRectItem):

    def __init__(self, rect: QRectF):
        super().__init__(rect)
        self.setFlags(QGraphicsRectItem.ItemIsSelectable)
        self.active_vertex = None

        self.points: List[QGraphicsRectItem] = []


class ImageViewer(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setMouseTracking(True)  # 开启鼠标移动事件追踪
        self.viewport().setCursor(Qt.ArrowCursor)

        self.image_item = None
        self.current_item = None
        self.start_x, self.start_y = None, None
        self.end_x, self.end_y = None, None
        self.pixmap = QPixmap()

        self.zoom_in_factor = 1.2
        self.zoom_out_factor = 0.8

        self._middle_button_pressed = False
        self._middle_button_last_pos = None

        self.side_length = 150

        self._fit_once = False  # 是否已经自适应窗口大小 1 次
        self._allow_adjust = True  # 是否允许调整矩形大小

        pen = QPen(Qt.black, 6)
        self.cross_item_h = QGraphicsLineItem()
        self.cross_item_h.setPen(pen)
        self.cross_item_v = QGraphicsLineItem()
        self.cross_item_v.setPen(pen)

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Delete:
            print(f"【ImageViewer】----del")
            items = self.get_all_rect_items()
            for item in items:
                if item.isSelected():
                    self._delete_rect(item)
        # if event.key() == Qt.Key_F:
        #     if self.image_item:
        #         self.fitInView(self.image_item, Qt.KeepAspectRatio)

    def load_image(self, image_path):
        self.pixmap = QPixmap(image_path)
        if not self.pixmap.isNull():
            self.side_length = int(max([self.pixmap.width(), self.pixmap.height()]) * 0.02)
            self.scene().clear()
            self.image_item = self.scene().addPixmap(self.pixmap)
            self.setSceneRect(QRectF(self.pixmap.rect()))
            self.fitInView(self.image_item, Qt.KeepAspectRatio)

            self.scene().addItem(self.cross_item_h)
            self.scene().addItem(self.cross_item_v)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Ensure the image fits the view on startup
        if self.image_item and not self._fit_once:
            self.fitInView(self.image_item, Qt.KeepAspectRatio)
            self._fit_once = True

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        pos = self.mapToScene(event.pos())
        x = pos.x()
        y = pos.y()
        print(f"【ImageViewer】 【mousePressEvent】 x={x}, y={y}")

        try:
            if event.button() == Qt.LeftButton:
                self.setDragMode(QGraphicsView.NoDrag)
                if not self.current_item:
                    # top_item = self.scene().itemAt(pos, self.transform())
                    top_item = self.get_topmost_item(pos)
                    print(f"【ImageViewer】 【mousePressEvent top_item={top_item}")
                    if top_item is self.image_item:
                        # pos = self.mapToScene(event.pos())
                        self.start_x, self.start_y = pos.x(), pos.y()
                        self.current_item = DraggableRectItem(QRectF(self.start_x, self.start_y, 0, 0))
                        brush = QColor(255, 0, 0, 30)  # 红色填充，透明度为100
                        self.current_item.setBrush(brush)
                        pen = QPen(Qt.red, 5)
                        self.current_item.setPen(pen)
                        self.scene().addItem(self.current_item)
                        print("【ImageViewer】 【mousePressEvent】 画新的框------------")
                    elif isinstance(top_item, DraggableRectItem):
                        # pos = self.mapToScene(event.pos())
                        # pos = event.pos()
                        # pos = self.mapFromScene(event.pos())
                        x, y = pos.x(), pos.y()
                        print(f"【DraggableRectItem】 x,y = {x}, {y}")

                        rect = top_item.rect()
                        top_left = rect.topLeft()
                        bottom_right = rect.bottomRight()
                        print(f"【DraggableRectItem】 top_left = {top_left}")
                        print(f"【DraggableRectItem】 bottom_right = {bottom_right}")

                        # 左上角范围
                        lt_min_x = top_left.x() - self.side_length / 2
                        lt_max_x = top_left.x() + self.side_length / 2
                        print(f"【DraggableRectItem】 lt_min_x,lt_max_x = {lt_min_x}, {lt_max_x}")
                        lt_min_y = top_left.y() - self.side_length / 2
                        lt_max_y = top_left.y() + self.side_length / 2
                        print(f"【DraggableRectItem】 lt_min_y,lt_max_y = {lt_min_y}, {lt_max_y}")

                        # 右下角范围
                        rb_min_x = bottom_right.x() - self.side_length / 2
                        rb_max_x = bottom_right.x() + self.side_length / 2
                        print(f"【DraggableRectItem】 rb_min_x,rb_max_x = {rb_min_x}, {rb_max_x}")
                        rb_min_y = bottom_right.y() - self.side_length / 2
                        rb_max_y = bottom_right.y() + self.side_length / 2
                        print(f"【DraggableRectItem】 rb_min_y,rb_max_y = {rb_min_y}, {rb_max_y}")

                        # Allow adjusting the top-left and bottom-right corners
                        if (lt_min_x <= x <= lt_max_x) and (lt_min_y <= y <= lt_max_y):
                            # 左上角
                            top_item.active_vertex = "top_left"
                            print("【DraggableRectItem】 top_left")
                        elif (rb_min_x <= x <= rb_max_x) and (rb_min_y <= y <= rb_max_y):
                            top_item.active_vertex = "bottom_right"
                            print("【DraggableRectItem】 bottom_right")
                        else:
                            print("【DraggableRectItem】 move")
                            self.start_x, self.start_y = pos.x(), pos.y()
                            top_item.active_vertex = 'move'
                        print(f"【mousePressEvent】 【DraggableRectItem】 【active_vertex:{top_item.active_vertex}】")
                        self.current_item = top_item
            elif event.button() == Qt.MiddleButton:
                self.viewport().setCursor(Qt.OpenHandCursor)
                self._middle_button_last_pos = event.pos()
                self._middle_button_pressed = True
        except Exception as e:
            print(f"error: {e}")

    def get_topmost_item(self, scene_pos):
        all_items = self.scene().items()
        for item in all_items:
            if isinstance(item, DraggableRectItem):
                if item.contains(item.mapFromScene(scene_pos)):  # 判断item是否包含给定的点
                    return item

        if self.image_item and self.image_item.contains(scene_pos):
            return self.image_item

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        pos = self.mapToScene(event.pos())
        x = pos.x()
        y = pos.y()
        try:
            self.cross_item_v.setLine(QLineF(QPointF(x, y - 100), QPointF(x, y + 100)))
            self.cross_item_h.setLine(QLineF(QPointF(x - 100, y), QPointF(x + 100, y)))
        except Exception as e:
            print(f"error: {e}")

        if self.current_item:
            if self.current_item.active_vertex and self._allow_adjust:
                # pos = self.mapToScene(event.pos())
                # pos = event.pos()
                # pos = self.mapFromScene(event.pos())
                x, y = pos.x(), pos.y()

                rect = self.current_item.rect()
                item_x_old = rect.x()
                item_y_old = rect.y()
                item_w_old = rect.width()
                item_h_old = rect.height()

                if self.current_item.active_vertex == "top_left":
                    w = (item_x_old + item_w_old) - x
                    h = (item_y_old + item_h_old) - y
                    self.current_item.setRect(QRectF(x, y, w, h))
                elif self.current_item.active_vertex == "bottom_right":
                    w = x - item_x_old
                    h = y - item_y_old
                    self.current_item.setRect(QRectF(item_x_old, item_y_old, w, h))
                elif self.current_item.active_vertex == "move":
                    x_move = (x - self.start_x)
                    y_move = (y - self.start_y)
                    x_new = item_x_old + x_move
                    y_new = item_y_old + y_move
                    self.current_item.setRect(QRectF(x_new, y_new, item_w_old, item_h_old))
                    self.start_x = x
                    self.start_y = y
                    print("整体移动矩形")
            elif self.current_item.active_vertex is None:

                self.end_x, self.end_y = pos.x(), pos.y()
                self.current_item.setRect(
                    QRectF(self.start_x, self.start_y, self.end_x - self.start_x, self.end_y - self.start_y))

                # 将矩形转换为从左上角，到右下角绘制
                rect = self.current_item.rect()
                tl_x = rect.x()
                tl_y = rect.y()
                br_x = rect.x() + rect.width()
                br_y = rect.y() + rect.height()
                if tl_x < br_x:
                    x = tl_x
                else:
                    x = br_x
                if tl_y < br_y:
                    y = tl_y
                else:
                    y = br_y
                w = abs(rect.width())
                h = abs(rect.height())
                self.current_item.setRect(QRectF(x, y, w, h))

                # if self.start_x < self.end_x:
                #     x = self.start_x
                # else:
                #     x = self.end_x
                #
                # if self.start_y < self.end_y:
                #     y = self.start_y
                # else:
                #     y = self.end_y
                # w = abs(self.start_x - self.end_x)
                # h = abs(self.start_y - self.end_y)
                # self.current_item.setRect(QRectF(x, y, w, h))

            self.draw_rect_points(self.current_item)

        if self._middle_button_pressed:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            delta = event.pos() - self._middle_button_last_pos
            self._middle_button_last_pos = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
        else:
            self.setDragMode(QGraphicsView.NoDrag)

        self.repaint()

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
        self.viewport().setCursor(Qt.ArrowCursor)
        self.setDragMode(QGraphicsView.NoDrag)
        if event.button() == Qt.LeftButton:
            self.current_item = None
            self.start_x, self.start_y, self.end_x, self.end_y = None, None, None, None
        elif event.button() == Qt.MiddleButton:
            self._middle_button_pressed = False

    # def mouseDoubleClickEvent(self, event):
    #     super().mouseDoubleClickEvent(event)
    #     print(f"【ImageViewer】 【mouseDoubleClickEvent】 【self.verticalScrollBar().value()】 "
    #           f"--------------- {self.verticalScrollBar().value()}")
    #     pos = self.mapToScene(event.pos())
    #     if event.button() == Qt.LeftButton:
    #         top_item = self.get_topmost_rect_item(pos)
    #         if isinstance(top_item, DraggableRectItem):
    #             if top_item.isSelected():
    #                 self._delete_rect(top_item)

    def wheelEvent(self, event):
        super().wheelEvent(event)

        # 滚轮缩放
        if event.angleDelta().y() > 0:
            self.scale(self.zoom_in_factor, self.zoom_in_factor)
        else:
            self.scale(self.zoom_out_factor, self.zoom_out_factor)

        print(f"self.pixmap.width()={self.pixmap.width()}, self.pixmap.height()={self.pixmap.height()}")
        print(f"self.get_all_rect_boxes()={self.get_all_rect_boxes()}")
        print(f"self.get_all_rect_points()={self.get_all_rect_points()}")
        print("= " * 30)

    def draw_rect_points(self, rect_item: DraggableRectItem):
        tl_point = rect_item.rect().topLeft()
        br_point = rect_item.rect().bottomRight()
        if rect_item.points:
            print(f"rect_item.points = {rect_item.points}")
            self.scene().removeItem(rect_item.points[0])
            self.scene().removeItem(rect_item.points[1])

        tl_point_item = self.draw_point(tl_point)
        br_point_item = self.draw_point(br_point)
        print(f"tl_point={tl_point}, br_point={br_point}")
        rect_item.points = [tl_point_item, br_point_item]

    def draw_point(self, point: QPointF):
        x = point.x() - self.side_length / 2
        y = point.y() - self.side_length / 2

        item = QGraphicsRectItem(QRectF(x, y, self.side_length, self.side_length))
        brush = QColor(255, 0, 0, 255)  # 红色填充，透明度为100
        item.setBrush(brush)
        pen = QPen(Qt.red, 1)
        item.setPen(pen)
        self.scene().addItem(item)
        return item

    def get_all_rect_boxes(self):
        """x,y,w,h"""
        ls = []
        for item in self.get_all_rect_items():
            rect = item.mapRectToItem(self.image_item, item.rect())
            x = rect.x()
            y = rect.y()
            w = rect.width()
            h = rect.height()
            ls.append([x, y, w, h])
        return ls

    def get_all_rect_points(self):
        """对角线上的两点坐标"""
        try:
            ls = []
            for item in self.get_all_rect_items():
                rect = item.mapRectToItem(self.image_item, item.rect())
                lt = rect.topLeft()
                rb = rect.bottomRight()
                ls.append([[lt.x(), lt.y()], [rb.x(), rb.y()]])
            return ls
        except Exception as e:
            print(f"error： {e}")

    def get_all_rect_items(self):
        # 获取场景中的全部矩形项
        all_items = self.scene().items()
        rect_items = [item for item in all_items if isinstance(item, DraggableRectItem)]
        return rect_items

    def clear_all_rect(self):
        print(f"clear_all_rect")
        rect_items = self.get_all_rect_items()
        for item in rect_items:
            self._delete_rect(item)

    def _delete_rect(self, item):
        self.scene().removeItem(item)
        for point_item in item.points:
            self.scene().removeItem(point_item)


class MyUi(object):

    def __init__(self, parent):
        layout = QVBoxLayout(parent)

        layout_1 = QHBoxLayout()
        self.del_all_btn = QPushButton(parent)
        self.del_all_btn.setText("删除全部")
        layout_1.addWidget(self.del_all_btn)
        layout.addLayout(layout_1)

        self.viewer = ImageViewer(parent)
        layout.addWidget(self.viewer)


class MyWidget(QWidget):

    def __init__(self, *args, parent=None):
        super().__init__(parent, *args)

        self.ui = MyUi(self)

        self._bind_event()

    def _bind_event(self):
        self.ui.del_all_btn.clicked.connect(self.ui.viewer.clear_all_rect)


class FourUi(object):

    def __init__(self, parent):
        layout = QGridLayout(parent)

        self.label_component_1 = LabelComponent(parent=parent)
        layout.addWidget(self.label_component_1, 0, 0, 1, 1)

        self.label_component_2 = LabelComponent(parent=parent)
        layout.addWidget(self.label_component_2, 0, 1, 1, 1)

        self.label_component_3 = LabelComponent(parent=parent)
        layout.addWidget(self.label_component_3, 1, 0, 1, 1)

        self.label_component_4 = LabelComponent(parent=parent)
        layout.addWidget(self.label_component_4, 1, 1, 1, 1)


class LabelComponent(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = QVBoxLayout(self)

        layout_1 = QHBoxLayout()
        self.del_all_btn = QPushButton(parent)
        self.del_all_btn.setText("删除全部")
        layout_1.addWidget(self.del_all_btn)
        layout.addLayout(layout_1)

        self.viewer = ImageViewer(parent)
        layout.addWidget(self.viewer)

        self.del_all_btn.clicked.connect(self.viewer.clear_all_rect)


class MyFourWidget(QWidget):

    def __init__(self, *args, parent=None):
        super().__init__(parent, *args)

        self.ui = FourUi(self)

    def load_image(self, image_path):
        self.ui.label_component_1.viewer.load_image(image_path)
        self.ui.label_component_2.viewer.load_image(image_path)
        self.ui.label_component_3.viewer.load_image(image_path)
        self.ui.label_component_4.viewer.load_image(image_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    image_path_el = "./images/EL_TP3"
    image_path_vl = "./images/VI_TP3"

    # widget = MyWidget()
    # widget.resize(1000, 600)
    # widget.ui.viewer.load_image(image_path_el)

    widget = MyFourWidget()
    widget.resize(1900, 1000)
    widget.load_image(image_path_el)
    # widget.ui.label_component_1.viewer.load_image(image_path_el)
    # widget.ui.label_component_2.viewer.load_image(image_path_vl)
    # widget.ui.label_component_3.viewer.load_image(image_path_vl)
    # widget.ui.label_component_4.viewer.load_image(image_path_el)

    widget.show()

    sys.exit(app.exec_())
