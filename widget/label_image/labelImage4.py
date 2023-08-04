# 下面述代码执行后，图像没有自适应窗口大小, 如何修改，使其只在启动时，适配窗口大小
import sys
from typing import List

from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QWidget, QVBoxLayout, \
    QHBoxLayout, QPushButton, QGraphicsItem, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QPen, QPainter, QMouseEvent, QColor, QResizeEvent, QKeyEvent
from PyQt5.QtCore import Qt, QRectF, QPointF, pyqtSignal

SIDE_LENGTH = 50

"""
拖拽，移动事件在自定义的矩形类中实现
"""


class DraggableRectItem(QGraphicsRectItem):
    # signal_draw_points = pyqtSignal(int)

    def __init__(self, rect: QRectF):
        super().__init__(rect)
        self.setFlags(QGraphicsRectItem.ItemIsMovable | QGraphicsRectItem.ItemIsSelectable)
        # self.setFlags(QGraphicsRectItem.ItemIsMovable)
        self.active_vertex = None

        self.points: List[QGraphicsRectItem] = []

    def mouseMoveEvent(self, event):
        if self.active_vertex:
            # pos = self.mapToScene(event.pos())
            pos = event.pos()
            x, y = pos.x(), pos.y()

            rect = self.rect()

            if self.active_vertex == "top_left":
                rect.setTopLeft(QPointF(x, y))
            elif self.active_vertex == "bottom_right":
                rect.setBottomRight(QPointF(x, y))

            self.setRect(rect)
        else:
            super().mouseMoveEvent(event)

        # try:
        #     self.signal_draw_points.emit(1)
        # except Exception as e:
        #     print(f"error: {e}")

        print(f"【DraggableRectItem】 【mouseMoveEvent】 【active_vertex:{self.active_vertex}】")

    def mousePressEvent(self, event):
        # pos = self.mapToScene(event.pos())
        # x, y = pos.x(), pos.y()
        # rect = self.rect()
        # if (rect.left() <= x <= rect.left() + 10 and rect.top() <= y <= rect.top() + 10):
        #     self.active_vertex = "top_left"
        # elif (rect.right() - 10 <= x <= rect.right() and rect.bottom() - 10 <= y <= rect.bottom()):
        #     self.active_vertex = "bottom_right"
        # else:
        #     super().mousePressEvent(event)
        # ----------
        print(f"【DraggableRectItem】 【mousePressEvent】 out")

        try:
            # pos = self.mapToScene(event.pos())
            pos = event.pos()
            x, y = pos.x(), pos.y()
            print(f"【DraggableRectItem】 x,y = {x}, {y}")

            rect = self.rect()
            top_left = rect.topLeft()
            bottom_right = rect.bottomRight()
            print(f"【DraggableRectItem】 top_left = {top_left}")
            print(f"【DraggableRectItem】 bottom_right = {bottom_right}")

            # 左上角范围
            lt_min_x = top_left.x() - SIDE_LENGTH / 2
            lt_max_x = top_left.x() + SIDE_LENGTH / 2
            print(f"【DraggableRectItem】 lt_min_x,lt_max_x = {lt_min_x}, {lt_max_x}")
            lt_min_y = top_left.y() - SIDE_LENGTH / 2
            lt_max_y = top_left.y() + SIDE_LENGTH / 2
            print(f"【DraggableRectItem】 lt_min_y,lt_max_y = {lt_min_y}, {lt_max_y}")

            # 右下角范围
            rb_min_x = bottom_right.x() - SIDE_LENGTH / 2
            rb_max_x = bottom_right.x() + SIDE_LENGTH / 2
            print(f"【DraggableRectItem】 rb_min_x,rb_max_x = {rb_min_x}, {rb_max_x}")
            rb_min_y = bottom_right.y() - SIDE_LENGTH / 2
            rb_max_y = bottom_right.y() + SIDE_LENGTH / 2
            print(f"【DraggableRectItem】 rb_min_y,rb_max_y = {rb_min_y}, {rb_max_y}")

            # Allow adjusting the top-left and bottom-right corners
            if (lt_min_x <= x <= lt_max_x) and (lt_min_y <= y <= lt_max_y):
                # 左上角
                self.active_vertex = "top_left"
                # self.end_x, self.end_y = rect.bottomRight().x(), rect.bottomRight().y()
                print("【DraggableRectItem】 top_left")
            elif (rb_min_x <= x <= rb_max_x) and (rb_min_y <= y <= rb_max_y):
                self.active_vertex = "bottom_right"
                # self.start_x, self.end_x = rect.topLeft().x(), rect.topLeft().y()
                print("【DraggableRectItem】 bottom_right")
            else:
                print("【DraggableRectItem】 else")
                self.active_vertex = None
                super().mousePressEvent(event)
            print(f"【DraggableRectItem】 【mousePressEvent】 【active_vertex:{self.active_vertex}】")
        except Exception as e:
            print(f"error: {e}")

    def mouseReleaseEvent(self, event):
        self.active_vertex = None
        super().mouseReleaseEvent(event)
        print(f"【DraggableRectItem】 【mouseReleaseEvent】 【active_vertex:{self.active_vertex}】")
        print("- " * 30)


