# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 建造者模式(Builder Pattern)也叫生成器模式_4_定义 --- P-126"
"""
定义：Separate the construction of a complex object from its representation so that
     the same construction process create different representations.（将一个复杂对象的构建
     与它的表示分离，使得同样的构建过程可以创建不同的表示。）

在建造者模式中，有以下4中角色：
    1. Product 产品类
    2. Builder 抽象建造者
    3. ConcreteBuilder 具体建造者
    4. Director 导演类

建造者模式的注意事项：
    1.建造者模式关注的是零件类型和装配工艺（顺序），这是它与工厂方法模式最大不同的地方，虽然同为创建类模式，但是注重点不同。

    2.记住一点你就可以游刃有余的使用了：
      建造者模式最主要的功能是基本方法的调用顺序安排，也就是这些基本方法已经实现了，通俗地说就是零件的装配，顺序不同产生的对象也不同；
      而工厂方法侧重点是创建，创建零件是它的主要职责，组装顺序不是它关心的。

    3.在使用建造者模式的时候，考虑一下模板方法模式，别孤立地思考一个模式，僵化的套用一个模式会让你受害无穷。
"""


# TODO(tip): 产品类通常是一个组合或继承（如模板方法模式）产生的类
# 产品类
class Product(object):

    def do_something(self):
        """独立业务处理"""
        pass


# 抽象建造者
class AbstractBuilder(object):

    def set_part(self):
        """设置产品的不同部分，以获得不同的产品"""
        # TODO(tip): set_part方法是零件配置，什么是零件？其他的对象，获得一个不同的零件，或者不同的装配顺序就可能产生不同的产品。
        pass

    def build_product(self):
        """建造产品"""
        pass


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# TODO(tip): 需要注意的是，有几个产品类就有几个具体的建造者，而且这多个产品类具有相同接口或抽象类。
# 具体建造者
class ConcreteBuilder(AbstractBuilder):
    def __init__(self):
        self.product = Product()

    def set_part(self):
        # 产品内部的逻辑，实现
        pass

    def build_product(self):
        # 组建一个产品
        return self.product


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# TODO(tip): 导演类起到封装的作用，避免高层模块深入到建造者内部的实现类。当然，当建造者模式比较庞大时，导演类可以有多个。
# 导演类
class Director(object):
    """导演类：负责按照指定的顺序生产模型"""

    def __init__(self):
        self.builder = ConcreteBuilder()

    def get_a_product(self):
        """构建不同的产品"""
        # 设置不同的零件
        self.builder.set_part()
        return self.builder.build_product()


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# 场景类
class Client(object):

    @staticmethod
    def main():
        director = Director()
        director.get_a_product().do_something()


if __name__ == '__main__':
    client = Client()
    client.main()
