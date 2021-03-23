# -*- coding:utf-8 -*-
# Dynamically create the widgets of layout.
import sys
from datetime import datetime

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QPushButton, QShortcut, QGridLayout


class MyWidget(QWidget):

    def __init__(self, *args):
        super().__init__(*args)

        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)

        #
        self.btn_1 = QPushButton("test button")
        self.layout.addWidget(self.btn_1, 0, 0, 1, 1)
        self.btn_1.clicked.connect(self.set_new_widget)

        #
        self.layout_image_area = QGridLayout()
        self.layout.addLayout(self.layout_image_area, 0, 1, 1, 1)

        temp_widget = Yyy(parent=self)
        self.layout_image_area.addWidget(temp_widget, 0, 0, 1, 1)

    def set_new_widget(self):
        temp_widget = self.layout_image_area.itemAtPosition(0, 0).widget()
        self.layout_image_area.removeWidget(temp_widget)
        temp_widget.deleteLater()

        b = QPushButton(self)
        b.setText(f"{id(b)}, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.layout_image_area.addWidget(b, 0, 0, 1, 1)


class Yyy(QWidget):

    def __init__(self, *args, parent=None):
        super().__init__(*args, parent=parent)

        layout = QHBoxLayout(self)
        layout.setSpacing(10)

        self.resize(100, 100)
        QShortcut(QKeySequence(self.tr('2')), self, parent.close)
        self.btn = QPushButton(self)
        self.btn.setText('yyy')
        layout.addWidget(self.btn)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWidget()
    win.setObjectName('win')

    win.show()
    sys.exit(app.exec_())
