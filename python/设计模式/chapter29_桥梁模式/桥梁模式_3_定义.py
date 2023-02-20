# -*- coding:utf-8 -*-

"""
桥梁模式的定义
桥梁模式（Bridge Pattern）也叫做桥接模式，是一个比较简单的模式，其定义如下：
Decouple an abstraction from its implementation so that the two can vary independently.
（将抽象和实现解耦，使得两者可以独立地变化。）


桥梁模式中的几个名词比较拗口，大家只要记住一句话就成：抽象角色引用实现角色，或者说抽象角色的部分实现是由实现角色完成的。
"""

""" ============================== 接口、抽象类、基类 =============================="""


# 实现化角色
class InterfaceImplementor(object):

    # 基本方法
    def doSomething(self):
        raise NotImplementedError()

    def doAnything(self):
        raise NotImplementedError()


# 抽象化角色
class Abstraction(object):

    def __init__(self, imp: InterfaceImplementor):
        # 定义对实现化角色的引用
        # 约束子类必须实现该构造函数
        self.imp = imp

    # 自身的行为
    def request(self):
        self.imp.doSomething()

    # 获得实现化角色
    def getImp(self):
        return self.imp


""" ============================== 具体类 =============================="""


# 具体实现化角色1
class ConcreteImplementor1(InterfaceImplementor):

    def doSomething(self):
        print(f'{self.__class__} --- doSomething')

    def doAnything(self):
        print(f'{self.__class__} --- doAnything')


# 具体实现化角色2
class ConcreteImplementor2(InterfaceImplementor):

    def doSomething(self):
        print(f'{self.__class__} --- doSomething')

    def doAnything(self):
        print(f'{self.__class__} --- doAnything')


# 具体抽象化角色
class RefinedAbstraction(Abstraction):

    def __init__(self, imp: InterfaceImplementor):
        super().__init__(imp)

    def request(self):
        super().request()
        self.getImp().doAnything()


# 场景类
class Client(object):
    @staticmethod
    def main():
        # 定义一个实现化角色
        imp = ConcreteImplementor1()
        # 定义一个抽象化角色
        abstraction = RefinedAbstraction(imp)
        # 执行行为
        abstraction.request()


if __name__ == '__main__':
    client = Client()
    client.main()
