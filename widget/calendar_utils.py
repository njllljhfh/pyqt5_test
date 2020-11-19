# -*- coding:utf-8 -*-
# __author__ = njl
import math
from datetime import datetime, timedelta


class CalendarUtils(object):
    """
    日期工具类
    """

    @classmethod
    def delta_day(cls, delta: int = 0) -> (datetime, datetime):
        """
        根据偏移量获取日期
        :param delta: 日期偏移量(0今天, -1昨天, -2前天, 1明天, 2后天, ...)
        :return:
        """
        _from = datetime.now() + timedelta(days=delta)
        _from = _from.replace(hour=0, minute=0, second=0, microsecond=0)

        _to = _from.replace(hour=23, minute=59, second=59, microsecond=99999)
        return _from, _to

    @classmethod
    def delta_week(cls, delta: int = 0) -> (datetime, datetime):
        """
        根据偏移量获取目标周的日期范围
        :param delta: 周偏移量(0本周, -1上周, -2上上周, 1下周, 2下下周, ...)
        :return:
        """
        now = datetime.now()
        week = now.weekday()

        _from = now - timedelta(days=week - (7 * delta))
        _from = _from.replace(hour=0, minute=0, second=0, microsecond=0)

        _to = now + timedelta(days=(6 - week) + (7 * delta))
        _to = _to.replace(hour=23, minute=59, second=59, microsecond=99999)
        return _from, _to

    @classmethod
    def delta_month(cls, delta: int = 0) -> (datetime, datetime):
        """
        根据偏移量获取目标月的日期范围
        :param delta: 月份偏移量(0本月, -1上月, -2上上月，1下月, 2下下月, ...)
        :return: (目标月的起始日期，目标月的结束日期)
        """

        now = datetime.now()
        _from = datetime(*cls._target_month(now.year, now.month, delta), 1)
        _to = datetime(*cls._target_month(_from.year, _from.month, 1), 1) - timedelta(days=1)
        _to = _to.replace(hour=23, minute=59, second=59, microsecond=99999)
        return _from, _to

    @classmethod
    def delta_quarter(cls, delta: int = 0) -> (datetime, datetime):
        """
        根据偏移量获取目标季度的日期范围
        :param delta: 季度偏移量(0本季度, -1上季度, -2上上季度, 1下季度, 2下下季度, ...)
        :return: (目标季度的起始日期，目标季度的结束日期)
        """
        now = datetime.now()

        # 调用接口的日期所在的年月
        year, month = cls._target_month(now.year, now.month, delta * 3)

        # 调用接口的日期所在的季度
        quarter = int(math.ceil(month / 3))

        # 调用接口的日期所在的季度的首月
        end_month_of_quarter = quarter * 3

        # 调用接口的日期所在的季度的末月
        start_month_of_quarter = end_month_of_quarter - 2

        _from = datetime(year, start_month_of_quarter, 1)

        if end_month_of_quarter == 12:
            year += 1
            end_month_of_quarter = 0
        _to = datetime(year, end_month_of_quarter + 1, 1) - timedelta(days=1)
        _to = _to.replace(hour=23, minute=59, second=59, microsecond=99999)
        return _from, _to

    @classmethod
    def delta_year(cls, delta: int = 0) -> (datetime, datetime):
        """
        根据偏移量获取目标年度的日期范围
        :param delta: 年偏移量(0今年, -1去年, -2前年，1明年, 2后年, ...)
        :return:
        """
        now = datetime.now()
        start_year = now.year + delta
        if start_year < 1:
            start_year = 1
        _from = datetime(start_year, 1, 1)
        _to = datetime(_from.year + 1, 1, 1) - timedelta(days=1)
        _to = _to.replace(hour=23, minute=59, second=59, microsecond=99999)
        return _from, _to

    @classmethod
    def delta_all_date(cls) -> (datetime, datetime):
        """
        获取截止到今天为止的全部日期范围
        :return:
        """
        _from = datetime(1, 1, 1)
        _to = datetime.now()
        _to = _to.replace(hour=23, minute=59, second=59, microsecond=99999)
        return _from, _to

    @classmethod
    def _target_month(cls, year: int, month: int, delta: int) -> (int, int):
        """
        根据月份偏移量，计算偏移后的'年'和'月'
        :param year: 当前年
        :param month: 当前月
        :param delta: 月份偏移量(0本月, -1上月, -2上上月, 1下月, 2下下月...)
        :return: (目标年, 目标月)
        """
        _month = month + delta
        _year = year
        if _month < 1:
            delta_year = math.ceil(abs(_month) / 12)
            delta_year = delta_year if delta_year else 1
            _year -= delta_year
            _month = delta_year * 12 + _month
            if _month == 0:
                _month = 12  # 0月表示上一年的12月
                _year -= 1  # 年份减去1
                if _year < 1:
                    _month = 1
                    _year = 1
        elif _month > 12:
            delta_year = math.floor(_month / 12)
            _year += delta_year
            _month %= 12
        return _year, _month


