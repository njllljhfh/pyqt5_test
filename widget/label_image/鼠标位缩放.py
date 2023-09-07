# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt


class ImageViewer(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QPainter.Antialiasing)  # 启用抗锯齿渲染
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)  # 鼠标位置缩放
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setMouseTracking(True)
        self.setScene(scene)

        self._fit_once = False

    def wheelEvent(self, event):
        # 获取鼠标位置（在视图坐标中）
        # mouse_point = event.pos()

        # 将鼠标位置转换为场景坐标
        # scene_point = self.mapToScene(mouse_point)

        # 获取当前的缩放因子
        # current_scale = self.transform().m22()

        # 根据鼠标滚轮方向计算缩放因子的变化
        if event.angleDelta().y() > 0:
            zoom_factor = 1.2  # 放大
        else:
            zoom_factor = 0.8  # 缩小

        # 计算新的缩放因子
        # new_scale = current_scale * zoom_factor

        # 设置新的缩放因子
        # self.setTransform(self.transform().scale(zoom_factor, zoom_factor), False)
        self.scale(zoom_factor, zoom_factor)

        # 将视图的中心点设置为鼠标位置
        # self.centerOn(scene_point)

    def fit_in_view(self):
        self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self._fit_once:
            self.fit_in_view()
            self._fit_once = True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    scene = QGraphicsScene()
    viewer = ImageViewer(scene)

    # 添加一个图像项
    # pixmap = QPixmap("../../images/EL_TP3.jpg")  # 替换为你的图像文件路径
    # pixmap_item = QGraphicsPixmapItem(pixmap)
    # scene.addItem(pixmap_item)

    pixmap = QPixmap("../../images/EL_TP3.jpg")  # 替换为你的图像文件路径
    pixmap_item = scene.addPixmap(pixmap)

    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.addWidget(viewer)
    widget.setLayout(layout)
    widget.resize(1600, 900)
    widget.show()

    sys.exit(app.exec_())
