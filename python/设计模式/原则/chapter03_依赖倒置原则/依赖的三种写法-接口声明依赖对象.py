# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》 --- 依赖的三种写法-接口声明依赖对象 --- P-37"


# 汽车接口
class ICar(object):
    def run(self):
        """是汽车应该能跑"""
        pass


# 司机接口
class IDriver(object):
    def drive(self, car: ICar):
        """司机的主要职责就是驾驶汽车"""
        # TODO: 接口声明依赖对象
        car.run()


# 汽车实现类
class Benz(ICar):
    def run(self):
        print("奔驰汽车开始运行...")


class BMW(ICar):
    def run(self):
        print("宝马汽车开始运行...")


# 司机实现类
class Driver(IDriver):

    def drive(self, car: ICar):
        # TODO: ICar 是 car 参数的表面类型（在定义时赋予的类型）
        car.run()


class Client(object):

    @staticmethod
    def main():
        zhang_san = Driver()

        # TODO: Benz 是 car 参数的实际类型
        benz = Benz()
        zhang_san.drive(benz)
        # - - - - -

        # TODO: BMW 是 car 参数的实际类型
        # bmw = BMW()
        # zhang_san.drive(bmw)


if __name__ == '__main__':
    client = Client()
    client.main()
