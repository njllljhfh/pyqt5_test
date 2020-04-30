# -*- coding:utf-8 -*-
from enum import unique, Enum

from PyQt5.QtCore import Qt, QRect, QModelIndex, QPoint
from PyQt5.QtWidgets import QTableWidget, QApplication, QHeaderView, QStyleOptionButton, QStyle, QCheckBox, QMessageBox, \
    QTableWidgetItem, QLabel

import sys


class BaseEnum(Enum):

    @classmethod
    def value_exists(cls, value):
        """
        Determine whether the value is in class.
        :param value: The value of enumerate class.  <type: int>
        :return: True or False.  <type: bool>
        """
        if value in [member.value for member in cls.__members__.values()]:
            return True
        else:
            return False

    @classmethod
    def value_list(cls):
        """
        Get value list.
        :return: Value list.  <type: list>
        """

        return [member.value for member in cls.__members__.values()]


class MyHeader(QHeaderView):
    isOn = False

    def __init__(self, orientation, parent=None):
        QHeaderView.__init__(self, orientation, parent)

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()
        QHeaderView.paintSection(self, painter, rect, logicalIndex)
        painter.restore()

        try:
            if logicalIndex == 0:
                option = QStyleOptionButton()
                option.rect = QRect(10, 10, 7, 20)
                if self.isOn:
                    print(f"xxx--On")
                    option.state = QStyle.State_On
                else:
                    print(f"xxx--Off")
                    option.state = QStyle.State_Off
                self.style().drawControl(QStyle.CE_CheckBox, option, painter)
        except Exception as Error:
            print(Error)
            QMessageBox.warning(self, "警告", str(Error), QMessageBox.Yes, QMessageBox.Yes)

    def mousePressEvent(self, event):
        try:
            # print(f'self.(currentIndex()) = {self.currentIndex()}')
            # print(f'self.(currentIndex().column()) = {self.currentIndex().column()}')
            # print(f'self.(currentIndex().row()) = {self.currentIndex().row()}')
            print(f'self.currentIndex()) = {self.item}')
            if self.currentIndex() == 0:
                self.isOn = not self.isOn
                self.updateSection(0)
                QHeaderView.mousePressEvent(self, event)
                print('xxx')
            else:
                super(MyHeader, self).mousePressEvent(event)
        except Exception as Error:
            print(Error)


class MyTable(QTableWidget):
    @unique
    class HorizontalHeaderField(BaseEnum):
        """ 水平表头
        字段是表头英文名
        值是表头对应的列的索引号
        """
        empty = 0
        camera_id = 1
        camera_code = 2
        camera_name = 3  # 目前表中没有
        position = 4
        exposure_duration = 5
        iso = 6
        is_valid = 7  # 目前表中没有
        oper_status = 8  # 连接状态
        c_type = 9  # 相机类型(el、vi)
        create_time = 10
        option = 11

        @classmethod
        def value_name(cls, value):
            """ Map value to Chinese. """
            value_map = {
                cls.empty.value: "",
                cls.camera_id.value: "相机编号",
                cls.camera_code.value: "相机编码",
                cls.camera_name.value: "相机名称",
                cls.position.value: "相机位",
                cls.exposure_duration.value: "曝光时长",
                cls.iso.value: "增益",
                cls.is_valid.value: "状态",
                cls.oper_status.value: "连接状态",
                cls.c_type.value: "相机类型",
                cls.create_time.value: "创建时间",
                cls.option.value: "操作",
            }
            return value_map.get(value)

    def __init__(self):
        QTableWidget.__init__(self, 0, len(self.HorizontalHeaderField))
        self.resize(1300, 450)
        # super(MyTable, self).__init__(self, 0, len(self.HorizontalHeaderField))
        self.myHeader = MyHeader(Qt.Horizontal, self)
        self.setHorizontalHeader(self.myHeader)

        # 取消水平表头，当单元格选中时的高亮效果
        self.horizontalHeader().setHighlightSections(False)

        # 设置水平表头
        # self.setColumnCount(len(self.myHeader.HorizontalHeaderField))
        header_height = 21  # 表头高度
        self.horizontalHeader().setMinimumHeight(header_height)
        # 水平表头点击事件
        # self.cameraTable.horizontalHeader().sectionClicked.connect(self.eventHorizontalHeaderClicked)
        # 水平表头名字，列宽

        # 水平表头名字，列宽
        for horizontalHeader in self.HorizontalHeaderField:
            column = horizontalHeader.value
            item = QTableWidgetItem()
            item.setText(self.HorizontalHeaderField.value_name(horizontalHeader.value))  # 水平表头-中文
            self.setHorizontalHeaderItem(horizontalHeader.value, item)

            if horizontalHeader == self.HorizontalHeaderField.empty:  # 复选框-列宽
                pass
                # 水平表头 第一列的复选框
                column_width = 40  # 列宽
                # self.cameraTable.headerCheckBox = QCheckBox(self.cameraTable)
                # self.cameraTable.headerCheckBox.setTristate(True)  # 设置为 三态复选框的状态(未选中，半选中，选中)
                # self.cameraTable.headerCheckBox.setCheckState(Qt.Unchecked)  # 默认为未选中
                # w, h = 20, 20
                # offset = 4  # 偏移量基数
                # x, y = (column_width - w) / 2 + offset, (header_height - h) / 2 + offset * 3 / 4
                # self.cameraTable.headerCheckBox.init_x = x
                # self.cameraTable.headerCheckBox.init_y = y
                # self.cameraTable.headerCheckBox.init_w = w
                # self.cameraTable.headerCheckBox.init_h = h
                # self.cameraTable.headerCheckBox.setGeometry(QRect(x, y, w, h))
                # # self.cameraTable.headerCheckBox.setText("Id")
                # self.cameraTable.headerCheckBox.setObjectName("headerCheckBox")
                # self.cameraTable.headerCheckBox.setStyleSheet(
                #     "color: #ffffff;"
                #     "background-color: none;"
                # )
                # self.cameraTable.headerCheckBox.clicked.connect(self.headerCheckBoxClickedEvent)  # 表头复选框点击事件
                #
                self.setColumnWidth(column, column_width)
            elif horizontalHeader == self.HorizontalHeaderField.camera_id:  # 相机编号-列宽
                self.setColumnWidth(column, 140)
            elif horizontalHeader == self.HorizontalHeaderField.camera_name:  # 相机名称-列宽
                self.setColumnWidth(column, 130)
            elif horizontalHeader == self.HorizontalHeaderField.position:  # 相机位置-列宽
                self.setColumnWidth(column, 60)
            elif horizontalHeader == self.HorizontalHeaderField.exposure_duration:  # 曝光-列宽
                self.setColumnWidth(column, 60)
            elif horizontalHeader == self.HorizontalHeaderField.iso:  # 增益-列宽
                self.setColumnWidth(column, 60)
            elif horizontalHeader == self.HorizontalHeaderField.is_valid:  # 状态-列宽
                self.setColumnWidth(column, 70)
            elif horizontalHeader == self.HorizontalHeaderField.oper_status:  # 连接状态-列宽
                self.setColumnWidth(column, 70)
            elif horizontalHeader == self.HorizontalHeaderField.c_type:  # 相机类型-列宽
                self.setColumnWidth(column, 90)
            elif horizontalHeader == self.HorizontalHeaderField.create_time:  # 时间-列宽
                self.setColumnWidth(column, 130)
            elif horizontalHeader == self.HorizontalHeaderField.option:  # 操作-列宽
                self.setColumnWidth(column, 100)
            else:
                pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myTable = MyTable()
    myTable.show()
    sys.exit(app.exec_())
