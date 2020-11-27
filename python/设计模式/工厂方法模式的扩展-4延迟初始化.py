# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》 ---  工厂方法模式的扩展-4延迟初始化 --- P-93"

from typing import ClassVar


# 抽象产品类（人类接口）
class Human(object):

    def get_color(self):
        pass

    def talk(self):
        pass


# 具体产品类（黑色人种）
class BlackHuman(Human):

    def get_color(self):
        print("黑色人种的皮肤颜色是黑色的！")

    def talk(self):
        print("黑人会说话，一般人听不懂。")


# 具体产品类（黄色人种）
class YellowHuman(Human):

    def get_color(self):
        print("黄色人种的皮肤颜色是黄色的！")

    def talk(self):
        print("黄色人种会说话，一般说的都是双字节。")


# 具体产品类（白色人种）
class WhiteHuman(Human):

    def get_color(self):
        print("白色人种的皮肤颜色是白色的！")

    def talk(self):
        print("白色人种会说话，一般说的都是单字节。")


# 具体工厂类（人类创建工厂）
class HumanFactory(object):
    map_class_name_to_obj = dict()

    @classmethod
    def create_human(cls, human: ClassVar[Human]):
        if human.__name__ in cls.map_class_name_to_obj:
            human_obj = cls.map_class_name_to_obj.get(human.__name__)
        else:
            human_obj = human()
            cls.map_class_name_to_obj[human.__name__] = human_obj
        return human_obj


# 场景类（女娲）
class NvWa(object):

    @staticmethod
    def main():
        black_human = HumanFactory.create_human(BlackHuman)
        black_human.get_color()
        black_human.talk()
        print(f"{type(black_human)}")
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")

        yellow_human = HumanFactory.create_human(YellowHuman)
        yellow_human.get_color()
        yellow_human.talk()
        print(f"{type(yellow_human)}")
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")

        white_human = HumanFactory.create_human(WhiteHuman)
        white_human.get_color()
        white_human.talk()
        print(f"{type(white_human)}")
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")


if __name__ == '__main__':
    nv_wa = NvWa()
    nv_wa.main()