class ImageViewer(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        # self.setDragMode(QGraphicsView.ScrollHandDrag)
        # self.setMouseTracking(True)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.viewport().setCursor(Qt.ArrowCursor)

        self.image_item = None
        self.current_item: DraggableRectItem = None
        self.start_x, self.start_y = None, None
        self.end_x, self.end_y = None, None
        self.pixmap = QPixmap()

        self.zoom_in_factor = 1.2
        self.zoom_out_factor = 0.8

        self._middle_button_pressed = False
        self._middle_button_last_pos = None

        self._fit_once = False

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Delete:
            print(f"【ImageViewer】----del")
            # self._alt_down = True
            items = self.get_all_rect_items()
            for item in items:
                if item.isSelected():
                    self.scene().removeItem(item)

    def load_image(self, image_path):
        self.pixmap = QPixmap(image_path)
        if not self.pixmap.isNull():
            self.scene().clear()
            self.image_item = self.scene().addPixmap(self.pixmap)
            self.setSceneRect(QRectF(self.pixmap.rect()))
            self.fitInView(self.image_item, Qt.KeepAspectRatio)

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

        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.NoDrag)
            if not self.current_item:
                # top_item = self.scene().itemAt(pos, self.transform())
                top_item = self.get_topmost_rect_item(pos)
                print(f"【ImageViewer】 【mousePressEvent top_item={top_item}")
                if top_item is self.image_item:
                    pos = self.mapToScene(event.pos())
                    self.start_x, self.start_y = pos.x(), pos.y()
                    self.current_item = DraggableRectItem(QRectF(self.start_x, self.start_y, 0, 0))
                    brush = QColor(255, 0, 0, 30)  # 红色填充，透明度为100
                    self.current_item.setBrush(brush)
                    pen = QPen(Qt.red, 5)
                    self.current_item.setPen(pen)
                    self.scene().addItem(self.current_item)

                    print("【ImageViewer】 【mousePressEvent】 画新的框------------")
        elif event.button() == Qt.MiddleButton:
            self.viewport().setCursor(Qt.OpenHandCursor)
            self._middle_button_last_pos = event.pos()
            self._middle_button_pressed = True

    def get_topmost_rect_item(self, scene_pos):
        all_items = self.scene().items()
        for item in all_items:
            if isinstance(item, DraggableRectItem):
                if item.contains(item.mapFromScene(scene_pos)):  # 判断item是否包含给定的点
                    return item

        if self.image_item and self.image_item.contains(scene_pos):
            return self.image_item

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
        x = point.x() - SIDE_LENGTH / 2
        y = point.y() - SIDE_LENGTH / 2

        item = QGraphicsRectItem(QRectF(x, y, SIDE_LENGTH, SIDE_LENGTH))
        brush = QColor(255, 0, 0, 255)  # 红色填充，透明度为100
        item.setBrush(brush)
        pen = QPen(Qt.red, 1)
        item.setPen(pen)
        self.scene().addItem(item)
        return item

    def mouseMoveEvent(self, event):
        try:
            super().mouseMoveEvent(event)
            pos = self.mapToScene(event.pos())
            if self.current_item:

                self.end_x, self.end_y = pos.x(), pos.y()
                self.current_item.setRect(
                    QRectF(self.start_x, self.start_y, self.end_x - self.start_x, self.end_y - self.start_y))

                self.draw_rect_points(self.current_item)

                if self.start_x < self.end_x:
                    x = self.start_x
                else:
                    x = self.end_x

                if self.start_y < self.end_y:
                    y = self.start_y
                else:
                    y = self.end_y
                w = abs(self.start_x - self.end_x)
                h = abs(self.start_y - self.end_y)
                self.current_item.setRect(QRectF(x, y, w, h))

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
        except Exception as e:
            print(f"error = {e}")

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
        self.viewport().setCursor(Qt.ArrowCursor)
        self.setDragMode(QGraphicsView.NoDrag)
        if event.button() == Qt.LeftButton:
            self.current_item = None
        elif event.button() == Qt.MiddleButton:
            self._middle_button_pressed = False

    def mouseDoubleClickEvent(self, event):
        print(f"【ImageViewer】 【self.verticalScrollBar().value()】 --------------- {self.verticalScrollBar().value()}")

    def wheelEvent(self, event):
        super().wheelEvent(event)
        # 滚轮缩放
        if event.angleDelta().y() > 0:
            self.scale(self.zoom_in_factor, self.zoom_in_factor)
        else:
            self.scale(self.zoom_out_factor, self.zoom_out_factor)

        print(f"self.pixmap.width()={self.pixmap.width()}, self.pixmap.height()={self.pixmap.height()}")
        print(f"self.get_rect_box()={self.get_rect_box()}")
        print(f"self.get_rect_points()={self.get_rect_points()}")
        print("= " * 30)

    def get_rect_box(self):
        """x,y,w,h"""
        if self.current_item:
            # rect = self.current_item.rect()
            rect = self.current_item.mapRectToItem(self.image_item, self.current_item.rect())
            x = rect.x()
            y = rect.y()
            w = rect.width()
            h = rect.height()
            return x, y, w, h

    def get_rect_points(self):
        """对角线上的两点坐标"""
        try:
            # if self.current_item:
            #     rect: QRectF = self.current_item.rect()
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
            self.scene().removeItem(item)


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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ImageViewer()

    try:
        # Load the image
        # image_path = "../../images/EL_TP3"  # Replace with the actual image file path
        # viewer.load_image(image_path)
        # Create a QWidget to hold the QGraphicsView
        # widget = QWidget()
        # layout = QVBoxLayout()
        # layout.addWidget(viewer)
        # widget.setLayout(layout)

        image_path = "../../images/EL_TP3"
        widget = MyWidget()
        widget.resize(1000, 600)
        widget.ui.viewer.load_image(image_path)
        widget.show()

        sys.exit(app.exec_())
    except Exception as e:
        print(f"error: {e}")
