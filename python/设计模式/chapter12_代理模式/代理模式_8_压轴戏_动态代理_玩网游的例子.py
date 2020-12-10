# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 代理模式_8_压轴戏_动态代理-玩网游的例子 --- P-145"
"""
动态代理是在实现阶段不用关心代理谁，而在运行阶段才指定代理哪一个对象。
现在有一个非常流行的名称叫做面向横切面编程，也就是AOP(Aspect Oriented Programing)，其核心就是采用了动态代理机制。
"""
from types import MethodType
from typing import ClassVar


# 游戏者接口
class IGamePlayer(object):

    def login(self, user, password):
        """登录游戏"""
        pass

    def kill_boss(self):
        """杀怪，网络游戏的主要特色"""
        pass

    def upgrade(self):
        """升级"""
        pass


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# 游戏者
class GamePlayer(IGamePlayer):

    def __init__(self, name: str):
        # 通过构造函数传递名称
        self.name = name

    def kill_boss(self):
        # 打怪，最期望的就是杀老怪
        print(f"{self.name}，在打怪！")

    def login(self, user, password):
        # 进游戏之前你肯定要哦登录的吧，这是一个必要条件
        print(f"登录名为 {user} 的用户 {self.name} 登录成功！")

    def upgrade(self):
        # 升级，升级有很多种方法，花钱买是一种，做任务也是一种
        print(f"{self.name}，又升了一级！")


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# TODO(tip): 子类继承InvocationHandler类，根据业务需求重写__call__()方法，可实现自定义的前处理、后处理等功能。
# 动态代理 Handler 类
class InvocationHandler(object):

    def __init__(self, obj, func):
        """
        :param obj: 被代理的对象
        :param func: 被代理对象的方法
        """
        self.obj = obj  # TODO：这个属性貌似没有用
        self.func = func

    def __call__(self, *args, **kwargs):
        # print('handler:', self.func, args, kwargs)
        result = self.func(*args, **kwargs)

        func_name = self.func.__name__
        if func_name == "login":
            # 如果登录方法，发送信息
            print(f"有人在用我的账号登录!")

        return result


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


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
        ret = None
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


# 动态代理场景类
class Client(object):

    @staticmethod
    def main():
        # 定义一个痴迷的玩家
        player = GamePlayer("张三")
        # 动态产生一个代理者
        proxy = DynamicProxy(player, InvocationHandler)
        # 开始打游戏，记下时间戳
        print(f"开始时间是：2009-08-25 10:45")
        # 登录
        proxy.login("zhangSan", "password")
        # 开始杀怪
        proxy.kill_boss()
        # 升级
        proxy.upgrade()
        # 记录结束游戏时间
        print(f"结束时间是：2009-08-26 03:40")


if __name__ == '__main__':
    client = Client()
    client.main()
