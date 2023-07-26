# -*- coding:utf-8 -*-
# __author__ = "Dragon"
import sys
from datetime import datetime, date
from enum import unique, Enum

from PyQt5.QtCore import QDate, Qt, pyqtSlot
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QCalendarWidget, QComboBox, QApplication

from calendar_utils import CalendarUtils


@unique
class DateSpanField(Enum):
    """选择日期(按照：今日、本周、本月、本季度、本年度)"""

    all_date = 0
    today = 1
    current_week = 2
    current_month = 3
    current_quarter = 4
    current_year = 5

    @classmethod
    def value_name(cls, value):
        """ Map value to Str. """
        value_map = {
            cls.all_date.value: "全部",
            cls.today.value: "今日",
            cls.current_week.value: "本周",
            cls.current_month.value: "本月",
            cls.current_quarter.value: "本季度",
            cls.current_year.value: "本年度",
        }
        return value_map.get(value)

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


class DateSpan(QWidget):
    """日期范围选择控件"""

    def __init__(self, *args, parent=None):
        super().__init__(parent, *args)
        # 初始化数据
        self.field_ls = [date_span_field for date_span_field in DateSpanField]
        self.field_default = DateSpanField.current_year
        # - - -
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        # layout.setSpacing(6)

        # 时间
        self.date_label_1 = QLabel()
        self.date_label_1.setText("起止时间：")
        # self.date_label_1.setFixedSize(60, 20)
        layout.addWidget(self.date_label_1)

        # 起始日期QLineEdit
        self.start_date_line_edit = DateLineEdit(parent=self)
        self.start_date_line_edit.setPlaceholderText("起始日期")
        # self.start_date_line_edit.setFixedSize(87, 23)
        layout.addWidget(self.start_date_line_edit)

        # 至
        # width = 8  # 至label的左右间隙
        # self.spacer_1 = QSpacerItem(width, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        # layout.addItem(self.spacer_1)

        self.date_label_2 = QLabel()
        self.date_label_2.setText("至")
        # self.date_label_2.setFixedHeight(20)
        # self.date_label_2.adjustSize()
        layout.addWidget(self.date_label_2)

        # self.spacer_2 = QSpacerItem(width, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        # layout.addItem(self.spacer_2)

        # 结束日期QLineEdit
        self.end_date_line_edit = DateLineEdit(parent=self)
        self.end_date_line_edit.setPlaceholderText("结束日期")
        # self.end_date_line_edit.setFixedSize(87, 23)
        layout.addWidget(self.end_date_line_edit)

        #
        # self.spacer_1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # layout.addItem(self.spacer_1)

        # 选择日期(按照：今日、本周、本月、本季度、本年度)
        self.combo_box = QComboBox(parent=parent)
        # self.combo_box.setMinimumSize(80, 20)
        # self.combo_box.setFixedSize(80, 24)
        layout.addWidget(self.combo_box)

        # 绑定事件
        self.start_date_line_edit.calendar.clicked.connect(self.start_date_line_edit_change_event_handler)
        self.end_date_line_edit.calendar.clicked.connect(self.end_date_line_edit_change_event_handler)
        self.combo_box.currentIndexChanged.connect(self.combo_box_current_index_changed_handler)
        self.combo_box.activated.connect(self.combo_box_current_index_changed_handler)  # 点击combo_box的item时触发

        # 初始化ui及数据
        self.set_field()

    def set_field(self, field_ls=None, field_default=None):
        """
        设置可选择的时间范围选项（使用方式见下方例子）
        :param field_ls: 可显示的选项列表（枚举类DateSpanField的部分成员列表）
        :param field_default: 默认显示的选项（枚举类DateSpanField的某个成员）
        :return:
        """

        try:
            self.field_ls = field_ls or self.field_ls
            self.field_default = field_default or self.field_default

            index_default = self.field_ls.index(self.field_default)

            # 初始化选择日期(按照：今日、本周、本月、本季度、本年度)
            self.combo_box.clear()
            for _index, date_span_field in enumerate(self.field_ls):
                self.combo_box.addItem("")
                self.combo_box.setItemText(_index,
                                           DateSpanField.value_name(date_span_field.value))
            self.combo_box.setCurrentIndex(index_default)
        except Exception as e:
            raise e

    def combo_box_current_index_changed_handler(self, index: int):
        """
        日期范围变化-信号处理
        :param index: 日期范围QComboBox变化后的索引值
        :return: None
        """
        try:
            current_date_span_field = self.field_ls[index]

            if current_date_span_field == DateSpanField.all_date:
                start_date, end_date = CalendarUtils.delta_all_date()
                # print(f"全部 = {start_date, end_date}")
            elif current_date_span_field == DateSpanField.today:
                start_date, end_date = CalendarUtils.delta_day(0)
                # print(f"今日 = {start_date, end_date}")
            elif current_date_span_field == DateSpanField.current_week:
                start_date, end_date = CalendarUtils.delta_week(0)
                # print(f"本周 = {start_date, end_date}")
            elif current_date_span_field == DateSpanField.current_month:
                start_date, end_date = CalendarUtils.delta_month(0)
                # print(f"本月 = {start_date, end_date}")
            elif current_date_span_field == DateSpanField.current_quarter:
                start_date, end_date = CalendarUtils.delta_quarter(0)
                # print(f"本季度 = {start_date, end_date}")
            elif current_date_span_field == DateSpanField.current_year:
                start_date, end_date = CalendarUtils.delta_year(0)
                # print(f"本年度 = {start_date, end_date}")
            else:
                raise ValueError(f"日期范围错误：{index}")

            start_q_date = QDate(start_date.year, start_date.month, start_date.day)
            end_q_date = QDate(end_date.year, end_date.month, end_date.day)

            self.set_date_range(start_q_date, end_q_date)
            # start_date_str = start_date.strftime("%Y%m%d%H%M%S")
            # end_date_str = end_date.strftime("%Y%m%d%H%M%S")
            # print(f'start_date = {start_date_str}')
            # print(f'end_date = {end_date_str}')
            # print(f"start_q_date = {start_q_date}")
            # print(f"end_q_date = {end_q_date}")
        except Exception as e:
            raise e

    def set_date_range(self, start_q_date: QDate, end_q_date: QDate):
        """
        设置起止日期、结束日期、起始日期的最小值、结束日期的最大值
        :param start_q_date: 起始日期
        :param end_q_date: 结束日期
        :return: None
        """
        try:
            # print(f"start_q_date = {start_q_date}")
            # print(f"end_q_date = {end_q_date}")
            # 1.先设置日期范围
            self.start_date_line_edit_change_event_handler(start_q_date)  # 设置结束日期的最小时间
            self.end_date_line_edit_change_event_handler(end_q_date)  # 设置起始日期的最大时间
            # 2.在设置日期范围
            self.end_date_line_edit.calendar.setSelectedDate(end_q_date)  # 选择结束日期
            self.start_date_line_edit.calendar.setSelectedDate(start_q_date)  # 选择起始日期
            # 3.最后设置QLineEdit的文字
            self.start_date_line_edit.slot_select_date(start_q_date)  # 设置起始日期QLineEdit的文字
            self.end_date_line_edit.slot_select_date(end_q_date)  # 设置结束日期QLineEdit的文字
        except Exception as e:
            raise e

    def start_date_line_edit_change_event_handler(self, q_ate: QDate):
        """设置结束日期的最小时间"""
        try:
            # 设置结束日期的最小时间
            self.end_date_line_edit.set_min_date(q_ate)
        except Exception as e:
            raise e

    def end_date_line_edit_change_event_handler(self, q_ate: QDate):
        """设置起始日期的最大时间"""
        try:
            # 设置起始日期的最大时间
            self.start_date_line_edit.set_max_date(q_ate)
        except Exception as e:
            raise e

    def get_start_datetime(self):
        """获取起始时间"""
        q_date_start: date = self.start_date_line_edit.calendar.selectedDate().toPyDate()
        date_start: datetime = datetime.strptime(q_date_start.strftime('%Y%m%d') + '000000', '%Y%m%d%H%M%S')
        return date_start

    def get_end_datetime(self):
        """获取截止时间"""
        q_date_end: date = self.end_date_line_edit.calendar.selectedDate().toPyDate()
        date_end: datetime = datetime.strptime(q_date_end.strftime('%Y%m%d') + '235959', '%Y%m%d%H%M%S')
        return date_end


