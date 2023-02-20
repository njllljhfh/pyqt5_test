# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 观察者模式-通过聚集方式的被观察者 --- P-283"


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
        # 把李斯声明出来
        self._liSi: LiSi = LiSi()  # 注意：这里违背了"开闭原则"

    def haveBreakfast(self):
        print(f'韩非子：开始吃饭了。。。')
        self._liSi.update('韩非子在吃饭')

    def haveFun(self):
        print(f'韩非子：开始娱乐了。。。')
        self._liSi.update('韩非子在娱乐')


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


"""=== 场景类 ==="""


# 场景类
class Client(object):

    @staticmethod
    def main():
        # 定义出韩非子
        hanFeiZi = HanFeiZi()
        # 韩非子吃早餐了
        hanFeiZi.haveBreakfast()
        # 韩非子娱乐了
        hanFeiZi.haveFun()


if __name__ == '__main__':
    client = Client()
    client.main()

"""
该程序的设计违背了开闭原则。需要修改
"""
