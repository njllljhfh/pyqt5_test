# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 代理模式_5_扩展_强制代理 --- P-138"


# 强制代理的接口类
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

    def get_proxy(self):
        """每个人都可以找一下自己的代理"""
        pass


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# 强制代理的真实角色
class GamePlayer(IGamePlayer):

    def __init__(self, name: str):
        """
        :param name: 游戏者名称
        """
        # 通过构造函数传递名称
        self._name = name
        # 我的代理是谁
        self._proxy: IGamePlayer = None

    # TODO(tip): 这里对场景类屏蔽了代理对象
    def get_proxy(self):
        """找到自己的代理"""
        self._proxy = GamePlayerProxy(self)
        return self._proxy

    def kill_boss(self):
        # 打怪，最期望的就是杀老怪
        if self._is_proxy():
            print(f"{self._name}，在打怪！")
        else:
            print(f"请使用指定的代理访问")

    def login(self, user, password):
        # 进游戏之前你肯定要哦登录的吧，这是一个必要条件
        if self._is_proxy():
            print(f"登录名为 {user} 的用户 {self._name} 登录成功！")
        else:
            print(f"请使用指定的代理访问")

    def upgrade(self):
        if self._is_proxy():
            # 升级，升级有很多种方法，花钱买是一种，做任务也是一种
            print(f"{self._name}，又升了一级！")
        else:
            print(f"请使用指定的代理访问")

    def _is_proxy(self):
        """校验是否是代理访问"""
        if self._proxy is None:
            return False
        else:
            return True


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# TODO(tip): 代理角色也可以再次被代理
# 强制代理的代理类
class GamePlayerProxy(IGamePlayer):

    def __init__(self, game_player: IGamePlayer):
        self.game_player = game_player

    def kill_boss(self):
        # 代练杀怪
        self.game_player.kill_boss()

    def login(self, user, password):
        # 代练登录
        self.game_player.login(user, password)

    def upgrade(self):
        # 代练升级
        self.game_player.upgrade()


# 强制代理的场景类
class Client(object):

    @staticmethod
    def main_1():
        """直接访问真实角色"""
        print("- - - - - - - - - - 我们先按照常规的思路来运行一下，直接new一个真实角色 - - - - - - - - - - -")
        # TODO(tip): 不可以访问
        # 定义一个痴迷的玩家
        player = GamePlayer("张三")
        # 开始打游戏，记下时间戳
        print(f"开始时间是：2009-08-25 10:45")
        player.login("zhangSan", "password")
        # 开始杀怪
        player.kill_boss()
        # 升级
        player.upgrade()
        # 记录结束游戏时间
        print(f"结束时间是：2009-08-26 03:40")

    @staticmethod
    def main_2():
        """直接访问代理角色"""
        print("- - - - - - - - - - 直接访问代理角色 - - - - - - - - - - -")
        # TODO(tip): 不可以访问
        # 定义一个痴迷的玩家
        player = GamePlayer("张三")
        # 定义一个代练者
        proxy = GamePlayerProxy(player)
        # 开始打游戏，记下时间戳
        print(f"开始时间是：2009-08-25 10:45")
        proxy.login("zhangSan", "password")
        # 开始杀怪
        proxy.kill_boss()
        # 升级
        proxy.upgrade()
        # 记录结束游戏时间
        print(f"结束时间是：2009-08-26 03:40")

    @staticmethod
    def main_3():
        """用真实角色指定的代理访问"""
        print("- - - - - - - - - - 强制代理场景 - - - - - - - - - - -")
        # TODO(tip): 可以访问
        # TODO(tip): 强制代理的概念就是要从真实角色查找代理角色，不允许直接访问真实角色。
        #            高层模块只要调用 get_proxy 就可以访问真实角色的所有方法，
        #            它根本不需要产生一个代理出来，代理的管理已经由真实角色自己完成。
        # 定义一个痴迷的玩家
        player = GamePlayer("张三")
        # 获取指定的代理
        proxy = player.get_proxy()
        # 开始打游戏，记下时间戳
        print(f"开始时间是：2009-08-25 10:45")
        proxy.login("zhangSan", "password")
        # 开始杀怪
        proxy.kill_boss()
        # 升级
        proxy.upgrade()
        # 记录结束游戏时间
        print(f"结束时间是：2009-08-26 03:40")


if __name__ == '__main__':
    client = Client()
    # client.main_1()
    # client.main_2()
    client.main_3()
