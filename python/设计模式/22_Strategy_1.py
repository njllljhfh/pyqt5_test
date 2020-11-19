# -*- coding:utf-8 -*-
""" Strategy 抽象策略角色"""


class Strategy(object):

    def do_something(self):
        pass


""" ConcreteStrategy 具体策略角色"""


class StrategyA(Strategy):

    def do_something(self):
        print(f"执行 --- 策略A")


class StrategyB(Strategy):

    def do_something(self):
        print(f"执行 --- 策略B")


class StrategyC(Strategy):

    def do_something(self):
        print(f"执行 --- 策略C")


""" Context 封装角色"""


class Context(object):

    def __init__(self, strategy):
        self.strategy = strategy

    def operate(self):
        self.strategy.do_something()


if __name__ == '__main__':
    context = Context(StrategyA())
    context.operate()
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")

    context = Context(StrategyB())
    context.operate()
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")

    context = Context(StrategyC())
    context.operate()
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
