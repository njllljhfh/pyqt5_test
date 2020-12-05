# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》 --- 接口隔离原则-符合接口隔离原则 --- P-46"


# 美女接口
# TODO: 把美女接口拆成两个接口
# TODO: 根据接口隔离原则拆分接口时，首先必须满足单一职责原则。
class IGoodBodyGirl(object):

    def good_looking(self):
        """要有较好的面容"""
        pass

    def nice_figure(self):
        """要有好身材"""
        pass


class IGreatTemperament(object):

    def great_temperament(self):
        """要有气质"""
        pass


# 美女实现类
class PrettyGirl(IGoodBodyGirl, IGreatTemperament):

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

    def show_goodbody_girl(self, pretty_girl: IGoodBodyGirl):
        """搜索美女累出美女信息"""
        pass

    def show_great_temperament_girl(self, pretty_girl: IGreatTemperament):
        """搜索美女累出美女信息"""
        pass


# 星探实现类
class Searcher(AbstractSearcher):

    # def __init__(self, pretty_girl: IPrettyGirl):
    #     super().__init__(pretty_girl)

    def show_goodbody_girl(self, pretty_girl: IGoodBodyGirl):
        print(f"-----------外表美女的信息如下：-----------")
        pretty_girl.good_looking()
        pretty_girl.nice_figure()

    def show_great_temperament_girl(self, pretty_girl: IGreatTemperament):
        print(f"-----------气质美女的信息如下：-----------")
        pretty_girl.great_temperament()


# 场景类
class Client(object):

    @staticmethod
    def main():
        yan_yan = PrettyGirl("嫣嫣")
        yuan_yuan = PrettyGirl("圆圆")

        searcher = Searcher()
        searcher.show_goodbody_girl(yan_yan)
        print()
        searcher.show_great_temperament_girl(yuan_yuan)


if __name__ == '__main__':
    client = Client()
    client.main()
