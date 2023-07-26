# -*- coding:utf-8 -*-
# __author__ = "Dragon"
from functools import partial
from typing import List

from PyQt5.QtWidgets import QGridLayout, QFrame, QPushButton

"""
支持自定义按钮的个数，支持设置显示的行号
"""


class MultiButton(QFrame):

    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(*args, parent=parent, **kwargs)

        self._g_layout = QGridLayout(self)

        self.buttons = []
        self.column_count = None

    def button(self, p_int) -> QPushButton:
        return self.buttons[p_int]

    def set_name(self, p_int, value: str):
        btn = self.buttons[p_int]
        btn.setText(value)

    def set_names(self, name_ls: List[str], column_count=None):
        """
        :param name_ls: 每个按钮的名字
        :param column_count: 列数
        :return:
        """
        for btn in self.buttons:
            self._g_layout.removeWidget(btn)
            btn.deleteLater()

        self.column_count = column_count if column_count else len(name_ls)
        self.buttons.clear()
        for i, name in enumerate(name_ls):
            btn = QPushButton(self)
            btn.setObjectName(f'button_{i}')
            btn.setText(name)
            self.buttons.append(btn)
            self._g_layout.addWidget(btn, int(i / self.column_count), i % self.column_count)


def x(btn):
    print(f"btn------{btn.text()}")


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    my_widget = MultiButton()
    name_ls_ = ["总计", "OK", "NG"]
    my_widget.set_names(name_ls_, column_count=2)
    name_ls_ = ["1", "2", "3", "4"]
    my_widget.set_names(name_ls_, column_count=1)

    for i, btn in enumerate(my_widget.buttons):
        btn.clicked.connect(partial(x, btn))

    my_widget.layout().setContentsMargins(2, 2, 2, 2)
    my_widget.layout().setSpacing(5)
    my_widget.show()
    sys.exit(app.exec_())
    pass
