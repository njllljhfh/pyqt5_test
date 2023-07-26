# -*- coding:utf-8 -*-
# __author__ = "Dragon"
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QGridLayout, QFrame

"""
支持自定义统计元素的个数，支持设置显示的行号
"""


class Element(QFrame):

    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(*args, parent=parent, **kwargs)

        layout = QVBoxLayout(self)
        self.name = QLabel("")
        self.name.setAlignment(Qt.AlignCenter)
        self.value = QLabel("")
        self.value.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.name)
        layout.addWidget(self.value)


class LabelPanel(QFrame):

    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(*args, parent=parent, **kwargs)

        self._g_layout = QGridLayout(self)

        self.elements = []
        self.column_count = None

    def element(self, p_int):
        return self.elements[p_int]

    def set_value(self, p_int, value: str):
        element = self.elements[p_int]
        element.setText(value)

    def set_names(self, name_ls: List[str], column_count=None):
        """
        :param name_ls: 每个元素的名字
        :param column_count: 列数
        :return:
        """
        for element in self.elements:
            self._g_layout.removeWidget(element)
            element.deleteLater()

        self.column_count = column_count if column_count else len(name_ls)
        self.elements.clear()
        for i, name in enumerate(name_ls):
            element = Element(parent=self)
            element.setObjectName(f'element_{i}')
            element.name.setText(name)
            element.name.setObjectName(f'element_{i}_name')
            element.value.setObjectName(f'element_{i}_value')
            self.elements.append(element)
            self._g_layout.addWidget(element, int(i / self.column_count), i % self.column_count)

    def set_values(self, value_ls: List[str]):
        for i, element in enumerate(self.elements):
            element.value.setText(value_ls[i])

    def set_empty_values(self, value: str = "0"):
        for element in self.elements:
            element.value.setText(value)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    my_widget = LabelPanel()
    name_ls_ = ["总计", "OK", "NG"]
    my_widget.set_names(name_ls_, column_count=2)
    my_widget.layout().setContentsMargins(2, 2, 2, 2)
    my_widget.layout().setSpacing(5)
    my_widget.show()
    my_widget.set_values(["1", "2", "3"])
    sys.exit(app.exec_())
    pass
