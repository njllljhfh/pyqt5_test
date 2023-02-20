# -*- coding:utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal, QMutex, Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
import time


class GettingProductThread(QThread):
    """获取产品的线程"""
    signal_load_product = pyqtSignal(int)

    def __init__(self, parent=None):
        """
        :param parent:
        """
        super().__init__(parent)

    def run(self):
        i = 0
        while True:
            i += 1
            time.sleep(0.4)
            is_updating = self.parent()._is_updating
            print(f'is_updating-{is_updating}')
            if is_updating:
                continue
            else:
                self.signal_load_product.emit(i)
                print(f'线程-{i}')
                print('- ' * 20)

            # i += 1
            # time.sleep(0.4)
            # self.signal_load_product.emit(i)
            # print(f'线程-{i}')


class Aaa(QTableWidget):

    def __init__(self):
        # self.update_mutex = QMutex(mode=0)
        self._is_updating = False
        super().__init__()
        header_field = ['数字',]
        self.setColumnCount(len(header_field))
        self.setHorizontalHeaderLabels(header_field)
        self.thd = GettingProductThread(parent=self)

        # 异步连接信号：emit()方法不等待槽函数返回
        self.thd.signal_load_product.connect(self.slot_x, Qt.QueuedConnection)

        # 同步连接信号：emit()方法要等待槽函数返回
        # self.thd.signal_load_product.connect(self.slot_x, Qt.DirectConnection)

        self.thd.start()

    def slot_x(self, x):
        if self._is_updating is True:
            print(f'不处理-{x}')
        else:
            self._is_updating = True
            # self.update_mutex.lock()
            print(f'处理----{x}')

            row = self.rowCount()
            self.insertRow(row)
            Item = QTableWidgetItem(str(x))
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
            self.setItem(row, 0, Item)
            time.sleep(3)

            # self.update_mutex.unlock()
            self._is_updating = False


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    my_widget = Aaa()
    my_widget.resize(300,900)
    my_widget.show()
    sys.exit(app.exec_())
