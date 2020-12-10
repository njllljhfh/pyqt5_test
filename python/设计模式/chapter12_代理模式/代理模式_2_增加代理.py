# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 代理模式_2_增加代理 --- P-132"


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


# 代练者
class GamePlayerProxy(IGamePlayer):

    def __init__(self, player: IGamePlayer):
        self.game_player = player

    def kill_boss(self):
        # 代练杀怪
        self.game_player.kill_boss()

    def login(self, user, password):
        # 代练登录
        self.game_player.login(user, password)

    def upgrade(self):
        # 代练升级
        self.game_player.upgrade()


# 场景类
class Client(object):

    @staticmethod
    def main():
        # 定义一个痴迷的玩家
        player = GamePlayer("张三")
        # 然后再定义一个代练者
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


if __name__ == '__main__':
    client = Client()
    client.main()
