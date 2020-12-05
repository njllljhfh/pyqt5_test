# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》 --- 依赖的三种写法-构造函数传入依赖对象 --- P-42"


# 汽车接口
class ICar(object):
    def run(self):
        """是汽车应该能跑"""
        pass


# 司机接口
class IDriver(object):
    def drive(self):
        """司机的主要职责就是驾驶汽车"""
        pass


# 汽车实现类
class Benz(ICar):
    def run(self):
        print("奔驰汽车开始运行...")


class BMW(ICar):
    def run(self):
        print("宝马汽车开始运行...")


# 司机实现类
class Driver(object):
    def __init__(self, car: ICar):
        # TODO:构造函数传入依赖对象
        self.car = car

    def drive(self):
        self.car.run()


class Client(object):

    @staticmethod
    def main():
        benz = Benz()
        zhang_san = Driver(benz)
        zhang_san.drive()


if __name__ == '__main__':
    client = Client()
    client.main()
