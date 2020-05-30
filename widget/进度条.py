# -*- coding:utf-8 -*-
import sys
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QThread
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMessageBox, QProgressBar, QPushButton, QGridLayout

qss = """
MyQProgressBar QProgressBar::chunk
{
   background-color:rgb(33, 44, 55);
   width:10px;
   margin:0.5px;
}
"""


class MyWidget(QWidget):

    def __init__(self, *args):
        super().__init__(*args)
        # layout = QVBoxLayout(self)
        layout = QGridLayout(self)

        self.setMinimumSize(600, 300)
        self.my_progress_bar = MyQProgressBar()
        self.my_progress_bar.setVisible(False)
        # layout.addWidget(self.my_progress_bar)
        layout.addWidget(self.my_progress_bar, 0, 0, 1, 1)
        layout.setContentsMargins(0, 0, 0, 0)

        self.btn = QPushButton(self)
        self.btn.setText("开始")

        self.my_thread = MyThread()
        self.my_thread.init_data()
        self.my_thread.update_progress_signal.connect(self.my_progress_bar.set_process)
        self.my_thread.set_progress_bar_range_signal.connect(self.my_progress_bar.init_progress_bar)
        self.my_thread.error_signal.connect(self.my_thread_error_signal_handler)
        # self.my_thread.finished.connect(self.my_thread_finished_handler)
        # self.my_thread.start()

        self.btn.clicked.connect(self.start_my_thread)

    def start_my_thread(self):
        if not self.my_progress_bar.isVisible():
            self.my_progress_bar.setVisible(True)

        self.my_thread.start()

    def my_thread_finished_handler(self):
        """线程执行结束"""
        print(f"线程执行结束")
        if self.my_progress_bar.isVisible():
            self.my_progress_bar.close()

    @pyqtSlot(Exception)
    def my_thread_error_signal_handler(self, e):
        """"""
        qMessageBox = QMessageBox()
        qMessageBox.warning(self, "警告", str(e), QMessageBox.Yes, QMessageBox.Yes)


class MyQProgressBar(QWidget):
    def __init__(self, *args):
        super().__init__(*args)
        # 调用UI界面

        # 构建一个进度条
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        # layout.setSpacing(0)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setWindowModality(Qt.ApplicationModal)

        self.progress_bar = QProgressBar(self)
        # self.progress_bar.setObjectName("")

        self.setFixedSize(60, 15)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progress_bar.sizePolicy().hasHeightForWidth())
        self.progress_bar.setSizePolicy(sizePolicy)
        self.progress_bar.setTextVisible(False)  # 不显示进度数字
        # self.progress_bar.setRange(0, 1000)
        layout.addWidget(self.progress_bar)
        # layout.setAlignment(self.pbar, Qt.AlignVCenter)
        # self.setStyleSheet("{background-color: none;}")
        # 进度条位置,x,y,宽，高 坐标35-50,显示一个200*25界面
        # self.pbar.setGeometry(0, 0, 200, 25)
        # self.show()

        # self.setStyleSheet(qss)

    @pyqtSlot(int)
    def init_progress_bar(self, total_count):
        """设置进度条范围"""
        print(f"设置进度条范围={total_count}")
        self.progress_bar.setRange(0, total_count)
        # self.progress_bar.setValue(0)

    # @pyqtSlot(int, int)
    @pyqtSlot(int)
    def set_process(self, progress):
        """设置进度"""
        print(f"progress = {progress}")
        self.progress_bar.setValue(progress)
        if self.progress_bar.maximum() == progress and self.isVisible():
            print(f"self.progress_bar.maximum() = {self.progress_bar.maximum()}")
            self.close()


class MyThread(QThread):
    update_progress_signal = pyqtSignal(int)
    set_progress_bar_range_signal = pyqtSignal(int)
    error_signal = pyqtSignal(Exception)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quit_flag = False

    def init_data(self):
        self.quit_flag = False

    def run(self):
        data_ls = [i for i in range(0, 10)]
        total_count = len(data_ls)
        self.set_progress_bar_range_signal.emit(total_count)
        # print(f"data_ls = {data_ls}")
        for i in data_ls:
            # self.update_progress_signal.emit(i + 1, total_count)
            # if i == 5:
            #     self.update_progress_signal.emit(10)
            #     break
            self.update_progress_signal.emit(i + 1)
            # print(f"i = {i}")
            # time.sleep(0.003)
            time.sleep(0.3)
            # if i == 3:
            #     e = ValueError("错误")
            #     self.error_signal.emit(e)
            #     break

    def quit(self):
        self.quit_flag = True
        print(f"MyThread----quit")

    # def exit(self, returnCode=0):
    #     print(f"MyThread----exit")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
