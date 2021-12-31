# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》 --- 抽象工厂模式(Abstract Factory Pattern)-定义 --- P-100"
"""
抽象工厂模式-定义：
    Provide an interface for creating families of related or dependent objects
    without specifying their concrete classes.
    为创建一组相关或相互依赖的对象提供一个接口，而无需指定他们的具体类。
"""
"""
纵向扩展难：如增加一个产品C（产品族扩展）。不符合开闭原则。
横向扩展容易：如增加产品等级，只需要增加一个工厂类负责新增加出来的产品等级的产品的生产。符合开闭原则。
"""


# 抽象产品类
class AbstractProductA(object):

    def share_method(self):
        """每个产品共有的方法"""
        pass

    def do_something(self):
        """每个产品相同的方法，不同的实现"""
        pass


class AbstractProductB(object):

    def share_method_b(self):
        """每个产品共有的方法"""
        pass

    def do_something_b(self):
        """每个产品相同的方法，不同的实现"""
        pass


# 具体产品类
class ProductA1(AbstractProductA):
    """产品A1的实现类"""

    def do_something(self):
        print("产品A1的实现方法")


class ProductA2(AbstractProductA):
    """产品A2的实现类"""

    def do_something(self):
        print("产品A2的实现方法")


class ProductB1(AbstractProductB):
    """产品B1的实现类"""

    def do_something_b(self):
        print("产品B1的实现方法")


class ProductB2(AbstractProductB):
    """产品B2的实现类"""

    def do_something_b(self):
        print("产品B2的实现方法")


# 抽象工厂类
# todo(注意)：有N个产品族，在抽象工厂类中就应该有N个创建方法。
class AbstractCreator(object):
    def create_product_a(self):
        """创建A产品家族"""
        pass

    def create_product_b(self):
        """创建B产品家族"""
        pass


# 具体工厂类
# todo(注意)：有M个产品等级就应该有M个实现工厂类，在每个实现工厂中，实现不同产品族的生产任务。
class Creator1(AbstractCreator):
    """产品等级1的实现类"""

    def create_product_a(self):
        """只生产产品等级为1的A产品"""
        return ProductA1()

    def create_product_b(self):
        """只生产产品等级为1的B产品"""
        return ProductB1()


class Creator2(AbstractCreator):
    """产品等级2的实现类"""

    def create_product_a(self):
        """只生产产品等级为2的A产品"""
        return ProductA2()

    def create_product_b(self):
        """只生产产品等级为2的B产品"""
        return ProductB2()


# 场景类
class Client(object):

    @classmethod
    def main(cls):
        # 定义出两个工厂
        creator1 = Creator1()
        creator2 = Creator2()

        # 产生a1对象
        a1 = creator1.create_product_a()
        # 产生a2对象
        a2 = creator2.create_product_a()
        # 产生b1对象
        b1 = creator1.create_product_b()
        # 产生b2对象
        b2 = creator2.create_product_b()

        # 然后在这里就可以为所欲为了...


if __name__ == '__main__':
    nv_wa = Client()
    nv_wa.main()
