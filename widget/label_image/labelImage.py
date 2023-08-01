# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt, QRectF


class ImageViewer(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setDragMode(QGraphicsView.ScrollHandDrag)  # 添加拖动功能

        self.image_item = None
        self.rect_item = None
        self.start_x, self.start_y = None, None
        self.end_x, self.end_y = None, None
        self.zoom_in_factor = 1.2
        self.zoom_out_factor = 0.8

    def load_image(self, image_path):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.scene().clear()
            self.image_item = self.scene().addPixmap(pixmap)
            self.setSceneRect(QRectF(pixmap.rect()))
            self.fitInView(self.image_item, Qt.KeepAspectRatio)

    def mousePressEvent(self, event):
        if not self.rect_item:
            pos = self.mapToScene(event.pos())
            self.start_x, self.start_y = pos.x(), pos.y()
            self.rect_item = QGraphicsRectItem(QRectF(self.start_x, self.start_y, 0, 0))
            pen = QPen(Qt.red, 10)  # Set the border color to red with a width of 2 pixels
            self.rect_item.setPen(pen)
            self.scene().addItem(self.rect_item)

    def mouseMoveEvent(self, event):
        if self.rect_item:
            pos = self.mapToScene(event.pos())
            self.end_x, self.end_y = pos.x(), pos.y()
            self.rect_item.setRect(
                QRectF(self.start_x, self.start_y, self.end_x - self.start_x, self.end_y - self.start_y))

    def mouseReleaseEvent(self, event):
        self.rect_item = None

    def wheelEvent(self, event):
        super().wheelEvent(event)
        # 滚轮缩放
        if event.angleDelta().y() > 0:
            self.scale(self.zoom_in_factor, self.zoom_in_factor)
        else:
            self.scale(self.zoom_out_factor, self.zoom_out_factor)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    viewer = ImageViewer()
    # Load the image
    image_path = "../../images/EL_TP3"  # Replace with the actual image file path
    viewer.load_image(image_path)

    # Create a QWidget to hold the QGraphicsView
    widget = QWidget()
    layout = QVBoxLayout()
    widget.setLayout(layout)
    layout.addWidget(viewer)
    widget.show()

    sys.exit(app.exec_())
