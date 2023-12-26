# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 策略模式 --- P-500"


"""
策略模式-定义:
    Define a family of algorithms,encapsulate each one,and make them interchangeable.
    定义一组算法， 将每个算法都封装起来， 并且使它们之间可以互换。
"""

# 抽象策略角色（妙计接口）
class IStrategy(object):

    def operate(self):
        """每个锦囊妙计都是一个可执行的算法"""
        pass


# 具体策略角色（具体计策）
class BackDoor(IStrategy):
    """乔国老开后门"""

    def operate(self):
        print(f"找乔国老帮忙，让吴国太给孙权施加压力")


class GivenGreenLight(IStrategy):
    """吴国太开绿灯"""

    def operate(self):
        print(f"求吴国太开绿灯，放行！")


class BlockEnemy(IStrategy):
    """孙夫人断后"""

    def operate(self):
        print(f"孙夫人断后，挡住追兵！")


# 封装角色（锦囊）
class Context(object):

    def __init__(self, strategy):
        self.strategy = strategy

    def operate(self):
        self.strategy.operate()


# 使用计谋
class ZhaoYun(object):

    @staticmethod
    def main():
        print(f"--- 刚刚到吴国的时候拆第一个 ---")
        strategy = BackDoor()
        context = Context(strategy)  # 拿到锦囊妙计
        context.operate()  # 执行
        print(f"= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ")

        print(f"--- 刘备乐不思蜀了，拆第二个了 ---")
        strategy = GivenGreenLight()
        context = Context(strategy)
        context.operate()
        print(f"= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ")

        print(f"--- 孙权的小兵追了，咋办？拆第三个 ---")
        strategy = BlockEnemy()
        context = Context(strategy)
        context.operate()
        print(f"= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ")


if __name__ == '__main__':
    zhao_yun = ZhaoYun()
    zhao_yun.main()
