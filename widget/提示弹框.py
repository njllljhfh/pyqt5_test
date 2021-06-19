# -*- coding:utf-8 -*-
import sys
import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMessageBox, QApplication, QPushButton, QHBoxLayout, QWidget

qss = '''
QMessageBox {
    color: rgb(220, 220, 220);
    background-color: rgb(61, 61, 61);
}

QPushButton {
    background-color: rgb(51, 51, 51);
    color: rgb(241, 241, 241);
}

QLabel {
    color: rgb(241, 241, 241);
}

'''


class WarningMessageBoxOne(QMessageBox):  # 警告
    def __init__(self, *args):
        super().__init__(*args)
        self.btn_yes = self.addButton("确认", QMessageBox.YesRole)
        # self.no = self.box.addButton("取消", QMessageBox.NoRole)
        # QTimer.singleShot(1000, self.box.accept) # 定时关闭
        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap(":/icons/title.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.box.setWindowIcon(icon)
        self.setStyleSheet(qss)

    # def msg_exec(self):
    #     if self.box.clickedButton() == self.yes:
    #         return True
    #     else:
    #         return False

    def closeEvent(self, event: QCloseEvent) -> None:
        print(f'close')
        super().close()


class MyWidget(QWidget):

    def __init__(self, *args, parent=None):
        """
        :param parent: 父级对象
        :param has_header_checkbox: 是否有表头复选框
        """
        super().__init__(parent, *args)

        try:
            layout = QHBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            self.btn = QPushButton("xxx")
            layout.addWidget(self.btn)

            self.btn.clicked.connect(self.retrieve_task_list)

            self.info_box = None

            self.retrieve_task_list()
        except Exception as e:
            print(f'Error: {e}')

    def retrieve_task_list(self):
        try:
            my_thread = ThreadTaskList(parent=self)
            my_thread.signal_err_msg.connect(self.handler_err)
            my_thread.start()
        except Exception as e:
            print(f'Error: {e}')

    def handler_err(self, info):
        try:
            if not self.info_box:
                self.info_box = WarningMessageBoxOne(QMessageBox.Warning, "提示", info)
                self.info_box.buttonClicked.connect(self.handler_clear_info_box)
                self.info_box.exec_()
                self.info_box = None
            else:
                self.info_box: WarningMessageBoxOne
                self.info_box.setText(info)
        except Exception as e:
            print(f'Error: {e}')

    def handler_clear_info_box(self):
        try:
            print(f'handler_clear_info_box')
            self.info_box = None
        except Exception as e:
            print(f'Error: {e}')


class ThreadTaskList(QThread):
    """获取任务数据"""
    signal_err_msg = pyqtSignal(str)  # 错误信号(参数1：错误信息)

    def __init__(self, parent=None, callback=None):
        """
        :param parent: 父级对象
        :param callback: 列表刷新后的回调函数
        """
        super().__init__(parent)

    def run(self):
        try:
            for i in range(1, 4):
                info = f'{i}---错误'
                self.signal_err_msg.emit(info)
                print(f'发送error, {i}')
                time.sleep(1)
        except Exception as e:
            print(f'Error: {e}')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    my_widget = MyWidget()

    my_widget.show()
    sys.exit(app.exec_())
