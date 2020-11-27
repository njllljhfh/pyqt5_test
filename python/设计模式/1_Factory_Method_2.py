# -*- coding:utf-8 -*-
"""
Factory Method（工厂方法）:多个工厂
"""


#
class Human(object):

    def get_color(self):
        pass

    def talk(self):
        pass


#
class BlackHuman(Human):

    def get_color(self):
        print("黑皮肤")

    def talk(self):
        print("我是黑人")


class YellowHuman(Human):

    def get_color(self):
        print("黄皮肤")

    def talk(self):
        print("我是黄种人")


class WhiteHuman(Human):

    def get_color(self):
        print("白皮肤")

    def talk(self):
        print("我是白人")


#
class AbsHumanFactory(object):
    def create_human(self, class_human: Human):
        pass


#
class BlackHumanFactory(AbsHumanFactory):
    def create_human(self, class_human: BlackHuman) -> BlackHuman:
        return class_human()


class YellowHumanFactory(AbsHumanFactory):
    def create_human(self, class_human: YellowHuman) -> YellowHuman:
        return class_human()


class WhiteHumanFactory(AbsHumanFactory):
    def create_human(self, class_human: WhiteHuman) -> WhiteHuman:
        return class_human()


if __name__ == '__main__':
    yin_yang_lu = BlackHumanFactory()
    black_human = yin_yang_lu.create_human(BlackHuman)
    black_human.get_color()
    black_human.talk()
    print(f"{type(black_human)}")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")

    yin_yang_lu = YellowHumanFactory()
    yellow_human = yin_yang_lu.create_human(YellowHuman)
    yellow_human.get_color()
    yellow_human.talk()
    print(f"{type(yellow_human)}")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")

    yin_yang_lu = WhiteHumanFactory()
    white_human = yin_yang_lu.create_human(WhiteHuman)
    white_human.get_color()
    white_human.talk()
    print(f"{type(white_human)}")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
