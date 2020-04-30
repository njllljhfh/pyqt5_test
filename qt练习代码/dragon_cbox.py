# -*- coding:utf-8 -*-
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QTableWidget, QApplication, QHeaderView, QStyleOptionButton, QStyle, QCheckBox, QMessageBox

import sys


class MyHeader(QHeaderView):
    isOn = False

    def __init__(self, orientation, parent=None):
        QHeaderView.__init__(self, orientation, parent)

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()
        QHeaderView.paintSection(self, painter, rect, logicalIndex)
        painter.restore()

        try:
            if logicalIndex == 0:
                option = QStyleOptionButton()
                option.rect = QRect(10, 10, 7, 20)
                if self.isOn:
                    option.state = QStyle.State_On
                else:
                    option.state = QStyle.State_Off
                self.style().drawControl(QStyle.CE_CheckBox, option, painter)
        except Exception as Error:
            print(Error)
            QMessageBox.warning(self, "警告", str(Error), QMessageBox.Yes, QMessageBox.Yes)

    def mousePressEvent(self, event):
        self.isOn = not self.isOn
        self.updateSection(0)
        QHeaderView.mousePressEvent(self, event)
        print('xxx')


class MyTable(QTableWidget):
    def __init__(self):
        QTableWidget.__init__(self, 0, 3)
        # super(MyTable, self).__init__()

        myHeader = MyHeader(Qt.Horizontal, self)
        self.setHorizontalHeader(myHeader)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myTable = MyTable()
    myTable.show()
    sys.exit(app.exec_())
