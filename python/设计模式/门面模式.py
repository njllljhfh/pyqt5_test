# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》 ---  门面模式（又称：外观模式） --- P-295"


# 子系统
class ClassA(object):

    def do_something_a(self):
        """业务逻辑"""
        print(f"do_something_a - - - ClassA")


class ClassB(object):

    def do_something_b(self):
        """业务逻辑"""
        print(f"do_something_b - - - ClassB")


class ClassC(object):

    def do_something_c(self):
        """业务逻辑"""
        print(f"do_something_c - - - ClassC")


# 注意：门面不参与子系统内的业务逻辑
# 封装类
class Context(object):
    """该封装类的作用就是残生一个业务规则 complex_method."""

    def __init__(self):
        self.a = ClassA()
        self.c = ClassC()

    def complex_method(self):
        self.a.do_something_a()
        self.c.do_something_c()


# 门面
class Facade(object):

    def __init__(self):
        # 被委托的对象
        self.a = ClassA()
        self.b = ClassB()
        self.context = Context()

    def method_a(self):
        self.a.do_something_a()

    def method_b(self):
        self.b.do_something_b()

    def method_c(self):
        self.context.complex_method()


# 新增门面
class Facade2(object):

    def __init__(self):
        """为什么要委托而不再编写一个门面呢？在面向对象编程中，尽量保持相同的代码只写一遍，避免以后到处修改相似代码的悲剧。"""
        # 引用原有门面
        self._facade = Facade()

    def method_b(self):
        # 对外提供唯一的访问方法
        self._facade.method_b()
