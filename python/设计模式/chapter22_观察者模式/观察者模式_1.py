# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 观察者模式 --- P-279"

import threading
import time


# 被观察者接口
class IHanFeiZi(object):

    def haveBreakfast(self):
        # 韩非子也是人，也要吃早饭的
        pass

    def haveFun(self):
        # 韩非子也是人，是人就要娱乐活动
        pass


# 具体的被观察者
class HanFeiZi(IHanFeiZi):

    def __init__(self):
        # 韩非子是否在吃饭，作为被监控的判断标准
        self._isHavingBreakfast = False
        # 韩非子是否在娱乐
        self._isHavingFun = False

    def haveBreakfast(self):
        print(f'韩非子：开始吃饭了。。。')
        self._isHavingBreakfast = True

    def haveFun(self):
        print(f'韩非子：开始娱乐了。。。')
        self._isHavingFun = True

    @property
    def isHavingBreakfast(self):
        return self._isHavingBreakfast

    def setHavingBreakfast(self, value: bool):
        self._isHavingBreakfast = value

    @property
    def isHavingFun(self):
        return self._isHavingFun

    def setHavingFun(self, value: bool):
        self._isHavingFun = value


# 抽象观察者接口
class ILiSi(object):
    def update(self, context: str):
        pass


# 观察者具体类
class LiSi(ILiSi):

    def update(self, context: str):
        print(f'李斯：观察到韩非子活动，开始向老板汇报了。。。')
        self._reportToQinShiHuang(context)
        print(f'李斯：汇报完毕。。。')
        print('- ' * 20)

    @staticmethod
    def _reportToQinShiHuang(reportContext):
        print(f'李斯：报告，秦老板！韩非子有活动了--->{reportContext}')


# 间谍类
class Spy(threading.Thread):

    def __init__(self, hanFeiZi, liSi, activityType):
        super().__init__()

        self._hanFeiZi: HanFeiZi = hanFeiZi
        self._liSi: LiSi = liSi
        self._type = activityType

    def run(self):
        while True:  # fixme: 死循环耗费cpu资源
            if self._type == 'breakfast':  # 监控是否在吃早餐
                if self._hanFeiZi.isHavingBreakfast:
                    self._liSi.update(f'{threading.currentThread().getName()}: 韩非子在吃饭')
                    # 重置转台继续监控
                    self._hanFeiZi.setHavingBreakfast(False)
            else:  # 监控是否在娱乐
                if self._hanFeiZi.isHavingFun:
                    self._liSi.update(f'{threading.currentThread().getName()}: 韩非子在娱乐')
                    self._hanFeiZi.setHavingFun(False)


"""=== 场景类 ==="""


# 场景类
class Client(object):

    @staticmethod
    def main():
        # 定义出韩非子和李斯
        liSi = LiSi()
        hanFeiZi = HanFeiZi()

        # 观察早餐
        watchBreakfast = Spy(hanFeiZi, liSi, 'breakfast')
        watchBreakfast.start()

        # 观察娱乐情况
        watchFun = Spy(hanFeiZi, liSi, 'fun')
        watchFun.start()

        # 然后我们看看韩非子在干什么
        time.sleep(1)  # 主线程等待1秒后再往下执行
        # 韩非子吃早餐了
        hanFeiZi.haveBreakfast()
        time.sleep(1)
        # 韩非子娱乐了
        hanFeiZi.haveFun()


if __name__ == '__main__':
    client = Client()
    client.main()
