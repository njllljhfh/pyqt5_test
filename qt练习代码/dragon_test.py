# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import QWidget

from ui.dragon_test_ui import Ui_dragonTest


class DragonTestWin(QWidget, Ui_dragonTest):

    def __init__(self, parent=None):
        super(DragonTestWin, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    myWin = DragonTestWin()
    myWin.show()
    sys.exit(app.exec_())
