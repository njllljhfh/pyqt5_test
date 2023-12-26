# -*- coding:utf-8 -*-
import sys
from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette, QIcon
from PyQt5.QtWidgets import QWidget, QColorDialog, QApplication, QVBoxLayout, QPushButton, QLabel, QLineEdit, \
    QHBoxLayout, QSizePolicy

qss = """
QWidget {
    color: rgb(255, 255, 255);
    background-color: rgb(69, 67, 91);
    font-size: 14px;
    font-family: sans-serif;
}

QPushButton {
    color: rgb(0, 0, 0);
    background-color: rgb(217,202,230);
}

QLabel {
    min-height: 20px;
    min-width: 120px;
}

QLineEdit {
    min-height: 20px;
}
"""


# 自定义的QWidget例子
class ExampleWidget(QWidget):
    """例子"""

    def __init__(self, parent=None, *args):
        super().__init__(parent, *args)
        layout = QVBoxLayout(self)

        layout_rgba = QHBoxLayout()
        self.color_rgba_lab = QLabel()
        self.color_rgba_lab.setText("10进制（RGBA）: ")
        self.color_rgba_lab.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout_rgba.addWidget(self.color_rgba_lab)
        self.color_rgba_line_edit = QLineEdit()
        self.color_rgba_line_edit.setReadOnly(True)
        layout_rgba.addWidget(self.color_rgba_line_edit)
        layout.addLayout(layout_rgba)

        layout_rgba_hexadecimal = QHBoxLayout()
        self.color_rgba_hexadecimal_lab = QLabel()
        self.color_rgba_hexadecimal_lab.setText("16进制（RGBA）: ")
        self.color_rgba_hexadecimal_lab.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout_rgba_hexadecimal.addWidget(self.color_rgba_hexadecimal_lab)
        self.color_rgba_hexadecimal_line_edit = QLineEdit()
        self.color_rgba_hexadecimal_line_edit.setReadOnly(True)
        layout_rgba_hexadecimal.addWidget(self.color_rgba_hexadecimal_line_edit)
        layout.addLayout(layout_rgba_hexadecimal)

        layout_color_value = QHBoxLayout()
        self.color_value_lab = QLabel()
        self.color_value_lab.setText("颜色值（RGB）: ")
        self.color_value_lab.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout_color_value.addWidget(self.color_value_lab)
        self.color_value_line_edit = QLineEdit()
        self.color_value_line_edit.setReadOnly(True)
        layout_color_value.addWidget(self.color_value_line_edit)
        layout.addLayout(layout_color_value)

        layout_color = QHBoxLayout()
        self.color_lab = QLabel()
        self.color_lab.setText("颜  色: ")
        self.color_lab.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout_color.addWidget(self.color_lab)
        self.selected_color_btn = QPushButton()
        self.selected_color_btn.setObjectName("selected_color_btn")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.selected_color_btn.setSizePolicy(sizePolicy)
        layout_color.addWidget(self.selected_color_btn)
        layout.addLayout(layout_color)

        self.set_color_btn = QPushButton(self)
        self.set_color_btn.setText("调色")
        layout.addWidget(self.set_color_btn)

        self.setStyleSheet(qss)

        self.setWindowTitle("Color Palette")
        icon_path = "E:\\Matrixtime\\workfile\\GitHub\\pyqt5_test\\widget\\icons\\调色板.png"
        self.setWindowIcon(QIcon(icon_path))
        size = (370, 230)
        self.setFixedSize(*size)

        self.initial_color = QColor(255, 255, 255, 255)
        self.set_color_btn.clicked.connect(partial(self.open_color_dialog, self.initial_color))
        self.selected_color_btn.clicked.connect(partial(self.open_color_dialog, None))

        self.init_data()

    def init_data(self):
        self.set_data(self.initial_color)

    def open_color_dialog(self, initial_color=None):
        try:
            # color_dialog = QColorDialog()
            # color: QColor = color_dialog.getColor()
            if initial_color is None:
                color_ls = list(map(int, self.color_rgba_line_edit.text().split(',')))
                initial_color = QColor(*color_ls)
            color = QColorDialog.getColor(initial_color, self, 'Select Color')
            if color.isValid():
                self.set_data(color)
                print(f"确定-获取当前颜色")
            else:
                print("取消-保持颜色不变")
                pass
        except Exception as e:
            print(e)

    def set_data(self, color: QColor):
        print("color.getRgb() = ", color.getRgb())
        print("color.name(QColor.HexRgb) = ", color.name(QColor.HexRgb))
        print("color.name(QColor.HexArgb) = ", color.name(QColor.HexArgb))
        self.color_rgba_line_edit.setText(",".join(map(str, color.getRgb())))
        self.color_rgba_hexadecimal_line_edit.setText(self._get_rgba_name(color))
        self.selected_color_btn.setStyleSheet(f"background-color: {color.name()};")
        self.color_value_line_edit.setText(color.name(QColor.HexRgb))
        print("- " * 40)

    def _get_rgba_name(self, color: QColor):
        argb = color.name(QColor.HexArgb)
        rgba = argb[:1] + argb[3:] + argb[1:3]
        return rgba

    # def selected_color_btn_clicked_event(self):
    #     try:
    #         background_color: QColor = self.selected_color_btn.palette().color(QPalette.Background)
    #         print("++++++background_color.getRgb()= {}".format(background_color.getRgb()))
    #         color_dialog = QColorDialog()
    #         color_dialog.setCurrentColor(background_color)
    #         color: QColor = color_dialog.getColor()
    #         if color.isValid():
    #             self.set_data(color)
    #             print(f"确定-获取当前颜色")
    #         else:
    #             print("取消-保持颜色不变")
    #             pass
    #     except Exception as e:
    #         print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_widget = ExampleWidget()
    my_widget.show()
    sys.exit(app.exec_())
