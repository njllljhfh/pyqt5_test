import sys
from typing import Dict

from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QWidget, QVBoxLayout, \
    QHBoxLayout, QPushButton, QGridLayout, QFrame, QFileDialog, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QPen, QPainter, QMouseEvent, QColor, QKeyEvent
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QPointF


class LabelRectItem(QGraphicsRectItem):

    def __init__(self, rect: QRectF):
        super().__init__(rect)
        self.setFlags(QGraphicsRectItem.ItemIsSelectable)
        self.active_vertex = None


class ImageViewer(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.viewport().setCursor(Qt.ArrowCursor)

        self.image_item = None
        self.current_item = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.pixmap = QPixmap()

        self.zoom_in_factor = 1.3
        self.zoom_out_factor = 0.8

        self._middle_button_pressed = False
        self._middle_button_last_pos = None

        self.side_length = 150

        self._fit_once = False  # 是否已经自适应窗口大小 1 次
        self._allow_adjust = True  # 是否允许调整矩形大小
        # self._label_max_num = float('inf')  # 无穷
        self._label_max_num = 1

        self.side_ratio = 0.06  # 角点可捕获的像素与图像长边的比

        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def load_image(self, image_path):
        self.pixmap = QPixmap(image_path)
        if not self.pixmap.isNull():
            self.side_length = int(max([self.pixmap.width(), self.pixmap.height()]) * self.side_ratio)
            self.scene().clear()
            self.image_item = self.scene().addPixmap(self.pixmap)
            self.setSceneRect(QRectF(self.pixmap.rect()))
            self.fitInView(self.image_item, Qt.KeepAspectRatio)

    def fit_in_view(self):
        if self.image_item:
            self.fitInView(self.image_item, Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.image_item and not self._fit_once:
            self.fitInView(self.image_item, Qt.KeepAspectRatio)
            self._fit_once = True

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Delete:
            items = self._get_all_rect_items()
            for item in items:
                if item.isSelected():
                    self._delete_rect(item)
        if event.key() == Qt.Key_F:
            self.fit_in_view()

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        pos = self.mapToScene(event.pos())
        x = pos.x()
        y = pos.y()
        # print(f"【ImageViewer】 【mousePressEvent】 event.x()={event.x()}, event.y()={event.y()}")
        print(f"【ImageViewer】 【mousePressEvent】 x={x}, y={y}")

        try:
            if event.button() == Qt.LeftButton:
                self.setDragMode(QGraphicsView.NoDrag)
                if self.image_item:
                    if not self.current_item:
                        top_item = self.get_topmost_item(pos)
                        # print(f"【ImageViewer】 【mousePressEvent】 top_item={top_item}")
                        # if top_item is self.image_item:
                        if top_item is self.image_item and (len(self._get_all_rect_items()) < self._label_max_num):
                            self.start_x, self.start_y = pos.x(), pos.y()
                            self.current_item = LabelRectItem(QRectF(self.start_x, self.start_y, 0, 0))
                            brush = QColor(255, 0, 0, 30)  # 红色填充，透明度为100
                            self.current_item.setBrush(brush)
                            pen = QPen(Qt.red, 5)
                            self.current_item.setPen(pen)
                            # self.scene().addItem(self.current_item)
                            # print("【ImageViewer】 【mousePressEvent】 画新的框------------")
                        elif isinstance(top_item, LabelRectItem):
                            x, y = pos.x(), pos.y()
                            # print(f"【ImageViewer】 【mousePressEvent】 x,y = {x}, {y}")

                            rect = top_item.rect()
                            top_left = rect.topLeft()
                            bottom_right = rect.bottomRight()
                            # print(f"【ImageViewer】 【mousePressEvent】 top_left = {top_left}")
                            # print(f"【ImageViewer】 【mousePressEvent】 bottom_right = {bottom_right}")

                            # 左上角范围
                            lt_min_x = top_left.x() - self.side_length / 2
                            lt_max_x = top_left.x() + self.side_length / 2
                            # print(f"【ImageViewer】 【mousePressEvent】 lt_min_x,lt_max_x = {lt_min_x}, {lt_max_x}")
                            lt_min_y = top_left.y() - self.side_length / 2
                            lt_max_y = top_left.y() + self.side_length / 2
                            # print(f"【ImageViewer】 【mousePressEvent】 lt_min_y,lt_max_y = {lt_min_y}, {lt_max_y}")

                            # 右下角范围
                            rb_min_x = bottom_right.x() - self.side_length / 2
                            rb_max_x = bottom_right.x() + self.side_length / 2
                            # print(f"【ImageViewer】 【mousePressEvent】 rb_min_x,rb_max_x = {rb_min_x}, {rb_max_x}")
                            rb_min_y = bottom_right.y() - self.side_length / 2
                            rb_max_y = bottom_right.y() + self.side_length / 2
                            # print(f"【ImageViewer】 【mousePressEvent】 rb_min_y,rb_max_y = {rb_min_y}, {rb_max_y}")

                            # Allow adjusting the top-left and bottom-right corners
                            if (lt_min_x <= x <= lt_max_x) and (lt_min_y <= y <= lt_max_y):
                                # 左上角
                                top_item.active_vertex = "top_left"
                                # print("【ImageViewer】 【mousePressEvent】 top_left")
                            elif (rb_min_x <= x <= rb_max_x) and (rb_min_y <= y <= rb_max_y):
                                top_item.active_vertex = "bottom_right"
                                # print("【ImageViewer】 【mousePressEvent】 bottom_right")
                            else:
                                # print("【ImageViewer】 【mousePressEvent】 move")
                                self.start_x, self.start_y = pos.x(), pos.y()
                                top_item.active_vertex = 'move'
                            # print(f"【ImageViewer】 【mousePressEvent】 active_vertex={top_item.active_vertex}】")
                            self.current_item = top_item
            elif event.button() == Qt.MiddleButton:
                self.viewport().setCursor(Qt.OpenHandCursor)
                self._middle_button_last_pos = event.pos()
                self._middle_button_pressed = True
        except Exception as e:
            print(f"error: {e}")
            raise e

    def mouseMoveEvent(self, event: QMouseEvent):
        try:
            super().mouseMoveEvent(event)
            pos = self.mapToScene(event.pos())
            x, y = pos.x(), pos.y()
            if self.current_item:
                print(f"self.current_item = {self.current_item}")
                x_min = 0
                y_min = 0
                image_width = self.image_item.boundingRect().width()
                image_height = self.image_item.boundingRect().height()
                if self.current_item.active_vertex and self._allow_adjust:

                    rect = self.current_item.rect()
                    item_x_old = rect.x()
                    item_y_old = rect.y()
                    item_w_old = rect.width()
                    item_h_old = rect.height()

                    if self.current_item.active_vertex == "top_left":
                        x_max = image_width
                        y_max = image_height

                        x, y = self.get_valid_x_y(x, y, x_min, x_max, y_min, y_max)

                        w = (item_x_old + item_w_old) - x
                        h = (item_y_old + item_h_old) - y
                        self.current_item.setRect(QRectF(x, y, w, h))
                    elif self.current_item.active_vertex == "bottom_right":
                        x_max = image_width
                        y_max = image_height

                        x, y = self.get_valid_x_y(x, y, x_min, x_max, y_min, y_max)

                        w = x - item_x_old
                        h = y - item_y_old
                        self.current_item.setRect(QRectF(item_x_old, item_y_old, w, h))
                    elif self.current_item.active_vertex == "move":
                        x_max = image_width - item_w_old
                        y_max = image_height - item_h_old

                        x_move = (x - self.start_x)
                        y_move = (y - self.start_y)

                        x = item_x_old + x_move
                        y = item_y_old + y_move

                        x, y = self.get_valid_x_y(x, y, x_min, x_max, y_min, y_max)
                        self.current_item.setRect(QRectF(x, y, item_w_old, item_h_old))

                        self.start_x = pos.x()
                        self.start_y = pos.y()
                elif self.current_item.active_vertex is None:
                    x_max = image_width
                    y_max = image_height
                    drag_distance = (pos - QPointF(self.start_x, self.start_y)).manhattanLength()
                    if drag_distance > 3:
                        self.scene().addItem(self.current_item)
                        self.end_x, self.end_y = x, y
                        self.end_x, self.end_y = self.get_valid_x_y(x, y, x_min, x_max, y_min, y_max)
                        self.current_item.setRect(
                            QRectF(self.start_x, self.start_y, self.end_x - self.start_x, self.end_y - self.start_y))

                        # 将矩形转换为从左上角，到右下角绘制
                        rect = self.current_item.rect()
                        tl_x = rect.x()
                        tl_y = rect.y()
                        br_x = rect.x() + rect.width()
                        br_y = rect.y() + rect.height()
                        x = tl_x if tl_x < br_x else br_x
                        y = tl_y if tl_y < br_y else br_y
                        w = abs(rect.width())
                        h = abs(rect.height())
                        self.current_item.setRect(QRectF(x, y, w, h))

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
            self.start_x = None
            self.start_y = None
            self.end_x = None
            self.end_y = None
        elif event.button() == Qt.MiddleButton:
            self._middle_button_pressed = False

    def wheelEvent(self, event):
        super().wheelEvent(event)

        # 滚轮缩放
        if event.angleDelta().y() > 0:
            self.scale(self.zoom_in_factor, self.zoom_in_factor)
        else:
            self.scale(self.zoom_out_factor, self.zoom_out_factor)

        # print(f"图像pixmap宽度={self.pixmap.width()}, 图像pixmap高度={self.pixmap.height()}")
        # print(f"self.get_all_rect_boxes()={self.get_all_rect_boxes()}")
        # print(f"self.get_all_rect_points()={self.get_all_rect_points()}")
        # print("= " * 30)

    def get_topmost_item(self, scene_pos):
        all_items = self.scene().items()
        for item in all_items:
            if isinstance(item, LabelRectItem):
                # if item.contains(item.mapFromScene(scene_pos)):
                if item.contains(scene_pos):
                    return item

        if self.image_item and self.image_item.contains(scene_pos):
            return self.image_item

    @staticmethod
    def get_valid_x_y(x, y, x_min, x_max, y_min, y_max):
        if x < x_min:
            x = x_min
        elif x > x_max:
            x = x_max
        if y < y_min:
            y = y_min
        elif y > y_max:
            y = y_max
        return x, y

    def _get_all_rect_items(self):
        # 获取场景中的全部矩形项
        all_items = self.scene().items()
        rect_items = [item for item in all_items if isinstance(item, LabelRectItem)]
        return rect_items

    def _delete_rect(self, item):
        self.scene().removeItem(item)

    def get_all_rect_boxes(self):
        """全部矩形的 x,y,w,h"""
        ls = []
        for item in self._get_all_rect_items():
            rect = item.mapRectToItem(self.image_item, item.rect())
            x = rect.x()
            y = rect.y()
            w = rect.width()
            h = rect.height()
            ls.append([x, y, w, h])
        print(f"全部矩形的 box数据(x,y,w,h)={ls}")
        return ls

    def get_all_rect_points(self):
        """全部矩形的对角线上的两点坐标(左上、右下)"""
        ls = []
        for item in self._get_all_rect_items():
            rect = item.mapRectToItem(self.image_item, item.rect())
            tl = rect.topLeft()
            br = rect.bottomRight()
            ls.append([[tl.x(), tl.y()], [br.x(), br.y()]])
        print(f"全部矩形的顶点数据(左上、右下)={ls}")
        return ls

    def clear_all_rect(self):
        rect_items = self._get_all_rect_items()
        for item in rect_items:
            self._delete_rect(item)


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


class ImageLabelComponent(QFrame):
    """图像标注组件"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        layout_1 = QHBoxLayout()
        # layout_1.setSpacing(0)
        layout_1.setContentsMargins(0, 0, 0, 0)

        self.get_all_rect_points_btn = QPushButton(parent)
        self.get_all_rect_points_btn.setText("获取矩形点")
        layout_1.addWidget(self.get_all_rect_points_btn)

        self.get_all_rect_boxes_btn = QPushButton(parent)
        self.get_all_rect_boxes_btn.setText("获取矩形box")
        layout_1.addWidget(self.get_all_rect_boxes_btn)

        self.del_all_btn = QPushButton(parent)
        self.del_all_btn.setText("删除全部")
        layout_1.addWidget(self.del_all_btn)

        layout.addLayout(layout_1)

        self.viewer = ImageViewer(parent)
        layout.addWidget(self.viewer)

        self.get_all_rect_points_btn.clicked.connect(self.viewer.get_all_rect_points)
        self.get_all_rect_boxes_btn.clicked.connect(self.viewer.get_all_rect_boxes)
        self.del_all_btn.clicked.connect(self.viewer.clear_all_rect)


class ImageLabelGroup(QFrame):

    def __init__(self, label_component_num, column_num, parent=None):
        super().__init__()
        layout = QGridLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label_components: Dict[tuple:ImageLabelComponent] = dict()

        for i in range(label_component_num):
            row = int(i / column_num)
            col = i % column_num
            label_component = ImageLabelComponent(parent=parent)
            layout.addWidget(label_component, row, col, 1, 1)
            self.label_components[(row, col)] = label_component


class UploadBtn(QPushButton):
    signal_file_path_ls = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setText("上传图像文件")
        self.clicked.connect(self.upload_file)

    def upload_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        image_formats = "Image Files (*.png *.jpg *.bmp *.gif);;All Files (*)"
        file_path_ls, _ = QFileDialog.getOpenFileNames(self, "上传图像文件", "", image_formats, options=options)
        file_path_ls.sort()

        if file_path_ls:
            print("已选择的文件:")
            for file_path in file_path_ls:
                print(file_path)
            self.signal_file_path_ls.emit(file_path_ls)


class ImageLabelUi(object):

    def __init__(self, parent, label_component_num, column_num):
        layout = QGridLayout(parent)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.upload_btn = UploadBtn(parent=parent)

        layout.addWidget(self.upload_btn, 0, 0, 1, 1)

        self.image_label_group = ImageLabelGroup(label_component_num, column_num, parent=parent)
        layout.addWidget(self.image_label_group, 1, 0, 1, 1)


class ImageLabelPage(QWidget):

    def __init__(self, label_component_num, *args, parent=None, column_num=4):
        super().__init__(parent, *args)

        self.ui = ImageLabelUi(self, label_component_num, column_num)

        self.label_component_num = label_component_num
        self.column_num = column_num

        self._bind_event()

    def _bind_event(self):
        self.ui.upload_btn.signal_file_path_ls.connect(self.load_image_from_path)

    def load_image_from_path(self, image_path_ls):
        for i, image_path in enumerate(image_path_ls):
            row = int(i / self.column_num)
            col = i % self.column_num
            if (row, col) in self.ui.image_label_group.label_components:
                label_component = self.ui.image_label_group.label_components[(row, col)]
                label_component.viewer.load_image(image_path)

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)
        if event.modifiers() == Qt.ShiftModifier and event.key() == Qt.Key_F:
            for label_component in self.ui.image_label_group.label_components.values():
                label_component.viewer.fit_in_view()

        # if event.key() == Qt.Key_F:
        #     items = self._get_all_rect_items()
        #     for item in items:
        #         if item.isSelected():
        #             self._delete_rect(item)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # image_path_el = "./images/EL_362307271161687_1_1.jpg"

    # widget = MyWidget()
    # widget.resize(1000, 600)
    # widget.ui.viewer.load_image(image_path_el)

    num = 12
    col_num = 4
    widget = ImageLabelPage(num, column_num=col_num)
    widget.resize(1900, 1000)
    # widget.resize(1900, 350)
    # widget.load_image(image_path_el)
    # image_paths = [
    #     "./images/EL_362307271161687_1_1.jpg",
    #     "./images/EL_362307271161687_1_2.jpg",
    #     "./images/EL_362307271161687_1_3.jpg",
    #     "./images/EL_362307271161687_1_4.jpg",
    #     "./images/EL_362307271161687_2_1.jpg",
    #     "./images/EL_362307271161687_2_2.jpg",
    #     "./images/EL_362307271161687_2_3.jpg",
    #     "./images/EL_362307271161687_2_4.jpg",
    #     "./images/EL_362307271161687_3_1.jpg",
    #     "./images/EL_362307271161687_3_2.jpg",
    #     "./images/EL_362307271161687_3_3.jpg",
    #     "./images/EL_362307271161687_3_4.jpg",
    # ]
    # widget.load_image_from_path(image_paths)

    widget.show()

    sys.exit(app.exec_())
