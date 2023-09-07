# -*- coding:utf-8 -*-
import sys
import time

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QPushButton, QApplication

"""
测试，主线程是否可以修改QT子线程内部参数
测试结果：可以修改
"""


class MyThread(QThread):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.flag = True

    def run(self):
        while True:
            try:
                print(f"flag = {self.flag}")
                time.sleep(1)
            except Exception as e:
                print(e)


class MyWidget(QFrame):
    """图像标注组件"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.btn = QPushButton(self)
        self.btn.setText("按钮")
        layout.addWidget(self.btn)

        self.th = MyThread(parent=self)
        self.th.start()
        self.btn.clicked.connect(self.click_btn)

    def click_btn(self):
        print(f"点击按钮")
        self.th.flag = time.time()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
