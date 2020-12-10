# -*- coding:utf-8 -*-
from types import MethodType
from typing import ClassVar


# # ProxyFactory  传入h_cls（被装饰类的处理器类型）作为init的参数， 传入 cls（被装饰类的类型）作为call的参数
# class ProxyFactory(object):
#     def __init__(self, h_cls):
#         if issubclass(h_cls, InvocationHandler) or h_cls is InvocationHandler:
#             self.h_cls = h_cls
#         else:
#             raise HandlerException(h_cls)
#
#     def __call__(self, cls):
#         return Proxy(cls, self.h_cls)


# InvocationHandler 传入func（被装饰类的实例方法）作为init的参数
# class InvocationHandler(object):
#     def __init__(self, obj, func):
#         self.obj = obj  # TODO：这个属性貌似没有用
#         self.func = func
#
#     def __call__(self, *args, **kwargs):
#         print('handler:', self.func, args, kwargs)
#         return self.func(*args, **kwargs)


class InvocationHandler(object):
    def __init__(self, obj):
        self.obj = obj
        self.methods = dict()

    def invoke(self, method_name: str):
        print('get attr', method_name)
        isExist = hasattr(self.obj, method_name)
        ret = None
        if isExist:
            ret = getattr(self.obj, method_name)
            # 判断是不是方法
            if isinstance(ret, MethodType):
                if self.methods.get(method_name) is None:
                    # 生成 被代理对象方法的 代理对象
                    self.methods[method_name] = ret
                return self.methods[method_name]
            else:
                return ret
        return ret


# Proxy  传入cls（被装饰类的类型）、h_cls（被装饰类的处理器类型）作为init的参数
class Proxy(object):
    def __init__(self, obj, handler: InvocationHandler):
        self.obj = obj
        self.handler = handler

    def __getattr__(self, attr):
        return self.handler.invoke(attr)


# HandlerException 处理器异常
class HandlerException(Exception):
    def __init__(self, cls):
        super(HandlerException, self).__init__(cls, 'is not a hanlder class')


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


class Hero(object):
    def __init__(self, name, age=18):
        self.name = name
        self.age = age

    def show_info(self):
        print(f'姓名：{self.name}，年龄：{self.age}')

    def work(self, working="打猎"):
        print(f"{self.name}，{working}!")


class Client(object):

    def main(self):
        zy = Hero("赵云")
        h = InvocationHandler(zy)
        proxy = Proxy(zy, h)
        proxy.show_info()
        proxy.work(working='单骑救主')
        print(f"type(zy) = {type(zy)}")


if __name__ == '__main__':
    client = Client()
    client.main()
