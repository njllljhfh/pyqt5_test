# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 模板方法模式(Template Method Pattern)-定义 --- P-110"

"""
抽象模板，它的方法分为两类:
    基本方法：
        基本方法也叫基本操作，是由子类实现的方法，并且在模板方法中被调用。
    模板方法：
        可以由一个或几个，一般是一个具体方法，也就是一个框架，实现对基本方法的调度，完成固定的逻辑。

# TODO(注意): 一般模板方法不允许被复写。
"""


# 抽象模板类
class AbstractClass(object):

    # 基本方法
    def do_something(self):
        pass

    # 基本方法
    def do_anything(self):
        pass

    # 模板方法
    def template_method(self):
        """调用基本方法，完成相关逻辑"""
        self.do_something()
        self.do_anything()


# 具体模板
class ConcreteClass1(AbstractClass):

    # 实现基本方法
    def do_something(self):
        """业务逻辑处理"""
        print("do_something_1...")

    def do_anything(self):
        """业务逻辑处理"""
        print("do_anything_1...")


class ConcreteClass2(AbstractClass):

    # 实现基本方法
    def do_something(self):
        """业务逻辑处理"""
        print("do_something_2...")

    def do_anything(self):
        """业务逻辑处理"""
        print("do_anything_2...")


# 场景类
class Client(object):

    @staticmethod
    def main():
        class1 = ConcreteClass1()
        class2 = ConcreteClass2()
        # 调用模板方法
        class1.template_method()
        class2.template_method()


if __name__ == '__main__':
    client = Client()
    client.main()
