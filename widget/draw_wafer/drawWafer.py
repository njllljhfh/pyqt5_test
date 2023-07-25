import sys
from enum import unique, Enum

from PyQt5.QtGui import QPainter, QMouseEvent
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QWidget, QVBoxLayout, \
    QHBoxLayout, QButtonGroup, QRadioButton, QLabel, QAbstractButton
from PyQt5.QtCore import Qt, pyqtSignal, QSize


@unique
class PositionType(Enum):
    blank = 0
    bk = 1
    ok = 2
    ng = 3

    @classmethod
    def value_name(cls, value):
        """ Map value to Str. """
        value_map = {
            cls.blank.value: "空白",
            cls.bk.value: "背景",
            cls.ok.value: "OK",
            cls.ng.value: "NG",
        }
        return value_map.get(value)

    @classmethod
    def value_exists(cls, value):
        """
        Determine whether the value is in class.
        :param value: The value of enumerate class.  <type: int>
        :return: True or False.  <type: bool>
        """
        if value in [member.value for member in cls.__members__.values()]:
            return True
        else:
            return False

    @classmethod
    def value_list(cls):
        """
        Get value list.
        :return: Value list.  <type: list>
        """

        return [member.value for member in cls.__members__.values()]


class RatioBtnGroup(QWidget):
    """Two ration button widget."""
    # Signal of clicking one ration button of button group.
    signal_btn_group_button_clicked = pyqtSignal(QAbstractButton)

    def __init__(self, *args, parent=None, label_name="名称：", text_btn_a: str = "a", text_btn_b: str = "b",
                 alignment=Qt.AlignRight | Qt.AlignVCenter):
        super().__init__(parent, *args)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        # Label
        self.label = QLabel(parent)
        self.label.setObjectName("label")
        self.label.setText(label_name or "名称：")
        self.label.setAlignment(alignment)
        layout.addWidget(self.label)
        # RadioButton
        self.btn_a = QRadioButton(parent)
        self.btn_a.setObjectName("btn_a")
        self.btn_a.setText(text_btn_a or "a")
        layout.addWidget(self.btn_a)
        # RadioButton
        self.btn_b = QRadioButton(parent)
        self.btn_b.setObjectName("btn_b")
        self.btn_b.setText(text_btn_b or "b")
        self.btn_b.setChecked(True)
        layout.addWidget(self.btn_b)

        # ButtonGroup
        self.btn_group = QButtonGroup(parent)
        self.btn_group.setObjectName("btn_group")
        self.btn_group.addButton(self.btn_a)
        self.btn_group.addButton(self.btn_b)

        self.btn_group.buttonClicked.connect(self.signal_btn_group_button_clicked)


class FourRationBtnGroup(RatioBtnGroup):
    """Four ration button widget."""

    def __init__(self, *args, parent=None, label_name="名称：",
                 text_btn_a: str = "a", text_btn_b: str = "b", text_btn_c: str = "c", text_btn_d: str = "d",
                 alignment=Qt.AlignRight | Qt.AlignVCenter):
        super().__init__(*args, parent=parent, label_name=label_name,
                         text_btn_a=text_btn_a, text_btn_b=text_btn_b,
                         alignment=alignment)
        self.btn_c = QRadioButton(parent)
        self.btn_c.setObjectName("btn_c")
        self.btn_c.setText(text_btn_c or "c")
        self.layout().addWidget(self.btn_c)
        self.btn_group.addButton(self.btn_c)

        self.btn_d = QRadioButton(parent)
        self.btn_d.setObjectName("btn_d")
        self.btn_d.setText(text_btn_d or "d")
        self.layout().addWidget(self.btn_d)
        self.btn_group.addButton(self.btn_d)


