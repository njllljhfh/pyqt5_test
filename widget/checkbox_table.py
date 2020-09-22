# -*- coding:utf-8 -*-
# __author__= "NiuJinLong"
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QCheckBox, QHeaderView, QStyle, \
    QStyleOptionButton, QTableWidgetItem, QHBoxLayout, QAbstractItemView, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal, QRect, pyqtSlot, QSize


# import logging
#
# logger = logging.getLogger(__name__)


class CheckBoxHeader(QHeaderView):
    """自定义表头类:带复选框的表头"""

    # 复选框状态改变（参数1:改变后的表头复选框状态）
    check_state_change_signal = pyqtSignal(int)

    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self.check_state = Qt.Unchecked
        self.setContentsMargins(0, 0, 0, 0)

        # 这4个变量控制列头复选框的样式，位置以及大小
        self._x = 0
        self._y = 0
        self._width = 14
        self._height = 14

        # 复选框偏移量
        self._x_offset = 0
        self._y_offset = 2

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()
        super().paintSection(painter, rect, logicalIndex)
        painter.restore()

        if logicalIndex == 0:
            self._x = (rect.width() - self._width) / 2. + self._x_offset
            self._y = (rect.height() - self._height) / 2. + self._y_offset

            option = QStyleOptionButton()
            option.rect = QRect(rect.x() + self._x, rect.y() + self._y, self._width, self._height)
            option.state = QStyle.State_Enabled | QStyle.State_Active
            if self.check_state == Qt.Checked:
                option.state |= QStyle.State_On
            elif self.check_state == Qt.PartiallyChecked:
                option.state |= QStyle.State_NoChange
            else:
                option.state |= QStyle.State_Off
            self.style().drawControl(QStyle.CE_CheckBox, option, painter)

    def mousePressEvent(self, event):
        index = self.logicalIndexAt(event.pos())
        if index == 0:
            # print("index = {}".format(index))
            # x = self.sectionPosition(index)
            # print("x = {}".format(x))
            # if x + self._x < event.pos().x() < x + self._x + self._width \
            #         and self._y < event.pos().y() < self._y + self._height:
            if self._x < event.pos().x() < self._x + self._width \
                    and self._y < event.pos().y() < self._y + self._height:

                if self.check_state == Qt.Checked:
                    self.check_state = Qt.Unchecked
                else:
                    self.check_state = Qt.Checked

                # 当用户点击了行表头复选框，发送改变后的表头复选框状态
                self.check_state_change_signal.emit(self.check_state)
                self.updateSection(0)

        super().mousePressEvent(event)

    def set_check_state(self, check_state):
        """设置表头复选框状态"""
        if self.check_state != check_state:
            self.check_state = check_state
            self.updateSection(0)
            self.check_state_change_signal.emit(self.check_state)


