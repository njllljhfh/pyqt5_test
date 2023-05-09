# -*- coding:utf-8 -*-
import sys
import time

from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QMessageBox, \
    QTextBrowser
from PyQt5.QtGui import QIcon, QTextCursor


class LogMsg(QTextBrowser):

    def __init__(self, parent=None, max_log_num=10):
        super(LogMsg, self).__init__(parent=parent)
        self._count = 0
        self._max_log_num = max_log_num

    def log(self, msg: str):
        if self._count >= self._max_log_num:
            self.clear()
            self._count = 0

        self.append(msg + "\n")
        # print(f"收到的消息：{msg}")
        self._count += 1
        self.moveCursor(QTextCursor.End)


class SimpleNotebook(QWidget):
    def __init__(self):
        super(SimpleNotebook, self).__init__()  # 使用super函数可以实现子类使用父类的方法
        self.setWindowTitle("日志")
        self.setWindowIcon(QIcon('NoteBook.png'))
        self.resize(500, 500)
        self.text = LogMsg(parent=self, max_log_num=15)
        # self.text.setText("Have a nice day")
        # self.text.setPlaceholderText("Please add some here")  # 设置文本初始化内容，调用setReadOnly方法并传入False参数即可编辑浏览器框
        # self.text.textChanged.connect(lambda: print("it is changed"))

        # self.button_2 = QPushButton("Clear", self)
        # self.button_3 = QPushButton("Add", self)

        # self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        # self.h_layout.addWidget(self.button_2)
        # self.h_layout.addWidget(self.button_3)
        self.v_layout.addWidget(self.text)
        # self.v_layout.addLayout(self.h_layout)

        self.setLayout(self.v_layout)
        self.create_msg = CreateMsg()

        self._bind()

        self.create_msg.start()

    def _bind(self):
        # self.button_2.clicked.connect(lambda: self.button_click(self.button_2))
        # self.button_3.clicked.connect(self.add_text)
        # self.create_msg.new_log.connect(self.text.log, Qt.QueuedConnection)
        self.create_msg.new_log.connect(self.text.log)

    # def button_click(self, button):
    #     if button == self.button_2:
    #         print("文本被清除")
    #         self.text.clear()

    # def add_text(self):
    #     self.text.append("hello,world" * 30 + "\n")  # 调用append方法


class CreateMsg(QThread):
    new_log = pyqtSignal(str)

    def __init__(self):
        super(CreateMsg, self).__init__()

    def run(self):
        n = 1
        while True:
            msg = "hello world" * 20 + f"  {n}"
            self.new_log.emit(msg)
            time.sleep(0.4)
            n += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    test = SimpleNotebook()
    test.resize(450, 500)
    test.show()
    sys.exit(app.exec())