if __name__ == '__main__':
    print("{:<8s}\t{}".format("当前日期:", datetime.now()))
    print("*" * 60)

    print("{:<8s}\t{}".format("全部日期:", CalendarUtils.delta_all_date()))
    print("*" * 60)

    print("{:<8s}\t{}".format("前天:", CalendarUtils.delta_day(-2)))
    print("{:<8s}\t{}".format("昨天:", CalendarUtils.delta_day(-1)))
    print("{:<8s}\t{}".format("今天:", CalendarUtils.delta_day()))
    print("{:<8s}\t{}".format("明天:", CalendarUtils.delta_day(1)))
    print("{:<8s}\t{}".format("后天:", CalendarUtils.delta_day(2)))
    print("*" * 60)

    print("{:<8s}\t{}".format("上上周:", CalendarUtils.delta_week(-2)))
    print("{:<8s}\t{}".format("上周:", CalendarUtils.delta_week(-1)))
    print("{:<8s}\t{}".format("本周:", CalendarUtils.delta_week()))
    print("{:<8s}\t{}".format("下周:", CalendarUtils.delta_week(1)))
    print("{:<8s}\t{}".format("下下周:", CalendarUtils.delta_week(2)))
    print("*" * 60)

    print("{:<8s}\t{}".format("上上月:", CalendarUtils.delta_month(-2)))
    print("{:<8s}\t{}".format("上月:", CalendarUtils.delta_month(-1)))
    print("{:<8s}\t{}".format("本月:", CalendarUtils.delta_month()))
    print("{:<8s}\t{}".format("下月:", CalendarUtils.delta_month(1)))
    print("{:<8s}\t{}".format("下下月:", CalendarUtils.delta_month(2)))
    print("*" * 60)

    print("{:<8s}\t{}".format("0001年:", CalendarUtils.delta_year(-2019)))
    print("{:<8s}\t{}".format("前年:", CalendarUtils.delta_month(-2)))
    print("{:<8s}\t{}".format("去年:", CalendarUtils.delta_month(-1)))
    print("{:<8s}\t{}".format("本年:", CalendarUtils.delta_month()))
    print("{:<8s}\t{}".format("明年:", CalendarUtils.delta_month(1)))
    print("{:<8s}\t{}".format("后年:", CalendarUtils.delta_month(2)))
    print("*" * 60)

    print("{:<8s}\t{}".format("上上季度:", CalendarUtils.delta_quarter(-2)))
    print("{:<8s}\t{}".format("上季度:", CalendarUtils.delta_quarter(-1)))
    print("{:<8s}\t{}".format("本季度:", CalendarUtils.delta_quarter()))
    print("{:<8s}\t{}".format("下季度:", CalendarUtils.delta_quarter(1)))
    print("{:<8s}\t{}".format("下下季度:", CalendarUtils.delta_quarter(2)))
    print("*" * 60)

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    start_date, end_date = CalendarUtils.delta_quarter(0)
    print(f"本季度 = {start_date, end_date}")
    print(f"本季度_格式化 = {start_date.strftime('%Y-%m-%d %H:%M:%S'), end_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"起始: {start_date.year} 年 {start_date.month} 月 {start_date.day} 日")
    print(f"结束: {end_date.year} 年 {end_date.month} 月 {end_date.day} 日")

    print(f"type(start_date.strftime('%Y-%m-%d %H:%M:%S')) = {type(start_date.strftime('%Y-%m-%d %H:%M:%S'))}")