class BaseTableWidget(QTableWidget):
    """QTableWidget基类"""

    # 错误信号
    error_signal = pyqtSignal(Exception)

    def __init__(self, *args, parent=None, has_header_checkbox: bool = False):
        """
        :param parent: 父级对象
        :param has_header_checkbox: 是否有表头复选框
        """
        super().__init__(parent, *args)
        # 表头是否有checkbox
        self.has_header_checkbox = has_header_checkbox
        # 列偏移量
        self._column_offset = 1 if has_header_checkbox else 0
        # 全部行的复选框对象列表
        self.all_combobox_ls = list()
        # 已选择行的复选框对象的列表
        self.selected_combobox_ls = list()

    def set_table_header_field(self, header_field: list):
        """设置行表头字段"""
        try:
            # 表头字段，全局变量
            if self.has_header_checkbox:
                # 表头checkbox
                header_field.insert(0, None)
                self.setColumnCount(len(header_field))  # 设置列数
                header = CheckBoxHeader()  # 实例化自定义表头
                header.check_state_change_signal.connect(self.h_header_check_state_change_handler)
                self.setHorizontalHeader(header)  # 设置表头
            else:
                self.setColumnCount(len(header_field))  # 设置列数

            # 设置行表头字段
            self.setHorizontalHeaderLabels(header_field)
        except Exception as e:
            raise e

    def insert_one_row(self, row_data, row: int, refresh_all=False):
        """
        插入一行数据: 插入一行数据的方法，由子类实现。
        如果设置表头checkbox，请在子类中调用add_row_checkbox()添加每行的checkbox。
        如果不需要表头checkbox，请在子类中自行实现insert_one_row()方法。
        :param row_data: 数据
        :param row: 行号
        :param refresh_all: 调用insert_rows()方法插入多条数据时，是否全表刷新
        :return:
        """
        pass

    def add_row_checkbox(self, row, checkbox: QCheckBox, checkbox_widget: QWidget):
        """
        为每一行的第一列添加复选框
        :param row: 行号
        :param checkbox: 表头 QCheckBox 对象(可自定义该对象，自定义的对象继承QCheckBox类即可)
        :param checkbox_widget: 承载 表头QCheckBox 的 QWidget 对象(可自定义该对象，自定义的对象继承QWidget类即可)
        :return:
        """
        layout = QHBoxLayout(checkbox_widget)
        layout.addWidget(checkbox)
        layout.setAlignment(checkbox, Qt.AlignVCenter | Qt.AlignHCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setCellWidget(row, 0, checkbox_widget)
        checkbox.clicked.connect(self.row_checkbox_clicked_event(checkbox))
        self.all_combobox_ls.append(checkbox)

        return checkbox_widget

    def insert_rows(self, rows_data: list, refresh_all=False, specify_row: int = False):
        """
        插入多行数据,默认在table已有行的下一行添加数据
        :param rows_data: 数据(推荐类型：[dict, ...])
        :param refresh_all: 是否清空表从第0行插入数据
        :param specify_row: 从第几行开始插入（0 <= start_row <= 已有行数）
        :return:
        """

        try:
            if refresh_all:
                # 忽略指定行，从第0行开始插入
                self.clear_data()
                start_row = 0
            else:
                if specify_row is not False:
                    # 从指定行开始插入
                    start_row_min = 0
                    start_row_max = self.rowCount()
                    assert start_row_min <= specify_row <= start_row_max, \
                        "起始行号超出范围 {}-{}".format(start_row_min, start_row_max)
                    start_row = specify_row
                else:
                    # 从已有行的下一行开始插入
                    start_row = self.rowCount()  # 获取已有数据行数

            for i, row_data in enumerate(rows_data):
                row = start_row + i
                self.insert_one_row(row_data, row, refresh_all=refresh_all)

            # 当在已有行的中间插入数据时，可能需要执行该方法
            # if specify_row is not False:
            #     self.update_selected_checkbox_ls_and_all_checkbox_ls()

            self.update_header_checkbox_state()
        except Exception as e:
            self.error_signal.emit(e)

    def row_checkbox_clicked_event(self, checkbox: QCheckBox):
        """每行第一列QCheckBox"""

        def wrapper():
            row = self.get_row_by_row_checkbox(checkbox)
            self.selectRow(row)

            # 设置row复选框
            if checkbox.checkState() == Qt.Checked:
                self.selected_combobox_ls.append(checkbox)
            else:
                self.selected_combobox_ls.remove(checkbox)
            self.update_header_checkbox_state()

            self.get_selected_data()

        return wrapper

    def get_row_by_row_checkbox(self, checkbox: QCheckBox):
        """根据给定某行第一列checkbox，获取该checkbox所在行号"""

        for row in range(self.rowCount()):
            cell_widget: QWidget = self.cellWidget(row, 0)
            c_box = cell_widget.findChild(QCheckBox)
            if c_box is checkbox:
                return row

    def get_row_checkbox_by_row(self, row: int):
        """根据给定某行第一列checkbox，获取该checkbox所在行号"""

        cell_widget: QWidget = self.cellWidget(row, 0)
        checkbox = cell_widget.findChild(QCheckBox)
        return checkbox

    def update_header_checkbox_state(self):
        # 设置表头复选框
        if self.has_header_checkbox:
            h_header: CheckBoxHeader = self.horizontalHeader()
            if len(self.selected_combobox_ls) == 0:
                h_header.set_check_state(Qt.Unchecked)
            elif 0 < len(self.selected_combobox_ls) < self.rowCount():
                h_header.set_check_state(Qt.PartiallyChecked)
            elif len(self.selected_combobox_ls) == self.rowCount():
                h_header.set_check_state(Qt.Checked)

    def update_selected_checkbox_ls_and_all_checkbox_ls(self):
        """更新all_combobox_ls、selected_combobox_ls"""
        print("更新缓存的all_combobox_ls、selected_combobox_ls中的维护的checkbox")
        self.all_combobox_ls.clear()
        self.selected_combobox_ls.clear()
        for row in range(self.rowCount()):
            cell_widget = self.cellWidget(row, 0)
            row_checkbox = cell_widget.findChild(QCheckBox)
            self.all_combobox_ls.append(row_checkbox)

            if row_checkbox.checkState() == Qt.Checked:
                self.selected_combobox_ls.append(row_checkbox)

        # 更新表头复选框状态
        self.update_header_checkbox_state()

        self.get_selected_data()
        print("- " * 30)

    @pyqtSlot(int)
    def h_header_check_state_change_handler(self, check_state):
        """
        水平表头复选框状态改变事件
        :param check_state: 改变后的表头复选框状态
        :return:
        """
        try:
            if self.rowCount() == 0:
                h_header: CheckBoxHeader = self.horizontalHeader()
                h_header.set_check_state(Qt.Unchecked)
                return

            if check_state == Qt.Unchecked:
                self.selected_combobox_ls.clear()
                for checkbox in self.all_combobox_ls:
                    checkbox.setCheckState(Qt.Unchecked)
            elif check_state == Qt.Checked:
                self.selected_combobox_ls.clear()
                for checkbox in self.all_combobox_ls:
                    checkbox.setCheckState(Qt.Checked)
                    self.selected_combobox_ls.append(checkbox)
            else:
                # 改变后的表头复选框状态为:Qt.PartiallyChecked,不需要处理
                pass
            self.get_selected_data()
        except Exception as e:
            self.error_signal.emit(e)

    def get_selected_data(self):
        """获取已选择行号的列表"""
        print("已选的行数 = {}".format(len(self.selected_combobox_ls)))
        row_ls = [self.get_row_by_row_checkbox(combobox) for combobox in self.selected_combobox_ls]
        row_ls.sort()
        print("已选行号列表 = {}".format(row_ls))
        all_row_ls = [self.get_row_by_row_checkbox(combobox) for combobox in self.all_combobox_ls]
        all_row_ls.sort()
        print("全部行号列表 = {}".format(all_row_ls))
        print("- " * 30)
        return row_ls

    def remove_row(self, row: int):
        """
        移除行
        :param row: 行号
        :return:
        """
        self.removeRow(row)
        if self.has_header_checkbox:
            # 删除行后要更新缓存缓存的row_checkbox
            self.update_selected_checkbox_ls_and_all_checkbox_ls()

    def clear_data(self):
        """清除数据"""
        self.clearContents()
        self.setRowCount(0)
        self.all_combobox_ls.clear()
        self.selected_combobox_ls.clear()


if __name__ == '__main__':

    # 自定义的table子类
    class MyCheckboxTable(BaseTableWidget):
        """例子:BaseTableWidget的子类"""

        def __init__(self, *args, parent=None, has_header_checkbox: bool = False):
            super().__init__(*args, parent=parent, has_header_checkbox=has_header_checkbox)

            self.serial_num_max = 0
            self.init_ui()

        def init_ui(self):

            # 设置表格
            # 取消水平表头，当单元格选中时的高亮效果
            self.horizontalHeader().setHighlightSections(False)
            # 取消竖直表头
            self.verticalHeader().setHidden(True)
            # 设置不能编辑
            self.setEditTriggers(QAbstractItemView.NoEditTriggers)
            # 单行模式选择
            self.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.setSelectionMode(QAbstractItemView.SingleSelection)
            # 交替行颜色
            self.setAlternatingRowColors(True)

        def init_data(self):
            self.serial_num_max = 0
            pass

        def set_table_header_field(self, header_field: list):
            super().set_table_header_field(header_field)
            # self.horizontalHeader().setMinimumHeight(20) # 设置表头高度
            self.setColumnWidth(0, 40)  # 设置第0列宽度

        def insert_one_row(self, row_data: dict, row: int, refresh_all=False):
            """自己实现"""

            self.insertRow(row)

            serial_number = row + 1

            # - - -
            # if refresh_all:
            #     serial_number = row + 1
            #     self.serial_num_max = self.rowCount()
            # else:
            #     self.serial_num_max += 1
            #     serial_number = self.serial_num_max
            # print("self.serial_num_max = {}".format(self.serial_num_max))
            # - - -

            # 调用父类方法添加第一列的checkbox
            if self.has_header_checkbox:
                # 第1列
                row_checkbox = QCheckBox()
                row_checkbox.setProperty("name", "row_checkbox")
                checkbox_widget = QWidget(self)
                self.add_row_checkbox(row, row_checkbox, checkbox_widget)

            # 序号
            Item = QTableWidgetItem(str(serial_number))
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
            self.setItem(row, self._column_offset + 0, Item)

            # 名字
            Item = QTableWidgetItem(str(row_data["name"]))
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
            Item.setToolTip(str(row_data["name"]))
            self.setItem(row, self._column_offset + 1, Item)

            # 年龄
            Item = QTableWidgetItem(str(row_data["age"]))
            Item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
            self.setItem(row, self._column_offset + 2, Item)

            # 操作
            column_last = self._column_offset + 3  # 操作列
            delete_btn = QPushButton(self)
            delete_btn.setText("删除")
            delete_btn.setObjectName("delete_btn")  # objId
            delete_btn.setCursor(Qt.PointingHandCursor)
            delete_btn.setFixedSize(QSize(55, 20))

            # 用水平布局使得单元格居中
            operation_column_btn_widget = QWidget()
            operation_column_btn_widget.setProperty("name", "operation")
            # operation_column_btn_widget.setContentsMargins(0, 0, 0, 0)
            layOut = QHBoxLayout(operation_column_btn_widget)
            layOut.addWidget(delete_btn)  # 开始-按钮
            layOut.setAlignment(delete_btn, Qt.AlignVCenter)
            layOut.setContentsMargins(0, 0, 0, 0)
            layOut.setSpacing(2)
            self.setCellWidget(row, column_last, operation_column_btn_widget)

            # 绑定按钮事件
            delete_btn.clicked.connect(self.delete_btn_clicked_event(operation_column_btn_widget))

            # 更新序号
            self.update_all_back_rows_serial_number(row, plus_one=True)
            # - -

        def update_all_back_rows_serial_number(self, row: int, plus_one=True):
            """
            更新指定行后的全部行的序号
            :param row: 行号
            :param plus_one: True(插入1行)；False(删除一行)
            :return:
            """

            if plus_one:
                # 插入时加1
                start_row = row + 1
            else:
                # 删除时
                start_row = row

            print("当前行号 = {}".format(row))
            print("当前行的序号 = {}".format(row + 1))
            print("需要更新的起始行 = {}".format(start_row))
            print("表中总行数 = {}".format(self.rowCount()))

            # 遍历更新后面的全部行的序号
            for updated_row in range(start_row, self.rowCount()):
                new_serial_num = updated_row + 1
                print("下一行更新后的序号 = {}".format(new_serial_num))
                serial_item = self.item(updated_row, self._column_offset + 0)
                serial_item.setText(str(new_serial_num))
            print("——————————————————————————————")

        def delete_btn_clicked_event(self, operation_column_btn_widget: QWidget):
            """删除人工检测缺陷"""

            def wrapper():
                try:
                    # 获取当前点击行，任务名称的item
                    row = self._current_clicked_row(operation_column_btn_widget)
                    name_item = self.item(row, self._column_offset + 1)

                    print("删除人工检测缺陷:{}".format(name_item.text()))
                    self.remove_row(row)
                    self.update_all_back_rows_serial_number(row, plus_one=False)
                except Exception as e:
                    print(f"Error:{e}")

            return wrapper

        def _current_clicked_row(self, operation_column_btn_widget: QWidget) -> int:
            """
            通过操作列按钮的QWidget，获取该行名称的QTableWidgetItem
            :param operation_column_btn_widget:
            :return: 行号
            """
            row = 0
            column = self.columnCount() - 1
            for row_ in range(self.rowCount()):
                cellWidget = self.cellWidget(row_, column)
                if cellWidget is operation_column_btn_widget:
                    row = row_
                    print(f"row = {row}")
                    break
            self.selectRow(row)
            return row


    # 自定义的QWidget例子
    class ExampleWidget(QWidget):
        """例子"""

        def __init__(self, parent=None, *args):
            super().__init__(parent, *args)
            layout = QVBoxLayout(self)
            self.btn = QPushButton(self)
            self.btn.setText("确定")
            layout.addWidget(self.btn)

            self.check_box_table = MyCheckboxTable(has_header_checkbox=True)
            # self.check_box_table = MyCheckboxTable(has_header_checkbox=False)
            layout.addWidget(self.check_box_table)

            self.setWindowTitle('这是QTableWidget类行表头添加复选框全选功能')
            self.resize(600, 400)

            self.btn.clicked.connect(self.check_box_table.get_selected_data)

        def init_data(self):
            self.check_box_table.init_data()


    # - - -
    app = QApplication(sys.argv)
    my_widget = ExampleWidget()

    header_field = ['序号', '姓名', '年龄', '操作']
    my_widget.check_box_table.set_table_header_field(header_field)  # 设置表格行表头字段

    data = [
        {"name": "A", "age": "1"},
        {"name": "B", "age": "2"},
        {"name": "C", "age": "3"},
        {"name": "D", "age": "4"},
    ]
    my_widget.check_box_table.insert_rows(data, refresh_all=True)  # 尾部添加数据加数据
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n")

    data = [
        {"name": "A11", "age": "11"},
        {"name": "B22", "age": "22"},
        {"name": "C33", "age": "33"},
    ]
    # my_widget.check_box_table.insert_rows(data, refresh_all=False, specify_row=2)  # 指定行添加数据
    my_widget.check_box_table.insert_rows(data, refresh_all=False)  # 尾部添加数据加数据
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n")

    # print("总行数 = {}".format(my_widget.check_box_table.rowCount()))
    my_widget.check_box_table.insert_one_row({"name": "xxx", "age": "999"}, my_widget.check_box_table.rowCount() - 1)

    my_widget.show()
    sys.exit(app.exec_())
