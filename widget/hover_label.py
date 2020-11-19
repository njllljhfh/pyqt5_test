# -*- coding:utf-8 -*-
import sys

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QTableWidget, QApplication, QTableWidgetItem, QWidget, QHBoxLayout, QLabel, QPushButton, \
    QDialog


class OptionLabel(QLabel):
    """鼠标hover到QLabel时，显示widget"""

    def __init__(self, *args, parent=None, widget=None):
        """
        :param args:
        :param parent: 父级控件
        :param widget: 鼠标hover时显示的控件
        """
        super().__init__(parent, *args)

        # TODO:包含多个操作按钮控（件用户自定义)
        self.option_btn_widget = widget
        self.option_btn_widget.setParent(self)

        self.option_btn_widget.show()
        self.move_option_btn_widget()
        self.option_btn_widget.hide()

        self.setMouseTracking(True)

        self.setStyleSheet("""
            background-color: rgb(255, 80, 60);
        """)

    def leaveEvent(self, event: QEvent):
        print(f"OptionLabel---leaveEvent")
        self.option_btn_widget.hide()

    def enterEvent(self, event: QEvent):
        print(f"OptionLabel---enterEvent")
        self.move_option_btn_widget()
        self.option_btn_widget.show()

    def move_option_btn_widget(self):
        # 居中
        x = int((self.width() - self.option_btn_widget.width()) / 2)
        y = int((self.height() - self.option_btn_widget.height()) / 2)
        self.option_btn_widget.move(x, y)


# 以下是测试类
class MyTableWidget(QTableWidget):
    """QTableWidget基类"""

    def __init__(self, *args, parent=None):
        """
        :param parent: 父级对象
        :param has_header_checkbox: 是否有表头复选框
        """
        super().__init__(parent, *args)

        header_field = ['序号', '姓名', '年龄']
        self.setColumnCount(len(header_field))  # 设置列数
        # 设置行表头字段
        self.setHorizontalHeaderLabels(header_field)

        data_ls = [
            [f"{i}", f"njl{i}", f"{i}"] for i in range(1, 11)
        ]
        # self.setRowCount(len(data_ls))
        try:
            for row, data in enumerate(data_ls):
                self.insertRow(row)
                self.setRowHeight(row, 50)  # 设置行高
                for column, item_data in enumerate(data):
                    if column == self.columnCount() - 1:
                        # 用水平布局使得单元格居中
                        operation_column_btn_widget = QWidget()
                        operation_column_btn_widget.setProperty("name", "operation")
                        # operation_column_btn_widget.setContentsMargins(0, 0, 0, 0)
                        layOut = QHBoxLayout(operation_column_btn_widget)
                        label = OptionLabel(parent=self, widget=OptionBtnWidget())
                        label.setText(str(item_data))
                        label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                        layOut.addWidget(label)  # 开始-按钮
                        layOut.setContentsMargins(0, 0, 0, 0)
                        layOut.setSpacing(2)
                        self.setCellWidget(row, column, operation_column_btn_widget)
                    else:
                        Item = QTableWidgetItem(str(item_data))
                        Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
                        self.setItem(row, column, Item)
        except Exception as e:
            print(f"e = {e}")

        self.setMouseTracking(True)
        print(f"{self.hasMouseTracking()}")


class OptionBtnWidget(QWidget):
    """放操作按钮的控件"""

    def __init__(self, *args, parent=None):
        """
        :param parent: 父级对象
        :param has_header_checkbox: 是否有表头复选框
        """
        super().__init__(parent, *args)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)  # 无边框、置顶、任务栏不显示

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.btn = QPushButton(self)
        self.btn.setText("查看维修记录")
        layout.addWidget(self.btn)
        # - - -

        self.setStyleSheet("""
            background-color: rgb(100, 100, 100);
        """)
        self.btn.clicked.connect(self.btn_clicked_event)

    def btn_clicked_event(self):
        if self.isVisible():
            self.hide()
            # option_widget = OptionWidget(parent=self)
            option_widget = OptionWidget()  # 不设置父类，显示在屏幕的中间
            if option_widget.exec_() == QDialog.Accepted:
                pass
            else:
                pass


class OptionWidget(QDialog):

    def __init__(self, *args, parent=None):
        """
        :param parent: 父级对象
        :param has_header_checkbox: 是否有表头复选框
        """
        super().__init__(parent, *args)
        self.setFixedSize(200, 200)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    my_widget = MyTableWidget()
    my_widget.resize(500, 190)

    my_widget.show()
    sys.exit(app.exec_())

