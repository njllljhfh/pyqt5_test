# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》 --- 接口隔离原则-不符合接口隔离原则 --- P-46"


# 美女接口
# TODO:接口 IPrettyGirl 的设计是有缺陷的，过于庞大了，容纳了一些可变因素，
#      根据接口隔离原则，星探 AbstractSearcher 应该依赖于具有部分特质的女孩子,
#      而我们却把这些特质都封装起来了，放到了一个接口中，过度封装了。
class IPrettyGirl(object):

    def good_looking(self):
        """要有较好的面容"""
        pass

    def nice_figure(self):
        """要有好身材"""
        pass

    def great_temperament(self):
        """要有气质"""
        pass


# 美女实现类
class PrettyGirl(IPrettyGirl):

    def __init__(self, name):
        self.name = name

    def good_looking(self):
        print(f"{self.name}---脸蛋很漂亮！")

    def nice_figure(self):
        print(f"{self.name}---身材非常好！")

    def great_temperament(self):
        print(f"{self.name}---气质非常好！")


# 星探抽象类
class AbstractSearcher(object):

    def __init__(self, pretty_girl: IPrettyGirl):
        self.pretty_girl = pretty_girl

    def show(self):
        """搜索美女累出美女信息"""
        pass


# 星探实现类
class Searcher(AbstractSearcher):

    # def __init__(self, pretty_girl: IPrettyGirl):
    #     super().__init__(pretty_girl)

    def show(self):
        print(f"-----------美女的信息如下：-----------")
        self.pretty_girl.good_looking()
        self.pretty_girl.nice_figure()
        self.pretty_girl.great_temperament()


# 场景类
class Client(object):

    @staticmethod
    def main():
        yan_yan = PrettyGirl("嫣嫣")
        searcher = Searcher(yan_yan)
        searcher.show()


if __name__ == '__main__':
    client = Client()
    client.main()
