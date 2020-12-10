# -*- coding:utf-8 -*-
"""
类装饰器，实现动态代理
"""
from types import MethodType
from typing import ClassVar


# 动态代理 Handler 类
# InvocationHandler 传入func（被装饰类的实例方法）作为init的参数
class InvocationHandler(object):
    def __init__(self, obj, func):
        self.obj = obj  # TODO：这个貌似没有用
        self.func = func

    def __call__(self, *args, **kwargs):
        print('handler:', self.func, args, kwargs)
        return self.func(*args, **kwargs)


# 代理工厂类
# ProxyFactory  传入h_cls（被装饰类的处理器类型）作为init的参数， 传入 cls（被装饰类的类型）作为call的参数
class ProxyFactory(object):
    def __init__(self, h_cls: ClassVar[InvocationHandler]):
        if issubclass(h_cls, InvocationHandler) or h_cls is InvocationHandler:
            self.h_cls = h_cls
        else:
            raise HandlerException(h_cls)

    def __call__(self, cls):
        return DynamicProxy(cls, self.h_cls)


# 动态代理类
# Proxy  传入cls（被装饰类的类型）、h_cls（被装饰类的处理器类型）作为init的参数
class DynamicProxy(object):
    def __init__(self, cls, h_cls: ClassVar[InvocationHandler]):
        self.cls = cls
        self.h_cls = h_cls
        self.handlers = dict()

    def __call__(self, *args, **kwargs):
        self.obj = self.cls(*args, **kwargs)
        return self

    def __getattr__(self, attr: str):
        print('get attr', attr)
        isExist = hasattr(self.obj, attr)
        ret = None
        if isExist:
            ret = getattr(self.obj, attr)
            # 判断是不是方法
            if isinstance(ret, MethodType):
                if self.handlers.get(ret) is None:
                    # 生成 被代理对象方法的 代理对象
                    self.handlers[ret] = self.h_cls(self.obj, ret)
                return self.handlers[ret]
            else:
                return ret
        return ret


# HandlerException 处理器异常
class HandlerException(Exception):
    def __init__(self, cls):
        super(HandlerException, self).__init__(cls, 'is not a hanlder class')


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# 真实主题类
@ProxyFactory(InvocationHandler)
class Sample:
    def __init__(self, age):
        self.age = age

    def foo(self):
        print('hello', self.age)

    def add(self, x, y):
        return x + y


# TODO(tip): 这种类装饰器的方式，隐藏了动态代理 Proxy 类。
# 真实主题类
@ProxyFactory(InvocationHandler)
class Hero(object):
    def __init__(self, name, age=18):
        self.name = name
        self.age = age

    def show_info(self):
        print(f'姓名：{self.name}，年龄：{self.age}')

    def work(self, time, working="打猎"):
        print(f"{time}, {self.name}, {working}!")


# 场景类
class Client(object):
    @staticmethod
    def main():
        # 可以看到 s的类型是Proxy，而不是Sample 当调用s.foo方法时， 首先调用Proxy中的getattr方法， 然后被handler的call方法处理
        # s = Sample(12)
        # print(type(s))
        # s.foo()
        # s.add(1, 2)
        # s.add(2, 4)
        # print(s.age)
        # print("- " * 35)

        zy = Hero("赵云")
        zy.show_info()
        zy.work("早上9点", working='单骑救主')
        print(f"type(zy) = {type(zy)}")


if __name__ == '__main__':
    client = Client()
    client.main()
