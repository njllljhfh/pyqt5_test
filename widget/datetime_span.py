# -*- coding:utf-8 -*-
# __author__ = "Dragon"
import sys
from datetime import datetime
from enum import unique, Enum

from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QCalendarWidget, QComboBox, QApplication, QDateTimeEdit

from calendar_utils import CalendarUtils


@unique
class DatetimeSpanField(Enum):
    """选择日期(按照：今日、本周、本月、本季度、本年度、白班、夜班)"""

    all_date = 0
    today = 1
    current_week = 2
    current_month = 3
    current_quarter = 4
    current_year = 5
    day_shift = 6
    night_shift = 7

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
            cls.day_shift.value: "白班",
            cls.night_shift.value: "夜班",
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


class DatetimeSpan(QWidget):
    """datetime选择控件"""

    def __init__(self, *args, field_ls=None, field_default=None, parent=None):
        """
        :param field_ls: 可显示的选项列表（枚举类DateSpanField的部分成员列表）
        :param field_default: 默认显示的选项（枚举类DateSpanField的某个成员）
        """
        super().__init__(parent, *args)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        # layout.setSpacing(6)

        # 时间
        self.date_label_1 = QLabel()
        self.date_label_1.setText("起止时间：")
        # self.date_label_1.setFixedSize(60, 20)
        layout.addWidget(self.date_label_1)

        # 起始日期QLineEdit
        self.start_datetime = DatetimeLineEdit(parent=self)
        # self.start_datetime.setPlaceholderText("起始日期")
        # self.start_datetime.setFixedSize(87, 23)
        layout.addWidget(self.start_datetime)

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
        self.end_datetime = DatetimeLineEdit(parent=self)
        # self.end_datetime.setPlaceholderText("结束日期")
        # self.end_datetime.setFixedSize(87, 23)
        layout.addWidget(self.end_datetime)

        #
        # self.spacer_1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # layout.addItem(self.spacer_1)

        # 选择日期(按照：今日、本周、本月、本季度、本年度)
        self.combo_box = QComboBox(parent=parent)
        # self.combo_box.setMinimumSize(80, 20)
        # self.combo_box.setFixedSize(80, 24)
        layout.addWidget(self.combo_box)

        # 绑定事件
        self.combo_box.currentIndexChanged.connect(self._slot_combo_box_current_index_changed)
        # self.combo_box.activated.connect(self._slot_combo_box_current_index_changed)  # 点击combo_box的item时触发
        self.start_datetime.dateTimeChanged.connect(self._slot_start_datetime_changed)
        self.end_datetime.dateTimeChanged.connect(self._slot_end_datetime_changed)

        # 初始化数据
        self.field_ls = field_ls
        self.field_default = field_default or self.field_ls[0]
        self._set_field()

    def _slot_start_datetime_changed(self, q_datetime: QDateTime):
        # self.end_datetime.setMinimumDateTime(datetime)
        self.end_datetime.setMinimumDate(q_datetime.date())

    def _slot_end_datetime_changed(self, q_datetime: QDateTime):
        # self.start_datetime.setMaximumDateTime(datetime)
        self.start_datetime.setMaximumDate(q_datetime.date())

    def _set_field(self):
        try:
            # 初始化datetime的选项
            self.combo_box.clear()
            for _index, date_span_field in enumerate(self.field_ls):
                self.combo_box.addItem("")
                self.combo_box.setItemText(_index,
                                           DatetimeSpanField.value_name(date_span_field.value))

            index_default = self.field_ls.index(self.field_default)
            self.combo_box.setCurrentIndex(index_default)
        except Exception as e:
            raise e

    def _slot_combo_box_current_index_changed(self, index: int):
        """
        日期范围变化-信号处理
        :param index: 日期范围QComboBox变化后的索引值
        :return: None
        """
        try:
            current_date_span_field = self.field_ls[index]

            start: datetime
            end: datetime
            if current_date_span_field == DatetimeSpanField.all_date:
                start, end = CalendarUtils.delta_all_date()
                # print(f"全部 = {start, end}")
            elif current_date_span_field == DatetimeSpanField.today:
                start, end = CalendarUtils.delta_day(0)
                # print(f"今日 = {start, end}")
            elif current_date_span_field == DatetimeSpanField.current_week:
                start, end = CalendarUtils.delta_week(0)
                # print(f"本周 = {start, end}")
            elif current_date_span_field == DatetimeSpanField.current_month:
                start, end = CalendarUtils.delta_month(0)
                # print(f"本月 = {start, end}")
            elif current_date_span_field == DatetimeSpanField.current_quarter:
                start, end = CalendarUtils.delta_quarter(0)
                # print(f"本季度 = {start, end}")
            elif current_date_span_field == DatetimeSpanField.current_year:
                start, end = CalendarUtils.delta_year(0)
                # print(f"本年度 = {start, end}")
            elif current_date_span_field == DatetimeSpanField.day_shift:
                start, end = CalendarUtils.day_shift()
                # print(f"白班 = {start, end}")
            elif current_date_span_field == DatetimeSpanField.night_shift:
                start, end = CalendarUtils.night_shift(datetime.now())
                # print(f"夜班 = {start, end}")
            else:
                raise ValueError(f"日期范围错误：{index}")

            # 年月日时分秒
            start_q_datetime = QDateTime(start)
            end_q_datetime = QDateTime(end)
            self.set_datetime_range(start_q_datetime, end_q_datetime)

            # s = self.get_start_datetime()
            # e = self.get_end_datetime()
            # print(f"{self.combo_box.currentText()}:")
            # print("开始时间：", str(s), type(s))
            # print(f"开始时间_格式化 = {s.strftime('%Y-%m-%d %H:%M:%S')}")
            # print("结束时间：", str(e), type(e))
            # print(f"开始时间_格式化 = {e.strftime('%Y-%m-%d %H:%M:%S')}")
            # print("=" * 30)
        except Exception as e:
            raise e

    def set_datetime_range(self, start: QDateTime, end: QDateTime):
        """
        设置起始datetime、结束datetime
        :param start: 起始datetime
        :param end: 结束datetime
        :return: None
        """
        try:
            self.start_datetime.date = start
            self.end_datetime.date = end
        except Exception as e:
            raise e

    def get_start_datetime(self):
        """获取起始datetime"""
        q_datetime_start: QDateTime = self.start_datetime.date
        datetime_start: datetime = q_datetime_start.toPyDateTime()
        return datetime_start

    def get_end_datetime(self):
        """获取截止datetime"""
        q_datetime_end: QDateTime = self.end_datetime.date
        datetime_end: datetime = q_datetime_end.toPyDateTime()
        return datetime_end

    def set_option(self, option: DatetimeSpanField):
        try:
            index_default = self.field_ls.index(option)
            self.combo_box.setCurrentIndex(index_default)
        except ValueError:
            raise ValueError("不存在此选项")


