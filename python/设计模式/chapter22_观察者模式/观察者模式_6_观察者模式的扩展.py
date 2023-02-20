# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 观察者模式-观察者模式的扩展"
from __future__ import annotations

from typing import List

""" ============================== 接口、基类 =============================="""


# 观察者接口
class IObserver(object):
    def update(self, observable: AbstractObservable, obj: object):
        """
        :param observable: 被观察者
        :param obj: 要传递的数据对象 DTO(Data Transfer Object)。由被观察者生成，由观察者消费。
        :return:
        """
        pass


# 被观察者抽象类
class AbstractObservable(object):
    def __init__(self):
        # 所有的观察者
        self._observerList: List[IObserver] = []

    def addObserver(self, observer: IObserver):
        """添加观察者"""
        self._observerList.append(observer)

    def deleteObserver(self, observer: IObserver):
        """删除观察者"""
        self._observerList.remove(observer)

    def notifyObservers(self, obj: object):
        """通知所有观察者"""
        for observer in self._observerList:
            observer.update(self, obj)


# 韩非子自身活动的接口
class IHanFeiZi(object):

    def haveBreakfast(self):
        # 韩非子也是人，也要吃早饭的
        pass

    def haveFun(self):
        # 韩非子也是人，是人就要娱乐活动
        pass


""" ============================== 具体类 =============================="""


# 被观察者的实现类
class HanFeiZi(IHanFeiZi, AbstractObservable):

    def haveBreakfast(self):
        print(f'韩非子：开始吃饭了。。。')
        self.notifyObservers('韩非子在吃饭')

    def haveFun(self):
        print(f'韩非子：开始娱乐了。。。')
        self.notifyObservers('韩非子在娱乐')


# 具体观察者
class LiSi(IObserver):

    def update(self, observable, obj: object):
        print(f'李斯：观察到韩非子活动，开始向老板汇报了。。。')
        self._reportToQinShiHuang(obj)
        print(f'李斯：汇报完毕。。。')
        print('- ' * 20)

    @staticmethod
    def _reportToQinShiHuang(obj: object):
        """汇报给秦始皇"""
        print(f'李斯：报告，秦老板！韩非子有活动了--->{obj}')


class WangSi(IObserver):

    def update(self, observer, obj: object):
        print(f'王斯：观察到韩非子活动，王斯自己也开始活动了。。。')
        self._cry(obj)
        print(f'王斯：哭死了。。。')
        print('- ' * 20)

    @staticmethod
    def _cry(reportContext: object):
        """一看韩非子有活动，他就痛哭"""
        print(f'王斯：因为{reportContext}，--所以我悲伤呀!')


class LiuSi(IObserver):

    def update(self, observer, obj: str):
        print(f'刘斯：观察到韩非子活动，刘斯开始动作了。。。')
        self._happy(obj)
        print(f'刘斯：乐死了')
        print('- ' * 20)

    @staticmethod
    def _happy(reportContext: str):
        """一看韩非子有活动，他就快乐"""
        print(f'刘斯：因为{reportContext}，--所以我快乐呀!')


"""============================== 场景类 =============================="""


# 场景类
class Client(object):

    @staticmethod
    def main():
        # 三个观察者
        liSi = LiSi()
        wangSi = WangSi()
        liuSi = LiuSi()

        # 定义出韩非子
        hanFeiZi = HanFeiZi()

        # 有三个人在观察韩非子
        hanFeiZi.addObserver(liSi)
        hanFeiZi.addObserver(wangSi)
        hanFeiZi.addObserver(liuSi)

        # 看看韩非子在干什么
        hanFeiZi.haveBreakfast()


if __name__ == '__main__':
    client = Client()
    client.main()
