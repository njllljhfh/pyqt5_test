# -*- coding:utf-8 -*-
from __future__ import annotations

"""
中介者模式的定义为：
    Define an object that encapsulates how a set of objects interact.
    Mediator promotes loose coupling by keeping objects from referring to each other explicitly,
    and it lets you vary their interaction independently.
    （用一个中介对象封装一系列的对象交互，中介者使各对象不需要显示地相互作用，从而使其耦合松散，而且可以独立地改变它们之间的交互。）


中介者模式的使用场景:
    中介者模式适用于多个对象之间紧密耦合的情况，紧密耦合的标准是：在类图中出现了【蜘蛛网状】结构。
    在这种情况下一定要考虑使用中介者模式，这有利于把【蜘蛛网】梳理为【星型】结构，使原本复杂混乱的关系变得清晰简单。
    
可以在如下的情况下尝试使用中介者模式：
    ● N个对象之间产生了相互的依赖关系（N＞2）。
    ● 多个对象有依赖关系，但是依赖的行为尚不确定或者有发生改变的可能，在这种情况下一般建议采用中介者模式，降低变更引起的风险扩散。
    ● 产品开发。一个明显的例子就是MVC框架，把中介者模式应用到产品中，可以提升产品的性能和扩展性，
      但是对于项目开发就未必，因为项目是以交付投产为目标，而产品则是以稳定、高效、扩展为宗旨。
"""

""" ========================== 抽象类 ========================== """


# 通用抽象中介者
class AbstractMediator(object):

    def __init__(self):
        # 定义同事类
        self.c1: ConcreteColleague1 | None = None
        self.c2: ConcreteColleague2 | None = None

    """
    在Mediator抽象类中我们只定义了同事类的注入，为什么使用同事实现类注入而不使用抽象类注入呢？
    那是因为同事类虽然有抽象，但是没有每个同事类必须要完成的业务方法，
    当然如果每个同事类都有相同的方法，比如execute、handler等，那当然注入抽象类，做到依赖倒置。
    """

    # 通过getter/setter方法把同事类注入进来
    def getC1(self):
        return self.c1

    def setC1(self, c1: ConcreteColleague1):  # 注意：这里用的是 具体同事类
        self.c1 = c1

    def getC2(self):
        return self.c2

    def setC2(self, c2: ConcreteColleague2):
        self.c2 = c2

    # 中介者模式的业务逻辑
    def doSomething1(self):
        pass

    def doSomething2(self):
        pass


"""
为什么同事类要使用构造函数注入中介者， 而中介者使用getter/setter方式注入同事类呢？
这是因为同事类必须有中介者， 而中介者却可以只有部分同事类。
"""


# 抽象同事类
class Colleague(object):
    def __init__(self, mediator: AbstractMediator):
        self.mediator = mediator


""" ========================== 具体类 ========================== """


# 通用中介者
class ConcreteMediator(AbstractMediator):
    def __init__(self):
        super(ConcreteMediator, self).__init__()

    """中介者所具有的方法 doSomething1 和 doSomething2 都是比较复杂的业务逻辑，为同事类服务，其实现是依赖各个同事类来完成的。"""

    def doSomething1(self):
        print(f'{self.__class__} --- doSomething1')
        self.c1.selfMethod1()
        self.c2.selfMethod2()

    def doSomething2(self):
        print(f'{self.__class__} --- doSomething2')
        self.c1.selfMethod1()
        self.c2.selfMethod2()


# 具体同事类1
class ConcreteColleague1(Colleague):

    def __init__(self, mediator):
        super(ConcreteColleague1, self).__init__(mediator)

    # 自有方法 self-method
    def selfMethod1(self):
        # 处理自己的业务逻辑
        print(f'{self.__class__} --- selfMethod1')

    # 依赖方法 dep-method
    def depMethod1(self):
        # 处理自己的业务逻辑
        # 自己不能处理的业务逻辑， 委托给中介者处理
        self.mediator.doSomething1()


# 具体同事类2
class ConcreteColleague2(Colleague):

    def __init__(self, mediator):
        super(ConcreteColleague2, self).__init__(mediator)

    # 自有方法 self-method
    def selfMethod2(self):
        # 处理自己的业务逻辑
        print(f'{self.__class__} --- selfMethod2')

    # 依赖方法 dep-method
    def depMethod2(self):
        # 处理自己的业务逻辑
        # 自己不能处理的业务逻辑， 委托给中介者处理
        self.mediator.doSomething2()


# 场景类
class Client(object):
    @staticmethod
    def main():
        mediator0 = ConcreteMediator()

        Colleague1 = ConcreteColleague1(mediator0)
        Colleague2 = ConcreteColleague2(mediator0)

        mediator0.setC1(Colleague1)
        mediator0.setC2(Colleague2)

        print(f'================================== Colleague1 调用方法 ==================================')
        Colleague1.selfMethod1()
        print('- ' * 10)
        Colleague1.depMethod1()

        print(f'================================== Colleague2 调用方法 ==================================')
        Colleague2.selfMethod2()
        print('- ' * 10)
        Colleague2.depMethod2()


if __name__ == '__main__':
    client = Client()
    client.main()
