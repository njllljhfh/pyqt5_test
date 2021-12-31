# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 观察者模式-改进后的观察者和被观察者 --- P-285"


""" ============================== 接口 =============================="""


# 观察者接口
class Observer(object):
    def update(self, context: str):
        pass


# 被观察者接口
class Observable(object):

    def addObserver(self, observer: Observer):
        # 增加一个观察者
        pass

    def deleteObserver(self, observer: Observer):
        # 删除一个观察者
        pass

    def notifyObservers(self, context: str):
        # 既然要观察，我发生改变了他也应该有所动作，通知观察者
        pass


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
class HanFeiZi(IHanFeiZi, Observable):

    def __init__(self):
        # 所有的观察者
        self._observerList = []

    def addObserver(self, observer: Observer):
        """添加观察者"""
        self._observerList.append(observer)

    def deleteObserver(self, observer: Observer):
        """删除观察者"""
        self._observerList.remove(observer)

    def notifyObservers(self, context: str):
        """通知所有观察者"""
        for observer in self._observerList:
            observer.update(context)

    def haveBreakfast(self):
        print(f'韩非子：开始吃饭了。。。')
        self.notifyObservers('韩非子在吃饭')

    def haveFun(self):
        print(f'韩非子：开始娱乐了。。。')
        self.notifyObservers('韩非子在娱乐')


# 具体观察者
class LiSi(Observer):

    def update(self, context: str):
        print(f'李斯：观察到韩非子活动，开始向老板汇报了。。。')
        self._reportToQinShiHuang(context)
        print(f'李斯：汇报完毕。。。')
        print('- ' * 20)

    @staticmethod
    def _reportToQinShiHuang(reportContext: str):
        """汇报给秦始皇"""
        print(f'李斯：报告，秦老板！韩非子有活动了--->{reportContext}')


class WangSi(Observer):

    def update(self, context: str):
        print(f'王斯：观察到韩非子活动，王斯自己也开始活动了。。。')
        self._cry(context)
        print(f'王斯：哭死了。。。')
        print('- ' * 20)

    @staticmethod
    def _cry(reportContext: str):
        """一看韩非子有活动，他就痛哭"""
        print(f'王斯：因为{reportContext}，--所以我悲伤呀!')


class LiuSi(Observer):

    def update(self, context: str):
        print(f'刘斯：观察到韩非子活动，刘斯开始动作了。。。')
        self._happy(context)
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

"""
    好了，结果正确，也符合开闭原则了，同时也实现类间解耦，
    想再加观察者，继续实现 Observer 接口接成了，这时候必须修改 Client 程序，因为你的业务发生了变化。
    这就是 观察者模式。
"""
