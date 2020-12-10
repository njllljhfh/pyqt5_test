# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 代理模式_8_压轴戏_动态代理 --- P-148"
"""
动态代理是在实现阶段不用关心代理谁，而在运行阶段才指定代理哪一个对象。

现在有一个非常流行的名称叫做面向横切面编程，也就是AOP(Aspect Oriented Programing)，其核心就是采用了动态代理机制。

友情提示，在学习AOP框架时，弄清楚几个名词就成：切面（Aspect）、切入点（JoniPoint），
通知（Advice），织入（Weave）就够了，理解了这几个名词，应用时你就可以游刃有余了！
"""
from types import MethodType
from typing import ClassVar


# 抽象主题
class Subject(object):

    def do_something(self, work: str):
        """业务操作"""
        pass

    def do_something_2(self, work: str):
        """业务操作2"""
        pass


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# 真实主题
class RealSubject(Subject):

    def __init__(self, name, age):
        self.name = name
        self.__age = age

    def do_something(self, work):
        print(f"do something!----> {work}")

    def do_something_2(self, work):
        print(f"do something 2!----> {work}")

    @property
    def age(self):
        return self.__age


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# 通知接口类
class IAdvice(object):

    def exec(self):
        # 通知只有一个方法，执行即可
        pass


# 通知实现类
class BeforeAdvice(IAdvice):

    def exec(self):
        print(f"我是前置通知，我执行了！")


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# TODO(tip): 子类继承InvocationHandler类，根据业务需求重写__call__()方法，可实现自定义的前处理、后处理等功能。
# 动态代理 Handler 类
class InvocationHandler(object):
    """同书上的 MyInvocationHandler 类"""

    def __init__(self, obj, func):
        """
        :param obj: 被代理的对象
        :param func: 被代理对象的方法
        """
        self.obj = obj  # TODO：这个属性貌似没有用
        self.func = func

    def __call__(self, *args, **kwargs):
        """代理方法"""
        # print('handler:', self.func, args, kwargs)
        func_name = self.func.__name__

        # 寻找JoinPoint切入点，AOP框架使用元数据定义
        if func_name == "do_something":
            before_advice = BeforeAdvice()
            before_advice.exec()

        # 执行被代理的方法
        result = self.func(*args, **kwargs)

        return result


# 动态代理类
class DynamicProxy(object):

    def __init__(self, obj, h_cls: ClassVar[InvocationHandler]):
        """
        :param obj: 被代理的对象
        :param h_cls: 动态代理 Handler 类
        """
        self.obj = obj
        self.h_cls = h_cls
        self.handlers = dict()  # obj的方法 到 动态代理Handler类对象 的映射

    def __getattr__(self, attr):
        # print('get attr', attr)
        isExist = hasattr(self.obj, attr)
        ret = None  # 真实主题对象的属性
        if isExist:
            ret = getattr(self.obj, attr)
            # 判断是不是方法
            if isinstance(ret, MethodType):
                if self.handlers.get(ret) is None:
                    # 生成 被代理对象方法的 Handler对象
                    self.handlers[ret] = self.h_cls(self.obj, ret)
                return self.handlers[ret]
            else:
                return ret
        return ret


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# 具体业务的动态代理
class SubjectDynamicProxy(DynamicProxy):

    def __init__(self, obj, h_cl=InvocationHandler):
        super().__init__(obj, h_cl)


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# 动态代理场景类
class Client(object):

    @staticmethod
    def main():
        zy = RealSubject("赵云", 18)
        # proxy = DynamicProxy(zy, InvocationHandler)
        proxy = SubjectDynamicProxy(zy)
        proxy.do_something("Finish")
        print("- " * 35)

        proxy.do_something_2("Finish_2")
        print("- " * 35)

        print(f"姓名：{proxy.name}")
        print("- " * 35)

        print(f"年龄：{proxy.age}")
        print("- " * 35)

        print(f"type(proxy) = {type(proxy)}")
        print(hasattr(zy, "age"))


if __name__ == '__main__':
    client = Client()
    client.main()
