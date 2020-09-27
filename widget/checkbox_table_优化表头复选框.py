# -*- coding:utf-8 -*-
# __author__= "NiuJinLong"
# 优化：行复选框的enabled状态改变时，表头复选框的状态也根据情况而变化。
# 优化：可设置表头复选框是3态还是2态。
# 优化：表头复选框设置边长（这个自定义的qt在不同的windows上表现可能不一致，比如笔记本和台式机）。
# 优化：添加批量删除行方法。
import sys

from PyQt5.QtCore import Qt, pyqtSignal, QRect, pyqtSlot, QSize, QEvent
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QCheckBox, QHeaderView, QStyle, \
    QStyleOptionButton, QTableWidgetItem, QHBoxLayout, QAbstractItemView, QPushButton, QVBoxLayout


class CheckBoxHeader(QHeaderView):
    """自定义表头类:带复选框的表头"""

    # 复选框状态改变（参数1:改变后的表头复选框状态）
    check_state_change_signal = pyqtSignal(int)

    def __init__(self, orientation=Qt.Horizontal, parent=None, checkbox_side_length=16):
        """
        :param orientation: 设置为水平表头
        :param parent: 父级对象
        :param checkbox_side_length: 表头复选框边长
        """
        super().__init__(orientation, parent)
        self.check_state = Qt.Unchecked
        self.setContentsMargins(0, 0, 0, 0)

        # 这4个变量控制列头复选框的样式，位置以及大小
        self._x = 0
        self._y = 0
        self._width = checkbox_side_length
        self._height = checkbox_side_length

        # 复选框偏移量
        if self._width % 2 == 0:
            self._x_offset = 0
            self._y_offset = 0
            # self._x_offset = -1
            # self._y_offset = 1
        else:
            self._x_offset = 0
            self._y_offset = 0
            # self._x_offset = 0.5
            # self._y_offset = 0.5

        # 表头复选框是否是三态的
        self.is_tri_state = False

    @property
    def check_box_rect(self) -> QRect:
        """获取表头复选框的大小"""
        return QRect(self._x, self._y, self._width, self._height)

    def set_tri_state(self, tri_state: bool):
        """设置表头复选框是否为tri_state(三态)"""
        self.is_tri_state = tri_state

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()
        super().paintSection(painter, rect, logicalIndex)
        painter.restore()

        if logicalIndex == 0:
            # print(f"rect.x() = {rect.x()}")
            # print(f"rect.y() = {rect.y()}")
            # print(f"rect.width() = {rect.width()}")
            # print(f"rect.height() = {rect.height()}")
            # print(f"rect.center() = {rect.center()}")

            check_box_rect = QRect(
                (rect.width() - self._width + self._x_offset) / 2,
                (rect.height() - self._height + self._y_offset) / 2,
                self._width,
                self._height
            )
            self._x = check_box_rect.x()
            self._y = check_box_rect.y()

            # print(f"self._x = {self._x}")
            # print(f"self._y = {self._y}")
            # print(f"self._width = {self._width}")
            # print(f"self._height = {self._height}")

            option = QStyleOptionButton()
            option.rect = check_box_rect
            # print(f"check_box_rect.x() = {check_box_rect.x()}")
            # print(f"check_box_rect.y() = {check_box_rect.y()}")

            option.state = QStyle.State_Enabled | QStyle.State_Active
            if self.check_state == Qt.Checked:
                option.state |= QStyle.State_On
            elif self.check_state == Qt.PartiallyChecked:
                option.state |= QStyle.State_NoChange
            else:
                option.state |= QStyle.State_Off

            # self.style().drawControl(QStyle.CE_CheckBox, option, painter)
            checkBox = QCheckBox()
            self.style().drawPrimitive(QStyle.PE_IndicatorCheckBox, option, painter, checkBox)

    def mousePressEvent(self, event):
        index = self.logicalIndexAt(event.pos())
        if index == 0:
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
        """
        设置表头复选框状态
        :param check_state: Qt.Unchecked, Qt.PartiallyChecked, Qt.Checked
        :return:
        """
        if not self.is_tri_state:
            # 2态复选框的Qt.PartiallyChecked相当于Qt.Unchecked
            if check_state == Qt.PartiallyChecked:
                check_state = Qt.Unchecked

        if self.check_state != check_state:
            self.check_state = check_state
            self.updateSection(0)
            self.check_state_change_signal.emit(self.check_state)


