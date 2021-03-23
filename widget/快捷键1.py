# -*- coding:utf-8 -*-
import sys

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QPushButton, QShortcut, QKeySequenceEdit, QDialog


class MyWidget(QWidget):

    def __init__(self, *args):
        super().__init__(*args)

        layout = QHBoxLayout(self)
        layout.setSpacing(10)
        #
        self.btn_1 = QPushButton("test button")
        layout.addWidget(self.btn_1)

        self.btn_1.clicked.connect(self.xxx)

        self.yyy = Yyy(parent=self)
        self.yyy.setObjectName('hhh')
        self.yyy.setFixedSize(200, 200)
        layout.addWidget(self.yyy)

    def xxx(self):

        x = X(parent=self)
        # x = X()
        if x.exec_() == QDialog.Accepted:
            print('confirm.')
            pass
        else:
            print('close.')
            pass


class X(QDialog):

    def __init__(self, *args, parent=None):
        super().__init__(parent, *args)

        self.resize(100, 100)

        QShortcut(QKeySequence('ctrl+1'), self, parent.close)


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

    # Why this qss is not work?
    win.setStyleSheet('''
        MyWidget Yyy{
            background-color: rgb(255, 0, 0);
            border: 8px solid rgb(0, 0, 0);
        }
        ''')

    win.show()
    sys.exit(app.exec_())
