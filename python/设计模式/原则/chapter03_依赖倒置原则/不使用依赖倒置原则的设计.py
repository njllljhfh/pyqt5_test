# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》 --- chapter03_依赖倒置原则-不使用依赖倒置原则 --- P-39"
"""
    High level modules should not depend upon low level modules. Both should depend upon abstractions.
Abstractions should not depend upon details. Details should depend upon abstractions.
"""


class Benz(object):
    def run(self):
        print("奔驰汽车开始运行...")


class BMW(object):
    def run(self):
        print("宝马汽车开始运行...")


class Driver(object):

    # TODO:从设计的角度，此处的benz变量期望的类型是Benz，所以不能换成BMW类的实例对象。
    def drive(self, benz: Benz):
        """司机的主要职责就是驾驶汽车"""
        benz.run()


class Client(object):

    @staticmethod
    def main():
        zhang_san = Driver()
        benz = Benz()
        zhang_san.drive(benz)


if __name__ == '__main__':
    client = Client()
    client.main()
