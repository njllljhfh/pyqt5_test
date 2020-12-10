# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 代理模式_7_虚拟代理 --- P-145"


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


# 代理类
class Proxy(Subject):

    def __init__(self, ):
        self.subject = None

    def request(self):
        # TODO(tip): 在需要的时候才初始化对象，可以避免被代理对象较多而引起的初始化缓慢问题。
        #            其缺点是要在每个方法中判断主题对象是否被创建，这就是虚拟代理。
        # 判断一下真实主题是否初始化
        if self.subject is None:
            self.subject = RealSubject()

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
