# -*- coding:utf-8 -*-
import math
from datetime import datetime, date, timedelta
import calendar


class CalendarUtils:
    """
    日期工具类
    """

    @staticmethod
    def delta_day(delta=0):
        """
        :param delta:   偏移量
        :return:        0今天, -1昨天, -2前天, 1明天 ...
        """
        return (datetime.now() + timedelta(days=delta)).strftime('%Y-%m-%d')

    @staticmethod
    def delta_week(delta=0):
        """
        :param delta:   偏移量
        :return:        0本周, -1上周, 1下周 ...
        """
        now = datetime.now()
        week = now.weekday()
        _from = (now - timedelta(days=week - 7 * delta)).strftime('%Y-%m-%d')
        _to = (now + timedelta(days=6 - week + 7 * delta)).strftime('%Y-%m-%d')
        return _from, _to

    @staticmethod
    def delta_month(delta=0):
        """
        :param delta: 月份偏移量(0本月, -1上月, 1下月, 下下个月...)
        :return: (目标月的起始日期，目标月的结束日期)
        """

        def _delta_month(__year, __month, __delta):
            """

            :param __year: 当前年
            :param __month: 当前月
            :param __delta: 月份偏移量(0本月, -1上月, 1下月, 下下个月...)
            :return: (目标年，目标月)
            """
            _month = __month + __delta
            _year = __year
            if _month < 1:
                delta_year = math.ceil(abs(_month) / 12)
                delta_year = delta_year if delta_year else 1
                _year -= delta_year
                # _month = delta_year * 12 + __month + __delta
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

        now = datetime.now()
        _from = datetime(*_delta_month(now.year, now.month, delta), 1)

        _to = datetime(*_delta_month(_from.year, _from.month, 1), 1) - timedelta(days=1)
        # return _from.strftime('%Y-%m-%d %H:%M:%S'), _to.strftime('%Y-%m-%d %H:%M:%S')
        return _from, _to

    @staticmethod
    def delta_quarter(delta=0):
        """
        :param delta: 月份偏移量(0本月, -1上月, 1下月, 下下个月...)
        :return: (目标月的起始日期，目标月的结束日期)
        """
        pass

    @staticmethod
    def delta_year(delta=0):
        """
        :param delta:   偏移量
        :return:        0今年, -1去年, 1明年 ...
        """
        now = datetime.now()
        _from = datetime(now.year + delta, 1, 1)
        _to = datetime(_from.year + 1, 1, 1) - timedelta(days=1)
        return _from.strftime('%Y-%m-%d'), _to.strftime('%Y-%m-%d')


if __name__ == '__main__':
    print('当前日期: ', datetime.now())
    print('*' * 40)
    print('今天: ', CalendarUtils.delta_day())
    print('昨天: ', CalendarUtils.delta_day(-1))
    print('前天: ', CalendarUtils.delta_day(-2))
    print('明天: ', CalendarUtils.delta_day(1))
    print('后天: ', CalendarUtils.delta_day(2))
    print('*' * 40)
    print('本周: ', CalendarUtils.delta_week())
    print('上周: ', CalendarUtils.delta_week(-1))
    print('下周: ', CalendarUtils.delta_week(1))
    print('*' * 40)
    print('本月: ', CalendarUtils.delta_month())
    print('上月: ', CalendarUtils.delta_month(-1))
    print('下月: ', CalendarUtils.delta_month(1))
    print('2019年12月: ', CalendarUtils.delta_month(-5))
    print('2018年12月: ', CalendarUtils.delta_month(-17))
    print('2017年11月: ', CalendarUtils.delta_month(-17 - 13))
    print('0001年1月: ', CalendarUtils.delta_month(-12 * 2019 - 4))
    print('0000年12月: ', CalendarUtils.delta_month(-12 * 2019 - 5))
    print('*' * 40)
    print('本年: ', CalendarUtils.delta_year())
    print('去年: ', CalendarUtils.delta_year(-1))
    print('明年: ', CalendarUtils.delta_year(1))

    print(f"{math.ceil(0 / 12)}")
