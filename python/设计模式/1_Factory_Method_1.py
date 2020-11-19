# -*- coding:utf-8 -*-
"""
Factory Method（工厂方法）

意图：
定义一个用于创建对象的接口，让子类决定实例化哪一个类。Factory Method 使一个类的实例化延迟到其子类。


适用性：
当一个类不知道它所必须创建的对象的类的时候。
当一个类希望由它的子类来指定它所创建的对象的时候。
当类将创建对象的职责委托给多个帮助子类中的某一个，并且你希望将哪一个帮助子类是代理者这一信息局部化的时候。
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
class HumanFactor(AbsHumanFactory):
    def create_human(self, class_human: Human) -> Human:
        return class_human()


if __name__ == '__main__':
    yin_yang_lu = HumanFactor()

    black_human = yin_yang_lu.create_human(BlackHuman)
    black_human.get_color()
    black_human.talk()
    print(f"{type(black_human)}")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")

    yellow_human = yin_yang_lu.create_human(YellowHuman)
    yellow_human.get_color()
    yellow_human.talk()
    print(f"{type(yellow_human)}")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")

    white_human = yin_yang_lu.create_human(WhiteHuman)
    white_human.get_color()
    white_human.talk()
    print(f"{type(white_human)}")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