class DateLineEdit(QLineEdit):
    """带日期选择的QLineEdit"""

    def __init__(self, *args, parent=None):
        super().__init__(parent, *args)
        self.setFocusPolicy(Qt.NoFocus)
        self.calendar = CalendarWidget()
        self.calendar.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        # self.date = None
        self.calendar.clicked.connect(self.slot_select_date)

    @pyqtSlot(QDate)
    def slot_select_date(self, q_ate: QDate):
        """设置QLineEdit的文字"""
        # self.date = date
        self.setText("%04d-%02d-%02d" % (q_ate.year(), q_ate.month(), q_ate.day()))

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)

        gx, gy = event.globalX(), event.globalY()
        tx = gx - event.x()  # event.x()：鼠标在QLineEdit中的位置
        ty = gy - event.y() + self.height()
        if not self.calendar.isVisible():
            # 如果不可见
            self.calendar.setGeometry(tx, ty, 260, 260)
            self.calendar.show()

    def set_min_date(self, q_ate: QDate):
        self.calendar.setMinimumDate(q_ate)

    def set_max_date(self, q_ate: QDate):
        self.calendar.setMaximumDate(q_ate)

    # def focusInEvent(self, event: QFocusEvent):
    #     print("focusInEvent")
    #     super().focusInEvent(event)
    #
    # def focusOutEvent(self, event: QFocusEvent):
    #     print("focusOutEvent")
    #     super().focusOutEvent(event)
    #     self.calendar.close()
    #
    # def keyPressEvent(self, event: QKeyEvent):
    #     pass


class CalendarWidget(QCalendarWidget):
    """日期控件"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.activated.connect(self.activated_handler)

    @pyqtSlot(QDate)
    def activated_handler(self, q_ate: QDate):
        """双击鼠标关闭QCalendarWidget"""
        # print(f"双击CalendarWidget")
        if self.isVisible():
            self.close()

    # def mousePressEvent(self, event: QMouseEvent):
    #     super().mousePressEvent(event)
    #     if event.button() == Qt.RightButton:
    #         if self.isVisible():
    #             self.close()
    #
    # def mouseDoubleClickEvent(self, *args, **kwargs):
    #     super().mouseDoubleClickEvent(*args, **kwargs)
    #     if self.isVisible():
    #         self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    my_widget = DateSpan()
    date_span_field_ls = [DateSpanField.today,
                          DateSpanField.current_week,
                          DateSpanField.current_month,
                          DateSpanField.current_quarter,
                          DateSpanField.current_year]
    date_span_field_default = DateSpanField.current_year
    my_widget.set_field(field_ls=date_span_field_ls, field_default=date_span_field_default)
    my_widget.show()

    sys.exit(app.exec_())
