# -*- coding:utf-8 -*-
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QWidget, QApplication, QHBoxLayout

import apprsc_rc


class Xxx(QWidget):

    def __init__(self, *args):
        super().__init__(*args)

        layout = QHBoxLayout(self)
        self.label = QLabel("ok")
        self.label.setMinimumSize(300, 100)
        self.label.setAlignment(Qt.AlignHCenter)
        # pix = QPixmap(":icons/ng_img.png")
        pix = QPixmap("../icons/ng_img.png")
        self.label.setPixmap(pix)
        layout.addWidget(self.label)
        # self.setWindowIcon(QIcon(":icons/ng_img.png"))
        self.setWindowIcon(QIcon("../icons/ng_img.png"))


if __name__ == '__main__':
    # sys.path.append("..")
    from log_config import settings

    app = QApplication(sys.argv)
    # win = ImageCanvas()
    win = Xxx()
    win.show()

    sys.exit(app.exec_())
