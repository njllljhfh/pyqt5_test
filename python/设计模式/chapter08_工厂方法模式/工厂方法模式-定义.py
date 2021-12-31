# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》 --- 工厂方法模式(Factory Method) --- P-86"
"""
工厂方法模式-定义：
    Define an interface for creating an object, but let subclasses decide which class to instantiate.
    Factory Method lets a class defer instantiation to subclass.
    定义一个用于创建对象的接口，让子类决定实例化哪一个类。工厂方法使一个雷的实例化延迟到其子类。
"""

from typing import ClassVar


# TODO(tip): 该通用代码是一个比较使用，易扩展的框架，读者可以根据实际项目需要进行扩展。

# 抽象产品类
class Product(object):

    # 产品类的公共方法
    def method_1(self):
        # 业务逻辑处理
        pass

    # 抽象方法
    def method_2(self):
        pass


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# TODO(tip): 具体的产品类有多个，都继承与抽象产品类
# 具体产品类
class ConcreteProduct1(Product):

    def method_2(self):
        # 业务逻辑处理，实现
        pass


class ConcreteProduct2(Product):

    def method_2(self):
        # 业务逻辑处理，实现
        pass


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# TODO(tip): 抽象工厂负责定义产品对象的生产
# 抽象工厂类
class Creator(object):
    def create_product(self, product_class: ClassVar[Product]):
        """创建一个产品对象，其输入参数类型可以自行设置"""
        pass


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# TODO(tip): 具体如何生产一个产品的对象，是由具体工厂实现的
# 具体工厂类（人类创建工厂）
class ConcreteCreator(Creator):
    def create_product(self, product_class: ClassVar[Product]) -> Product:
        try:
            product = product_class()
            return product
        except Exception as e:
            # 处理异常
            pass


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# 场景类
class Client(object):

    @classmethod
    def main(cls):
        concrete_creator = ConcreteCreator()
        concrete_creator.create_product(ConcreteProduct1)
        # 继续业务处理
        pass


if __name__ == '__main__':
    client = Client()
    client.main()
