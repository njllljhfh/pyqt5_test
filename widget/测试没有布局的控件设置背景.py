# -*- coding:utf-8 -*-
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget,QRadioButton, QDateTimeEdit, QVBoxLayout, QApplication


class MyWidget(QWidget):
    def __init__(self, parent=None, *args):
        super().__init__(parent, *args)
        # layout = QVBoxLayout(self)

        # self.btn = QRadioButton(self)
        # self.btn.setChecked(True)
        # self.btn.setEnabled(False)
        # layout.addWidget(self.btn)

        self.setStyleSheet("""
        MyWidget {
            background-color: rgb(255, 0, 0); 
        }
        """)
        self.resize(200, 150)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_widget = MyWidget()
    my_widget.show()
    sys.exit(app.exec_())