class RowCheckBox(QCheckBox):
    # 参数1：该自定义的QCheckBox对象
    enabled_changed_signal = pyqtSignal(QCheckBox)

    def __init__(self, *args, parent=None):
        super().__init__(parent, *args)

    def changeEvent(self, event: QEvent):
        if event.type() == QEvent.EnabledChange:
            # print(f"event.type() = {event.type()}")
            # print(f"self.isEnabled() = {self.isEnabled()}")
            self.enabled_changed_signal.emit(self)

        self.update()


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
        self.all_checkbox_ls = list()
        # 已选择行的复选框对象的列表
        self.selected_checkbox_ls = list()
        # 可以点击的复选框对象的列表
        self.enabled_checkbox_ls = list()

    def set_table_header_field(self, header_field: list, checkbox_side_length: int = 16, is_tri_state: bool = False):
        """
        设置行表头字段
        :param header_field: 表头字段
        :param checkbox_side_length: 表头复选框的边长
        :param is_tri_state: 是否是3态复选框
        :return:
        """
        try:
            # 表头字段，全局变量
            if self.has_header_checkbox:
                # 表头checkbox
                header_field.insert(0, None)
                self.setColumnCount(len(header_field))  # 设置列数
                header = CheckBoxHeader(parent=self, checkbox_side_length=checkbox_side_length)  # 实例化自定义表头
                header.set_tri_state(is_tri_state)  # 3态
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
        :param refresh_all: 调用insert_rows()方法批量插入数据时，是否整表刷新
        :return:
        """
        pass

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

            self.update_header_checkbox_state()
        except Exception as e:
            self.error_signal.emit(e)

    def add_row_checkbox(self, row, row_checkbox: RowCheckBox, row_checkbox_widget: QWidget):
        """
        为每一行的第一列添加复选框
        :param row: 行号
        :param row_checkbox: 表头 QCheckBox 对象(可自定义该对象，自定义的对象继承QCheckBox类即可)
        :param row_checkbox_widget: 承载 表头QCheckBox 的 QWidget 对象(可自定义该对象，自定义的对象继承QWidget类即可)
        :return:
        """
        if row_checkbox.isEnabled() and (row_checkbox not in self.enabled_checkbox_ls):
            self.enabled_checkbox_ls.append(row_checkbox)
        if row_checkbox.checkState() == Qt.Checked and (row_checkbox not in self.selected_checkbox_ls):
            self.selected_checkbox_ls.append(row_checkbox)

        layout = QHBoxLayout(row_checkbox_widget)
        layout.addWidget(row_checkbox)
        layout.setAlignment(row_checkbox, Qt.AlignVCenter | Qt.AlignHCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setCellWidget(row, 0, row_checkbox_widget)
        self.all_checkbox_ls.append(row_checkbox)
        row_checkbox.clicked.connect(self.row_checkbox_clicked_slot(row_checkbox))
        row_checkbox.enabled_changed_signal.connect(self.row_checkbox_enabled_changed_slot)

        return row_checkbox_widget

    def row_checkbox_clicked_slot(self, checkbox: QCheckBox):
        """每行第一列QCheckBox"""

        def wrapper():
            row = self.get_row_by_row_checkbox(checkbox)
            self.selectRow(row)

            # 设置row复选框
            if checkbox.checkState() == Qt.Checked:
                self.selected_checkbox_ls.append(checkbox)
            else:
                self.selected_checkbox_ls.remove(checkbox)
            self.update_header_checkbox_state()

            # 测试调用的代码
            print(f"第{row}行的row_checkbox点击事件 - - - - - - -")
            self.get_selected_row_ls()
            # - - -

        return wrapper

    @pyqtSlot(QCheckBox)
    def row_checkbox_enabled_changed_slot(self, checkbox: QCheckBox):
        """row_checkbox的enabled改变事件"""

        if checkbox.isEnabled():
            if checkbox not in self.enabled_checkbox_ls:
                self.enabled_checkbox_ls.append(checkbox)
        else:
            if checkbox in self.enabled_checkbox_ls:
                checkbox.setCheckState(Qt.Unchecked)
                self.enabled_checkbox_ls.remove(checkbox)
            if checkbox in self.selected_checkbox_ls:
                self.selected_checkbox_ls.remove(checkbox)

        self.update_header_checkbox_state()

        # 测试调用的代码
        print(f"第{self.get_row_by_row_checkbox(checkbox)}行row_checkbox的enabled状态变为{checkbox.isEnabled()} - - - - -")
        self.get_selected_row_ls()
        # - - -

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
        """设置表头复选框"""

        if self.has_header_checkbox:
            h_header: CheckBoxHeader = self.horizontalHeader()
            if len(self.selected_checkbox_ls) == 0:
                h_header.set_check_state(Qt.Unchecked)
            elif len(self.selected_checkbox_ls) < len(self.enabled_checkbox_ls):
                if h_header.is_tri_state:
                    h_header.set_check_state(Qt.PartiallyChecked)
                else:
                    h_header.set_check_state(Qt.Unchecked)
            elif len(self.selected_checkbox_ls) == len(self.enabled_checkbox_ls):
                h_header.set_check_state(Qt.Checked)

    # 弃用
    def __update_checkbox_ls(self):
        """更新all_checkbox_ls、selected_checkbox_ls、enabled_checkbox_ls中的维护的checkbox"""

        if self.has_header_checkbox:
            self.all_checkbox_ls.clear()
            self.selected_checkbox_ls.clear()
            self.enabled_checkbox_ls.clear()
            for row in range(self.rowCount()):
                cell_widget = self.cellWidget(row, 0)
                row_checkbox: QCheckBox = cell_widget.findChild(QCheckBox)
                # 全部复选框
                self.all_checkbox_ls.append(row_checkbox)
                # 选择的复选框
                if row_checkbox.checkState() == Qt.Checked:
                    self.selected_checkbox_ls.append(row_checkbox)
                # enabled的复选框
                if row_checkbox.isEnabled():
                    self.enabled_checkbox_ls.append(row_checkbox)

            # 更新表头复选框状态
            self.update_header_checkbox_state()

            # 测试调用的代码
            self.get_selected_row_ls()
            # - - -

    @pyqtSlot(int)
    def h_header_check_state_change_handler(self, check_state):
        """
        水平表头复选框状态改变事件
        :param check_state: 改变后的表头复选框状态
        :return:
        """
        try:
            h_header: CheckBoxHeader = self.horizontalHeader()

            if self.rowCount() == 0 or len(self.enabled_checkbox_ls) == 0:
                h_header.set_check_state(Qt.Unchecked)
                return

            if check_state == Qt.Unchecked:
                if h_header.is_tri_state:
                    # 3态
                    self.selected_checkbox_ls.clear()
                    for checkbox in self.enabled_checkbox_ls:
                        checkbox.setCheckState(Qt.Unchecked)
                else:
                    # 2态
                    if len(self.selected_checkbox_ls) == len(self.enabled_checkbox_ls):
                        self.selected_checkbox_ls.clear()
                        for checkbox in self.enabled_checkbox_ls:
                            checkbox.setCheckState(Qt.Unchecked)

            elif check_state == Qt.Checked:
                self.selected_checkbox_ls.clear()
                for checkbox in self.enabled_checkbox_ls:
                    checkbox.setCheckState(Qt.Checked)
                    self.selected_checkbox_ls.append(checkbox)
            else:
                # 改变后的表头复选框状态为:Qt.PartiallyChecked,不需要处理
                pass

            # 测试调用的代码
            print("表头复选框状态改变事件 - - - - - - -")
            self.get_selected_row_ls()
            # - - -
        except Exception as e:
            self.error_signal.emit(e)

    def remove_row(self, row: int):
        """
        移除行
        :param row: 行号
        :return:
        """

        if self.has_header_checkbox:
            # 删除行之前更新缓存缓存的row_checkbox
            checkbox = self.get_row_checkbox_by_row(row)
            self.all_checkbox_ls.remove(checkbox)
            if checkbox in self.selected_checkbox_ls:
                self.selected_checkbox_ls.remove(checkbox)
            if checkbox in self.enabled_checkbox_ls:
                self.enabled_checkbox_ls.remove(checkbox)

            self.update_header_checkbox_state()
        # 删除行
        self.removeRow(row)

        # 测试调用的代码
        print(f"第{row}行删除事件 - - - - - - -")
        self.get_selected_row_ls()
        # - - -

    def remove_row_in_batch(self):
        """批量删除"""
        for row_checkbox in self.selected_checkbox_ls[:]:
            row = self.get_row_by_row_checkbox(row_checkbox)
            self.remove_row(row)

    def get_selected_row_ls(self) -> [int, ...]:
        """
        获取已选择行号的列表
        :return:
        """
        print(f"已选的行数 = {len(self.selected_checkbox_ls)}")
        selected_row_ls = [self.get_row_by_row_checkbox(combobox) for combobox in self.selected_checkbox_ls]
        selected_row_ls.sort()
        print(f"已选行号列表 = {selected_row_ls}     长度={len(selected_row_ls)}")
        enabled_row_ls = [self.get_row_by_row_checkbox(combobox) for combobox in self.enabled_checkbox_ls]
        enabled_row_ls.sort()
        print(f"可用行号列表 = {enabled_row_ls}     长度={len(enabled_row_ls)}")
        all_row_ls = [self.get_row_by_row_checkbox(combobox) for combobox in self.all_checkbox_ls]
        all_row_ls.sort()
        print(f"全部行号列表 = {all_row_ls}     长度={len(all_row_ls)}")
        print("- " * 30, "\n")
        return selected_row_ls

    def clear_data(self):
        """清除数据"""
        self.clearContents()
        self.setRowCount(0)

        if self.has_header_checkbox:
            self.all_checkbox_ls.clear()
            self.selected_checkbox_ls.clear()
            self.enabled_checkbox_ls.clear()


if __name__ == '__main__':

    # 自定义的table子类
    class MyCheckboxTable(BaseTableWidget):
        """例子:BaseTableWidget的子类"""

        def __init__(self, *args, parent=None, has_header_checkbox: bool = False):
            super().__init__(*args, parent=parent, has_header_checkbox=has_header_checkbox)

            # 一共插入过多少行数据（弃用）
            # self.serial_num_max = 0

            # 序号从几开始
            self.serial_num_offset = 0

            # 设置表的参数
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

        def init_data(self, serial_num_offset=0):

            # self.serial_num_max = 0

            self.serial_num_offset = serial_num_offset
            # self.serial_num_offset = 1

        def set_table_header_field(self, header_field: list, checkbox_side_length=16, is_tri_state=False):
            super().set_table_header_field(header_field,
                                           checkbox_side_length=checkbox_side_length,
                                           is_tri_state=is_tri_state)
            # self.horizontalHeader().setMinimumHeight(20) # 设置表头高度
            self.setColumnWidth(0, 40)  # 设置第0列宽度
            self.horizontalHeader().setFixedHeight(30)
            self.setColumnWidth(self.columnCount() - 1, 180)  # 设置操作列宽度

        def insert_one_row(self, row_data: dict, row: int, refresh_all=False):
            """自己实现"""

            self.insertRow(row)

            serial_number = row + self.serial_num_offset

            # - - -
            # if refresh_all:
            #     serial_number = row + 1
            #     self.serial_num_max = self.rowCount()
            # else:
            #     self.serial_num_max += 1
            #     serial_number = self.serial_num_max
            # print(f"self.serial_num_max = {self.serial_num_max}")
            # - - -

            # 调用父类方法添加第一列的checkbox
            if self.has_header_checkbox:
                # 第1列
                # row_checkbox = QCheckBox()
                row_checkbox = RowCheckBox()
                # - - - 不可用的checkbox - - -
                if serial_number % 2 == 0:
                    row_checkbox.setEnabled(False)
                # - - -
                row_checkbox.setProperty("name", "row_checkbox")
                row_checkbox_widget = QWidget(self)
                self.add_row_checkbox(row, row_checkbox, row_checkbox_widget)

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
            # 删除
            column_last = self._column_offset + 3  # 操作列
            delete_btn = QPushButton(self)
            delete_btn.setText("删除")
            delete_btn.setObjectName("delete_btn")  # objId
            delete_btn.setCursor(Qt.PointingHandCursor)
            delete_btn.setFixedSize(QSize(55, 20))

            # 修改行首row_checkbox的enable状态
            set_enable_status_btn = QPushButton(self)
            set_enable_status_btn.setText("改状态")
            set_enable_status_btn.setObjectName("set_enable_status_btn")  # objId
            set_enable_status_btn.setCursor(Qt.PointingHandCursor)
            set_enable_status_btn.setFixedSize(QSize(55, 20))
            if not self.has_header_checkbox:
                set_enable_status_btn.setEnabled(False)

            # 用水平布局使得单元格居中
            operation_column_btn_widget = QWidget()
            operation_column_btn_widget.setProperty("name", "operation")
            # operation_column_btn_widget.setContentsMargins(0, 0, 0, 0)
            layOut = QHBoxLayout(operation_column_btn_widget)

            layOut.addWidget(delete_btn)  # 删除-按钮
            layOut.setAlignment(delete_btn, Qt.AlignVCenter)

            layOut.addWidget(set_enable_status_btn)  # 改状态-按钮
            layOut.setAlignment(set_enable_status_btn, Qt.AlignVCenter)

            layOut.setContentsMargins(0, 0, 0, 0)
            layOut.setSpacing(2)
            self.setCellWidget(row, column_last, operation_column_btn_widget)

            # 绑定按钮事件
            delete_btn.clicked.connect(self.delete_btn_clicked_event(operation_column_btn_widget))
            set_enable_status_btn.clicked.connect(self.set_enable_status_btn_clicked_event(operation_column_btn_widget))

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

            # print(f"当前行号 = {row}")
            # print(f"当前行的序号 = {row + 1}")
            # print(f"需要更新的起始行 = {start_row}")
            # print(f"表中总行数 = {self.rowCount()}")

            # 遍历更新后面的全部行的序号
            for updated_row in range(start_row, self.rowCount()):
                new_serial_num = updated_row + self.serial_num_offset
                # print(f"下一行更新后的序号 = {new_serial_num}")
                serial_item = self.item(updated_row, self._column_offset + 0)
                serial_item.setText(str(new_serial_num))
            # print("——————————————————————————————")

        def delete_btn_clicked_event(self, operation_column_btn_widget: QWidget):
            """删除"""

            def wrapper():
                try:
                    # 获取当前点击行，任务名称的item
                    row = self._current_clicked_row(operation_column_btn_widget)
                    name_item = self.item(row, self._column_offset + 1)

                    # print(f"删除:{name_item.text()}")
                    self.remove_row(row)
                    self.update_all_back_rows_serial_number(row, plus_one=False)
                except Exception as e:
                    print(f"Error:{e}")

            return wrapper

        def delete_in_batch(self):
            """批量删除"""
            try:
                selected_row_ls = self.get_selected_row_ls()
                print(f"根据选择的行号，获取数据库id。删除数据库数据。")
                for row in selected_row_ls:
                    pass
            except Exception as e:
                print(f"Error:{e}")

            try:
                self.remove_row_in_batch()
                self.update_all_back_rows_serial_number(0, plus_one=False)
            except Exception as e:
                print(f"Error:{e}")

        def set_enable_status_btn_clicked_event(self, operation_column_btn_widget: QWidget):
            """设置row_checkbox的可用状态"""

            def wrapper():
                try:
                    # 获取当前点击行，任务名称的item
                    row = self._current_clicked_row(operation_column_btn_widget)
                    row_checkbox: RowCheckBox = self.get_row_checkbox_by_row(row)
                    row_checkbox.setEnabled(not row_checkbox.isEnabled())
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
                    # print(f"row = {row}")
                    break
            self.selectRow(row)
            return row


    # 自定义的QWidget例子
    class ExampleWidget(QWidget):
        """例子"""

        def __init__(self, parent=None, *args):
            super().__init__(parent, *args)
            layout = QVBoxLayout(self)

            layout_btn = QHBoxLayout()
            self.confirm_btn = QPushButton(self)
            self.confirm_btn.setText("确定")
            layout_btn.addWidget(self.confirm_btn)

            self.batch_rm_btn = QPushButton(self)
            self.batch_rm_btn.setText("批量删除")
            layout_btn.addWidget(self.batch_rm_btn)

            layout.addLayout(layout_btn)

            self.check_box_table = MyCheckboxTable(has_header_checkbox=True)
            # self.check_box_table = MyCheckboxTable(has_header_checkbox=False)
            layout.addWidget(self.check_box_table)

            self.setWindowTitle('带表头复选框的表')
            self.resize(600, 400)

            # qss = """
            # /**********表格样式**********/
            # MyCheckboxTable {
            #     background-color: rgb(67, 67, 67);
            #     alternate-background-color: rgb(53, 53, 53);
            #     selection-background-color: rgb(87, 87, 87);
            #     selection-color: rgb(220, 220, 220);
            #     color: rgb(220, 220, 220);
            # }
            #
            # MyCheckboxTable QHeaderView::section {
            #     background-color: rgb(53, 53, 53);
            #     color: rgb(220, 220, 220);
            # }
            # """
            # self.setStyleSheet(qss)

            self.confirm_btn.clicked.connect(self.check_box_table.get_selected_row_ls)
            self.batch_rm_btn.clicked.connect(self.check_box_table.delete_in_batch)

        def init_data(self):
            self.check_box_table.init_data(serial_num_offset=0)


    # - - -
    app = QApplication(sys.argv)
    my_widget = ExampleWidget()
    my_widget.init_data()

    header_field = ['序号', '姓名', '年龄', '操作']
    # 设置表格行表头字段
    my_widget.check_box_table.set_table_header_field(header_field, checkbox_side_length=16, is_tri_state=True)  # 3态
    # my_widget.check_box_table.set_table_header_field(header_field, checkbox_side_length=16, is_tri_state=False)  # 2态

    print("尾部插入4条数据=====================================================================\n")
    data = [
        {"name": "A", "age": "1"},
        {"name": "B", "age": "2"},
        {"name": "C", "age": "3"},
        {"name": "D", "age": "4"},
    ]
    my_widget.check_box_table.insert_rows(data, refresh_all=True)  # 尾部添加数据加数据

    print("从在3行插入3条数据=====================================================================\n")
    data = [
        {"name": "A11", "age": "11"},
        {"name": "B22", "age": "22"},
        {"name": "C33", "age": "33"},
    ]
    my_widget.check_box_table.insert_rows(data, refresh_all=False, specify_row=2)  # 指定行添加数据
    # my_widget.check_box_table.insert_rows(data, refresh_all=False)  # 尾部添加数据加数据

    print("倒数第二行插入1条数据=====================================================================\n")
    # print(f"总行数 = {my_widget.check_box_table.rowCount()}")
    my_widget.check_box_table.insert_one_row({"name": "xxx", "age": "777"}, my_widget.check_box_table.rowCount() - 1)
    my_widget.check_box_table.insert_one_row({"name": "yyy", "age": "888"}, my_widget.check_box_table.rowCount() - 1)
    my_widget.check_box_table.insert_one_row({"name": "zzz", "age": "999"}, my_widget.check_box_table.rowCount() - 1)

    my_widget.show()
    sys.exit(app.exec_())