class DatetimeLineEdit(QDateTimeEdit):
    def __init__(self, *args, **kwargs):
        super(DatetimeLineEdit, self).__init__(*args, **kwargs)

        self.setCalendarPopup(True)
        self.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.calendarWidget().setVerticalHeaderFormat(QCalendarWidget.ISOWeekNumbers)

    @property
    def date(self):
        return self.dateTime()

    @date.setter
    def date(self, value):
        self.setDateTime(value)


def judge_current_shift():
    now = datetime.now()
    day_shift_start, day_shift_end = CalendarUtils.day_shift()
    if day_shift_start <= now <= day_shift_end:
        return DatetimeSpanField.day_shift
    else:
        return DatetimeSpanField.night_shift


if __name__ == '__main__':
    app = QApplication(sys.argv)

    date_span_field_ls = [
        DatetimeSpanField.today,
        DatetimeSpanField.day_shift,
        DatetimeSpanField.night_shift,
        DatetimeSpanField.current_week,
        DatetimeSpanField.current_month,
        DatetimeSpanField.current_quarter,
        DatetimeSpanField.current_year
    ]
    my_widget = DatetimeSpan(field_ls=date_span_field_ls)
    my_widget.show()

    try:
        # current_shift = 123
        current_shift = judge_current_shift()
        my_widget.set_option(current_shift)
    except Exception as e:
        print(e)

    sys.exit(app.exec_())