class ColorGridWidget(QGraphicsView):
    signal_rect_item_clicked = pyqtSignal(int, int)  # row, col

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.grid_array = []
        self.grid_size = 20  # 每个方格的大小
        self.zoom_in_factor = 1.2
        self.zoom_out_factor = 0.8
        self.rows = 0
        self.cols = 0
        self.x_max = 0
        self.y_max = 0
        self.rect_item_map = {}

        self._drag_start_pos = None

        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setDragMode(QGraphicsView.ScrollHandDrag)  # 添加拖动功能
        self.setBackgroundBrush(Qt.darkGray)
        self.viewport().setCursor(Qt.ArrowCursor)

    def update_grid(self, grid_array):
        self.scene().clear()
        self.rect_item_map.clear()

        self.grid_array = grid_array
        self.rows = len(grid_array)
        self.cols = len(grid_array[0])
        self.x_max = self.cols * self.grid_size
        self.y_max = self.rows * self.grid_size

        for row in range(self.rows):
            for col in range(self.cols):
                value = self.grid_array[row][col]
                color = self.get_color_from_value(value)
                rect_item = QGraphicsRectItem(col * self.grid_size, row * self.grid_size,
                                              self.grid_size, self.grid_size)
                rect_item.row = row
                rect_item.col = col
                rect_item.setBrush(color)
                self.scene().addItem(rect_item)
                self.rect_item_map[(row, col)] = rect_item

    def update_one_grid(self, row, col, pos_type):
        rect_item = self.rect_item_map[(row, col)]
        self.grid_array[row][col] = pos_type
        color = self.get_color_from_value(pos_type)
        rect_item.setBrush(color)

    @classmethod
    def get_color_from_value(cls, pos_type):
        if pos_type == PositionType.blank.value:
            # 空白
            return Qt.white
        elif pos_type == PositionType.bk.value:
            # 背景
            return Qt.blue
        elif pos_type == PositionType.ok.value:
            # OK
            return Qt.green
        elif pos_type == PositionType.ng.value:
            # NG
            return Qt.red
        else:
            # 未知
            return Qt.yellow

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self._drag_start_pos = event.pos()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.viewport().setCursor(Qt.ArrowCursor)

        try:
            if event.button() == Qt.LeftButton:
                if self._drag_start_pos is not None:
                    drag_distance = (event.pos() - self._drag_start_pos).manhattanLength()
                    if drag_distance < 3:  # 设置拖动的阈值，可以根据实际情况调整
                        # print("左键单击")
                        scene_pos = self.mapToScene(event.pos())
                        # print(f"scene_pos.x()={scene_pos.x()}, scene_pos.y()={scene_pos.y()}")
                        # print(f"self.x_max={self.x_max}, self.y_max={self.y_max}")
                        if 0 <= scene_pos.x() <= self.x_max and 0 <= scene_pos.y() <= self.y_max:
                            row = int(scene_pos.y() / self.grid_size)
                            col = int(scene_pos.x() / self.grid_size)
                            print("左键点击位置: ({}, {})".format(row, col))
                            self.signal_rect_item_clicked.emit(row, col)
                    else:
                        # print("非左键单击")
                        pass

                    self._drag_start_pos = None
        except Exception as e:
            print(e)

    def wheelEvent(self, event):
        super().wheelEvent(event)
        # 滚轮缩放
        if event.angleDelta().y() > 0:
            self.scale(self.zoom_in_factor, self.zoom_in_factor)
        else:
            self.scale(self.zoom_out_factor, self.zoom_out_factor)

    def __del__(self):
        print(f'self.grid_array={self.grid_array}')


class Ui(object):

    def __init__(self, parent=None):
        layout = QVBoxLayout(parent)

        h_layout1 = QHBoxLayout(parent)
        h_layout1.addStretch(1)
        self.ratio_btn_group = FourRationBtnGroup(parent=parent, label_name="类型：",
                                                  text_btn_a="OK", text_btn_b="NG",
                                                  text_btn_c="背景", text_btn_d="空白")
        self.ratio_btn_group.label.setFixedSize(QSize(40, 20))
        self.ratio_btn_group.btn_a.setFixedSize(QSize(60, 20))
        self.ratio_btn_group.btn_b.setFixedSize(QSize(60, 20))
        self.ratio_btn_group.btn_c.setFixedSize(QSize(60, 20))
        self.ratio_btn_group.btn_d.setFixedSize(QSize(60, 20))
        h_layout1.addWidget(self.ratio_btn_group)
        h_layout1.addStretch(1)
        layout.addLayout(h_layout1)

        self.wafer_canvas = ColorGridWidget(parent=parent)
        layout.addWidget(self.wafer_canvas)


class MyWidget(QWidget):

    def __init__(self, grid_array, *args, parent=None, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.ui = Ui(parent=self)
        self.ui.wafer_canvas.update_grid(grid_array)

        self._bind_event()

    def _bind_event(self):
        self.ui.wafer_canvas.signal_rect_item_clicked.connect(self.update_die_data)

    def update_die_data(self, row, col):
        try:
            btn = self.ui.ratio_btn_group.btn_group.checkedButton()
            btn_text = btn.text()
            if btn_text == 'OK':
                pos_type = PositionType.ok.value
            elif btn_text == 'NG':
                pos_type = PositionType.ng.value
            elif btn_text == '背景':
                pos_type = PositionType.bk.value
            else:
                pos_type = PositionType.blank.value
            print(f"位置的类型: {PositionType.value_name(pos_type)}")
            self.ui.wafer_canvas.update_one_grid(row, col, pos_type)
            print("= " * 30)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    # 示例二维数组
    # array = [
    #     [1, 2, 1, 0],
    #     [0, 1, 2, 1],
    #     [2, 0, 1, 2]
    # ]
    # - - -

    array = [
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 2, 1, 1, 0],
        [1, 1, 1, 2, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 3, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 3, 1, 1, 0],
        [0, 0, 1, 3, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
    ]
    # - - -

    # from copy import copy
    #
    # l_0 = [0] * 100
    # print(l_0)
    # l = [2] * 100
    # l[0] = 0
    # l[-1] = 0
    # array = [copy(l) for i in range(100)]
    # array[0] = copy(l_0)
    # array[-1] = copy(l_0)
    # - - -

    # app = QApplication(sys.argv)
    #
    # grid_widget = ColorGridWidget(array)
    # widget = QWidget()  # 使用 QVBoxLayout 将 QGraphicsView 放入 QWidget 中
    # layout = QVBoxLayout()
    # layout.addWidget(grid_widget)
    # widget.setLayout(layout)
    # widget.show()
    #
    # sys.exit(app.exec_())

    app = QApplication(sys.argv)

    widget = MyWidget(array)
    widget.resize(500, 500)
    widget.show()

    sys.exit(app.exec_())
