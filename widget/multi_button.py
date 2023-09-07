# -*- coding:utf-8 -*-
# __author__ = "Dragon"
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
        self.column_count = None  # 最多显示几列, None表示有几个按钮就显示几列

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
            btn.setObjectName(f'multi_button_{i}')
            btn.setText(name)
            self.buttons.append(btn)
            self._g_layout.addWidget(btn, int(i / self.column_count), i % self.column_count)


if __name__ == '__main__':
    import sys
    from functools import partial
    from PyQt5.QtWidgets import QApplication

    qss = """
    QPushButton {
        border: none;
        border-radius: 6px;
        padding:10px;
        min-width: 80px;
    }
    #multi_button_0, #multi_button_1, #multi_button_2, #multi_button_3{
        color: rgb(0, 0, 0);
        background-color: rgb(74, 138, 244);
    }
    #multi_button_4{
        color: rgb(0, 0, 0);
        background-color: rgb(217, 0, 27);
    }
    """


    def x(btn):
        print(f"btn------{btn.text()}")


    app = QApplication(sys.argv)
    my_widget = MultiButton()
    my_widget.setStyleSheet(qss)
    # name_ls_ = ["1", "2", "3"]
    # my_widget.set_names(name_ls_, column_count=2)
    name_ls_ = ["A", "B", "C", "D", "E"]
    my_widget.set_names(name_ls_)
    # my_widget.set_names(name_ls_, column_count=2)

    for i, button in enumerate(my_widget.buttons):
        button.clicked.connect(partial(x, button))

    my_widget.layout().setContentsMargins(2, 2, 2, 2)
    my_widget.layout().setSpacing(5)
    my_widget.show()
    sys.exit(app.exec_())
    pass
