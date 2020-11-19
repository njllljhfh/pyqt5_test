# -*- coding:utf-8 -*-
"""
Factory Method（工厂方法）:延迟初始化
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
class HumanFactory(object):
    map_class_name_to_obj = dict()

    def create_human(self, class_human: Human):
        if class_human.__name__ in self.map_class_name_to_obj:
            human_obj = self.map_class_name_to_obj.get(class_human.__name__)
        else:
            human_obj = class_human()
            self.map_class_name_to_obj[class_human.__name__] = human_obj
        return human_obj


if __name__ == '__main__':
    yin_yang_lu = HumanFactory()
    black_human = yin_yang_lu.create_human(BlackHuman)
    black_human.get_color()
    black_human.talk()
    print(f"id(black_human) = {id(black_human)}")

    black_human_1 = yin_yang_lu.create_human(BlackHuman)
    black_human_1.get_color()
    black_human_1.talk()
    print(f"id(black_human_1) = {id(black_human_1)}")
    print(f"black_human is black_human_1 : {black_human is black_human_1}")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
