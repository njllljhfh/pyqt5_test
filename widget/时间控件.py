# -*- coding:utf-8 -*-
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QDateTimeEdit, QVBoxLayout, QApplication


class MyWidget(QWidget):
    def __init__(self, parent=None, *args):
        super().__init__(parent, *args)
        layout = QVBoxLayout(self)

        self.date_time_edit = QDateTimeEdit(self)
        self.date_time_edit.setObjectName("date_time_edit")
        self.date_time_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.date_time_edit.setCalendarPopup(True)
        layout.addWidget(self.date_time_edit)

        self.setStyleSheet("""
        QWidget {
            background-color: rgb(0, 0, 0); 
        }
        """)
        self.resize(200, 150)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_widget = MyWidget()
    my_widget.show()
    sys.exit(app.exec_())
