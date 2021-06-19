# -*- coding:utf-8 -*-
import sys

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QTableWidget, QApplication, QTableWidgetItem, QWidget, QHBoxLayout, QLabel, QPushButton, \
    QDialog, QFrame


class MyWidget(QFrame):

    def __init__(self, *args, parent=None):
        """
        :param parent: 父级对象
        :param has_header_checkbox: 是否有表头复选框
        """
        super().__init__(parent, *args)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.btn = QPushButton(self)
        self.btn.setText("查看维修记录")
        layout.addWidget(self.btn)
        # - - -
        self.btn.clicked.connect(self.btn_clicked_event)

    def btn_clicked_event(self):
        # option_widget = OptionWidget(parent=self)
        option_widget = OptionWidget()  # 不设置父类，显示在屏幕的中间
        option_widget.rejected.connect(self._dialog_rejected)
        option_widget.exec_()
        # if option_widget.exec_() == QDialog.Accepted:
        #     pass
        # else:
        #     pass

    def _dialog_rejected(self):
        print(f"_dialog_rejected")


class OptionWidget(QDialog):

    def __init__(self, *args, parent=None):
        """
        :param parent: 父级对象
        :param has_header_checkbox: 是否有表头复选框
        """
        super().__init__(parent, *args)
        self.setFixedSize(200, 200)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    my_widget = MyWidget()
    my_widget.resize(500, 190)

    my_widget.show()
    sys.exit(app.exec_())
