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
class InvocationHandler(object):
    def __init__(self, obj, func):
        self.obj = obj  # TODO：这个属性貌似没有用
        self.func = func

    def __call__(self, *args, **kwargs):
        # print('handler:', self.func, args, kwargs)
        func_name = self.func.__name__
        # if func_name == "show_info":
        #     print(f"老子的名号说出来吓死你！！！")

        result = self.func(*args, **kwargs)

        # if func_name == "show_info":
        #     print(f"吾乃常山赵子龙也！！！")
        return result


# Proxy  传入cls（被装饰类的类型）、h_cls（被装饰类的处理器类型）作为init的参数
class Proxy(object):
    def __init__(self, obj, h_cls: ClassVar[InvocationHandler]):
        self.obj = obj
        self.h_cls = h_cls
        self.handlers = dict()

    def __getattr__(self, attr):
        # print('get attr', attr)
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


class Hero(object):
    def __init__(self, name, age=18):
        self.name = name
        self.age = age

    def show_info(self):
        print(f'姓名：{self.name}，年龄：{self.age}')

    def work(self, working="打猎"):
        print(f"{self.name}，{working}!")


class Client(object):

    @staticmethod
    def main():
        zy = Hero("赵云")
        proxy = Proxy(zy, InvocationHandler)
        proxy.show_info()
        proxy.work(working='单骑救主')
        print(f"type(proxy) = {type(proxy)}")


if __name__ == '__main__':
    client = Client()
    client.main()
