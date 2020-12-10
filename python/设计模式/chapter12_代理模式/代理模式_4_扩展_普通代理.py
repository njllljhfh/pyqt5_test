# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 代理模式_4_扩展_普通代理 --- P-132"


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


# 普通代理的游戏者
class GamePlayer(IGamePlayer):

    def __init__(self, name: str, game_player: IGamePlayer = None):
        """
        :param name: 游戏者名称
        :param game_player: 代理
        """
        if not game_player:
            # TODO: 在构造函数中，传递进来一个 IGamePlayer 对象，检查谁能创建真实角色，
            #       当然还可以由其他的限制，比如类名不需为Proxy类等，读者可以根据实际情况进行扩展。
            raise TypeError("不能创建真实角色！")
        else:
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


# 普代理的代练者
class GamePlayerProxy(IGamePlayer):

    def __init__(self, name: str):
        # 通过构造函数传递用户名
        # TODO(tip): 仅仅修改了构造函数，出阿迪进来一个被代理者的名称，即可进行代理，在这种情况下，系统更加简洁了，
        #            调用者只知道地理存在就可以，不用知道代理了谁。
        try:
            self.game_player = GamePlayer(name, self)
        except Exception as e:
            # 异常处理
            pass

    def kill_boss(self):
        # 代练杀怪
        self.game_player.kill_boss()

    def login(self, user, password):
        # 代练登录
        self.game_player.login(user, password)

    def upgrade(self):
        # 代练升级
        self.game_player.upgrade()


# TODO(tip): 在该模式下，调用者只知道代理，而不用知道真实的角色是谁，屏蔽了真实角色的变更对高层模块的影响，
#            真实的主题角色想怎么修改就怎么修改，对高层次的模块没有任何影响，只要你实现了接口对应的方法，
#            该模式非常适合对扩展性要求较高的场合。
#            当然，在实际的项目中，一般都是通过约定来禁止new一个真实的角色，这也是一个非常好的方案。

# TODO(注意): 普通代理模式的约束问题，尽量通过团队内的编程规范来约束，因为一个主题类时可被重用的和可维护的，
#            使用技术约束的方式对系统维护是一种非常不利的因素。
# 普通代理的场景类
class Client(object):

    @staticmethod
    def main():
        # 定义一个代练者
        proxy = GamePlayerProxy("张三")
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
