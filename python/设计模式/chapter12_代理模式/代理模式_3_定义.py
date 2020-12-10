# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 代理模式（Proxy Pattern）又称委托模式_3_定义 --- P-132"
"""
定义：Provide a surrogate or placeholder for another object to control access to it.
     （为其他对象提供一种代理以控制这个对象的访问。）

3中角色：
    1. Subject 抽象主题角色
    2. RealSubject 具体主题角色
    3. Proxy 代理主题角色

注意事项：
    1. 一个代理类可以代理多个被委托者或被代理者，因此一个代理类具体代理哪个真是的主题角色，是由场景类决定的。
       当然，最简单的情况就是一个主题类和一个代理类就可以了，具体代理哪个实现类由高层模块来决定，也就是在代理类的构造函数中传递被代理者。

"""


# 抽象主题类
class Subject(object):

    def request(self):
        """定义一个方法"""
        pass


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# 具体主题类
class RealSubject(Subject):

    def request(self):
        # 实现方法
        # 业务逻辑处理
        pass


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# TODO(tip): RealSubject 是一个正常的业务实现类，代理模式的核心就在代理类上。
# 代理类
class Proxy(Subject):

    def __init__(self, subject: Subject):
        if not subject:
            # 默认被代理者
            self.subject = RealSubject()
        else:
            # 要代理那个实现类，
            self.subject = subject

    def request(self):
        # 实现接口中定义的方法
        self.before()
        self.subject.request()
        self.after()

    def before(self):
        """预处理"""
        # do something
        pass

    def after(self):
        """善后处理"""
        # do something
        pass
