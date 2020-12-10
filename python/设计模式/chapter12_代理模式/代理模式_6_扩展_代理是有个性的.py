# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 代理模式_6_扩展_代理是有个性的 --- P-143"

# TODO(tip): 一个类可以实现多个接口，完成不同任务的整合。也就是说代理类不仅可以实现主题类接口，也可以实现其他接口完成不同任务，
#            而且代理的目的是在目标对象方法的基础上做增强，这种增强的本质通常就是对目标对象的方法进行拦截和过滤。

# TODO(tip): 代理类不仅仅是可以有自己的运算方法，通常的情况下代理的职责并不一定单一，
#            它可以组合其他的真实角色，也可以实现自己的职责，比如计算费用。
#            代理类可以为真实角色预处理消息、过滤消息、消息转发、事后处理消息等。
#            当然一个代理类，也可以代理多个真实角色，并且真实角色之间可以有耦合关系。


# 代理类的接口
class IProxy(object):

    def count(self):
        """计算费用"""
        pass


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
class GamePlayerProxy(IGamePlayer, IProxy):

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
        self.count()

    def count(self):
        # 计算费用
        print(f"升级总费用是：150元")


# 强制代理的场景类
class Client(object):

    @staticmethod
    def main():
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
    client.main()
