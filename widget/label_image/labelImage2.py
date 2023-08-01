# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap, QPen, QPainter, QMouseEvent, QColor
from PyQt5.QtCore import Qt, QRectF


class ImageViewer(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setMouseTracking(True)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.viewport().setCursor(Qt.ArrowCursor)

        self.image_item = None
        self.rect_item = None
        self.start_x, self.start_y = None, None
        self.end_x, self.end_y = None, None
        self.pixmap = QPixmap()

        self.zoom_in_factor = 1.2
        self.zoom_out_factor = 0.8

        self.active_vertex = ''
        self.rect_item_complete = True
        self.half_side = 25

    def load_image(self, image_path):
        self.pixmap = QPixmap(image_path)
        if not self.pixmap.isNull():
            self.scene().clear()
            self.image_item = self.scene().addPixmap(self.pixmap)
            self.setSceneRect(QRectF(self.pixmap.rect()))
            self.fitInView(self.image_item, Qt.KeepAspectRatio)

            # 加载图像时画个框
            # rect_item = QGraphicsRectItem(QRectF(100, 100, 500, 300))
            # pen = QPen(Qt.red, 5)
            # rect_item.setPen(pen)
            # self.scene().addItem(rect_item)

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)

        if not self.rect_item:
            self.rect_item_complete = False
            pos = self.mapToScene(event.pos())
            self.start_x, self.start_y = pos.x(), pos.y()
            self.rect_item = QGraphicsRectItem(QRectF(self.start_x, self.start_y, 0, 0))
            brush = QColor(255, 0, 0, 30)  # 红色填充，透明度为100
            self.rect_item.setBrush(brush)
            pen = QPen(Qt.red, 5)
            self.rect_item.setPen(pen)
            self.scene().addItem(self.rect_item)
            print("mousePressEvent------------111")
        else:
            self.rect_item_complete = True
            self.active_vertex = ''

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        pos = self.mapToScene(event.pos())
        if self.rect_item:
            if self.rect_item_complete is False:
                if self.active_vertex == '' or self.active_vertex == "bottom_right":
                    self.end_x, self.end_y = pos.x(), pos.y()
                    self.rect_item.setRect(
                        QRectF(self.start_x, self.start_y, self.end_x - self.start_x, self.end_y - self.start_y))
                elif self.active_vertex == "left_top":
                    self.start_x, self.start_y = pos.x(), pos.y()
                    self.rect_item.setRect(
                        QRectF(self.start_x, self.start_y, self.end_x - self.start_x, self.end_y - self.start_y))
                print(f"mouseMoveEvent------------ self.active_vertex={self.active_vertex}")

        self.repaint()

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
        self.viewport().setCursor(Qt.ArrowCursor)

    def mouseDoubleClickEvent(self, event):
        if self.rect_item:
            print(f"mouseDoubleClickEvent --------------- rect_item")
            pos = self.mapToScene(event.pos())
            x, y = pos.x(), pos.y()
            rect = self.rect_item.rect()

            # 左上角范围
            lt_min_x = rect.topLeft().x() - self.half_side
            lt_max_x = rect.topLeft().x() + self.half_side
            lt_min_y = rect.topLeft().y() - self.half_side
            lt_max_y = rect.topLeft().y() + self.half_side

            # 右下角范围
            rb_min_x = rect.bottomRight().x() - self.half_side
            rb_max_x = rect.bottomRight().x() + self.half_side
            rb_min_y = rect.bottomRight().y() - self.half_side
            rb_max_y = rect.bottomRight().y() + self.half_side

            # Allow adjusting the top-left and bottom-right corners
            if (lt_min_x <= x <= lt_max_x) and (lt_min_y <= y <= lt_max_y):
                # 左上角
                print(f"rect.bottomRight()={rect.bottomRight()}")
                self.active_vertex = "left_top"
                self.end_x, self.end_y = rect.bottomRight().x(), rect.bottomRight().y()
                self.rect_item_complete = False
            elif (rb_min_x <= x <= rb_max_x) and (rb_min_y <= y <= rb_max_y):
                self.active_vertex = "bottom_right"
                self.start_x, self.end_x = rect.topLeft().x(), rect.topLeft().y()
                self.rect_item_complete = False
            else:
                self.rect_item_complete = True
                self.active_vertex = ''
            print(f"mouseDoubleClickEvent --------------- {self.active_vertex}")

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

    # def get_rect_in_pixmap(self):
    #     # 获取在pixmap中的矩形框坐标和大小
    #     if self.rect_item:
    #         rect = self.rect_item.rect()
    #         transform = self.transform()
    #         inv_transform = transform.inverted()[0]
    #         rect_in_pixmap = inv_transform.mapRect(rect)
    #         return rect_in_pixmap
    #
    # def get_rect_in_pixmap(self):
    #     # 获取在pixmap中的矩形框坐标和大小
    #     if self.rect_item:
    #         rect = self.rect_item.rect()
    #         pixmap_rect = self.image_item.boundingRect()
    #         print(f"pixmap_rect={pixmap_rect}")
    #         pixmap = self.image_item.pixmap()
    #         pixmap_width, pixmap_height = pixmap.width(), pixmap.height()
    #         print(f"pixmap_width={pixmap_width}, pixmap_height={pixmap_height}")
    #         scene_width, scene_height = pixmap_rect.width(), pixmap_rect.height()
    #         print(f"scene_width={scene_width}, scene_height={scene_height}")
    #         x_ratio, y_ratio = pixmap_width / scene_width, pixmap_height / scene_height
    #
    #         x = rect.x() * x_ratio
    #         y = rect.y() * y_ratio
    #         w = rect.width() * x_ratio
    #         h = rect.height() * y_ratio
    #
    #         return x, y, w, h
    # def get_rect_in_pixmap(self):
    #     # 获取在pixmap中的矩形框坐标和大小
    #     if self.rect_item:
    #         rect = self.rect_item.mapRectToItem(self.image_item, self.rect_item.rect())
    #         return rect.x(), rect.y(), rect.width(), rect.height()

    def get_rect_box(self):
        # 获取在pixmap中的矩形框坐标和大小
        if self.rect_item:
            rect = self.rect_item.rect()
            x = rect.x()
            y = rect.y()
            w = rect.width()
            h = rect.height()
            return x, y, w, h

    def get_rect_points(self):
        if self.rect_item:
            rect: QRectF = self.rect_item.rect()
            lt = rect.topLeft()
            rb = rect.bottomRight()
            return [[lt.x(), lt.y()], [rb.x(), rb.y()]]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ImageViewer()

    # Load the image
    image_path = "../../images/EL_TP3"  # Replace with the actual image file path
    viewer.load_image(image_path)

    # Create a QWidget to hold the QGraphicsView
    widget = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(viewer)
    widget.setLayout(layout)
    widget.show()

    sys.exit(app.exec_())
