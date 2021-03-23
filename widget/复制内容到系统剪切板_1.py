# -*- coding:utf-8 -*-
import sys

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QPushButton, QShortcut, QKeySequenceEdit


class MyWidget(QWidget):

    def __init__(self, *args):
        super().__init__(*args)

        layout = QHBoxLayout(self)
        layout.setSpacing(10)
        self.copy_product_code_btn = CopyProductCodeBtn(interval_time=1, parent=self)
        self.copy_product_code_btn.setText("复制条码")
        self.copy_product_code_btn.setFixedSize(120, 20)
        layout.addWidget(self.copy_product_code_btn)
        #
        btn1 = QPushButton("测试用的站位按钮1")
        layout.addWidget(btn1)

        # 更新产品条码
        self.copy_product_code_btn.update_product_code("11930200010000123456801")


class CopyProductCodeBtn(QPushButton):
    """复制产品编码"""

    def __init__(self, *args, interval_time: int = 3, parent=None):
        super().__init__(parent, *args)
        self._product_code = ""
        self.clicked.connect(self.clicked_event)
        # - - -

        # 时间间隔(秒)
        self.interval_time = interval_time

        # 定时器
        self.timer = QTimer()
        self.timer.setInterval(interval_time * 1000)  # 时间间隔换算为:秒
        self.timer.setTimerType(Qt.PreciseTimer)
        self.timer.timeout.connect(self.time_out_event)

        # - - -
        # QShortcut(QKeySequence(self.tr('ctrl+1')), self, parent.close)
        QShortcut(QKeySequence('ctrl+1'), self, parent.close)

    def clicked_event(self):
        try:
            print(f"产品条码: {self._product_code}")
            clipboard = QApplication.clipboard()  # 获取系统剪贴板指针
            clipboard.setText(str(self._product_code))  # 设置剪贴板文本信息
            text = clipboard.text()  # 获取剪贴板上文本信息

            self.setEnabled(False)
            self.setText("产品条码已复制")
            self.timer.start()

        except Exception as e:
            print(f"error = {e}")

    def time_out_event(self):
        if not self.isEnabled():
            self.setEnabled(True)
            self.setText("复制条码")
            self.timer.stop()

    def update_product_code(self, product_code: str):
        """
        更新产品条码
        :param product_code: 产品条码
        :return: None
        """
        self._product_code = product_code


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWidget()
    win.show()
    sys.exit(app.exec_())
