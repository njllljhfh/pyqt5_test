# -*- coding:utf-8 -*-
import math
from datetime import datetime, date, timedelta
import calendar


class CalendarUtils:
    """
    日期工具类
    """

    @classmethod
    def delta_day(cls, delta=0):
        """
        :param delta:   偏移量
        :return:        0今天, -1昨天, -2前天, 1明天 ...
        """
        return datetime.now() + timedelta(days=delta)

    @classmethod
    def delta_week(cls, delta=0):
        """
        :param delta:   偏移量
        :return:        0本周, -1上周, 1下周 ...
        """
        now = datetime.now()
        week = now.weekday()
        _from = now - timedelta(days=week - (7 * delta))
        _to = now + timedelta(days=(6 - week) + (7 * delta))
        _to = _to.replace(hour=23, minute=59, second=59)
        return _from, _to

    @classmethod
    def delta_month(cls, delta=0):
        """
        :param delta: 月份偏移量(0本月, -1上月, 1下月, 下下个月...)
        :return: (目标月的起始日期，目标月的结束日期)
        """

        now = datetime.now()
        _from = datetime(*cls.target_month(now.year, now.month, delta), 1)
        _to = datetime(*cls.target_month(_from.year, _from.month, 1), 1) - timedelta(days=1)
        _to = _to.replace(hour=23, minute=59, second=59)
        return _from, _to

    @classmethod
    def delta_quarter(cls, delta=0):
        """
        :param delta: 季度偏移量(0本季度, -1上季度, 1下季度, 下下个季度...)
        :return: (目标季度的起始日期，目标季度的结束日期)
        """
        now = datetime.now().replace(month=4)
        year, month = cls.target_month(now.year, now.month, delta * 3)
        # print(f"{year}年,{month}月")

        quarter = math.ceil(month / 3)
        # print(f"季度 = {quarter}")

        end_month_of_quarter = quarter * 3
        start_month_of_quarter = end_month_of_quarter - 2
        # print(f"季度起始月份：{start_month_of_quarter}, 季度结束月份：{end_month_of_quarter}")

        _from = datetime(year, start_month_of_quarter, 1)
        if end_month_of_quarter == 12:
            year += 1
            end_month_of_quarter = 0
        _to = datetime(year, end_month_of_quarter + 1, 1) - timedelta(days=1)
        _to = _to.replace(hour=23, minute=59, second=59)
        return _from, _to

    @classmethod
    def delta_year(cls, delta=0):
        """
        :param delta:   偏移量
        :return:        0今年, -1去年, 1明年 ...
        """
        now = datetime.now()
        start_year = now.year + delta
        if start_year < 1:
            start_year = 1
        _from = datetime(start_year, 1, 1)
        _to = datetime(_from.year + 1, 1, 1) - timedelta(days=1)
        _to = _to.replace(hour=23, minute=59, second=59)
        return _from, _to

    @classmethod
    def target_month(cls, year, month, delta) -> (int, int):
        """
        根据月份偏移量，计算偏移后的'年'和'月'
        :param year: 当前年
        :param month: 当前月
        :param delta: 月份偏移量(0本月, -1上月, 1下月, 下下个月...)
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
    print('当前日期: ', datetime.now())
    print('*' * 40)
    print('今天: ', CalendarUtils.delta_day())
    # print('2月29: ', CalendarUtils.delta_day(-28-30-31-1))
    print('昨天: ', CalendarUtils.delta_day(-1))
    print('前天: ', CalendarUtils.delta_day(-2))
    print('明天: ', CalendarUtils.delta_day(1))
    print('后天: ', CalendarUtils.delta_day(2))
    print('*' * 40)
    print('本周: ', CalendarUtils.delta_week())
    print('上周: ', CalendarUtils.delta_week(-1))
    print('下周: ', CalendarUtils.delta_week(1))
    print('*' * 40)
    print('2019年12月: ', CalendarUtils.delta_month(-5))
    print('2018年12月: ', CalendarUtils.delta_month(-17))
    print('2017年11月: ', CalendarUtils.delta_month(-17 - 13))
    print('0001年1月: ', CalendarUtils.delta_month(-12 * 2019 - 4))
    print('0000年12月: ', CalendarUtils.delta_month(-12 * 2019 - 5))
    print('上月: ', CalendarUtils.delta_month(-1))
    print('本月: ', CalendarUtils.delta_month())
    print('下月: ', CalendarUtils.delta_month(1))
    print('2024年2月: ', CalendarUtils.delta_month(7 + 12 * (4 - 1) + 2))

    print('*' * 40)
    print('0000年: ', CalendarUtils.delta_year(-2020))
    print('0001年: ', CalendarUtils.delta_year(-2019))
    print('本年: ', CalendarUtils.delta_year(0))
    print('去年: ', CalendarUtils.delta_year(-1))
    print('明年: ', CalendarUtils.delta_year(1))

    print(f"{math.ceil(0 / 12)}")
    print("#" * 40)
    print("上1季度", CalendarUtils.delta_quarter(-1))
    print("= = = " * 6)
    print("上2季度", CalendarUtils.delta_quarter(-2))
    print("= = = " * 6)
    print("本季度", CalendarUtils.delta_quarter(0))
    print("= = = " * 6)
    print("下1季度", CalendarUtils.delta_quarter(1))
    print("= = = " * 6)
    print("下2季度", CalendarUtils.delta_quarter(2))
    print("= = = " * 6)

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    start_date, end_date = CalendarUtils.delta_quarter(0)
    print(f"本季度 = {start_date, end_date}")
    print(f"本季度_格式化 = {start_date.strftime('%Y-%m-%d %H:%M:%S'), end_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"起始: {start_date.year} 年 {start_date.month} 月 {start_date.day} 日")
    print(f"结束: {end_date.year} 年 {end_date.month} 月 {end_date.day} 日")
