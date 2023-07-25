# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.lineEdit = QLineEdit(self)
        self.lineEdit.textChanged.connect(self.handleTextChanged)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lineEdit)
        self.setLayout(self.layout)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)  # 设置延迟时间，单位为毫秒
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.handleInputFinished)

    def handleTextChanged(self):
        # 每次文本发生更改时，重新启动计时器
        self.timer.start()

    def handleInputFinished(self):
        # 当计时器超时时，表示输入结束
        text = self.lineEdit.text()
        print("输入结束：", text)


if __name__ == "__main__":
    app = QApplication([])
    widget = MyWidget()
    widget.show()
    app.exec()
