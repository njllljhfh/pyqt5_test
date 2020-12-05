# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》 --- 抽象工厂模式 --- P-95"


# 抽象产品接口（人类接口）
class Human(object):

    def get_color(self):
        """每个人种都有相应的颜色"""
        pass

    def talk(self):
        """人类会说话"""
        pass

    def get_sex(self):
        """每个人都有性别"""
        pass


# 抽象产品类
class AbstractYellowHuman(Human):

    def get_color(self):
        print("黄色人种的皮肤颜色是黄色的！")

    def talk(self):
        print("黄色人种会说话，一般说的都是双字节。")


class AbstractWhiteHuman(Human):

    def get_color(self):
        print("白色人种的皮肤颜色是白色的！")

    def talk(self):
        print("白色人种会说话，一般说的都是单字节。")


class AbstractBlackHuman(Human):

    def get_color(self):
        print("黑色人种的皮肤颜色是黑色的！")

    def talk(self):
        print("黑人会说话，一般人听不懂。")


# 每个抽象类都有两个实现类
class FemaleYellowHuman(AbstractYellowHuman):
    def get_sex(self):
        print("黄人女性。")


class MaleYellowHuman(AbstractYellowHuman):
    def get_sex(self):
        print("黄人男性。")


class FemaleWhiteHuman(AbstractWhiteHuman):
    def get_sex(self):
        print("白人女性。")


class MaleWhiteHuman(AbstractWhiteHuman):
    def get_sex(self):
        print("白人男性。")


class FemaleBlackHuman(AbstractBlackHuman):
    def get_sex(self):
        print("黑人女性。")


class MaleBlackHuman(AbstractBlackHuman):
    def get_sex(self):
        print("黑人男性。")


# 抽象工厂接口
class HumanFactory(object):
    def create_yellow_human(self):
        """制造一个黄色人种"""
        pass

    def create_white_human(self):
        """制造一个白色人种"""
        pass

    def create_black_human(self):
        """制造一个黑色人种"""
        pass


# 具体工厂类
class FemaleFactory(HumanFactory):
    """生产男性"""

    def create_yellow_human(self):
        return FemaleYellowHuman()

    def create_white_human(self):
        return FemaleWhiteHuman()

    def create_black_human(self):
        return FemaleBlackHuman()


class MaleFactory(HumanFactory):
    """生产女性"""

    def create_yellow_human(self):
        return MaleYellowHuman()

    def create_white_human(self):
        return MaleWhiteHuman()

    def create_black_human(self):
        return MaleBlackHuman()


# 场景类（女娲）
class NvWa(object):

    @classmethod
    def main(cls):
        # 男性生产工厂
        male_factory = MaleFactory()
        # 女性生产工厂
        female_factory = FemaleFactory()

        # 生产线建立完毕，开始生产人了
        print("----生产一个黄色女性----")
        female_yellow_human = female_factory.create_yellow_human()
        female_yellow_human.get_color()
        female_yellow_human.talk()
        female_yellow_human.get_sex()

        print("----生产一个黄色男性----")
        male_yellow_human = male_factory.create_yellow_human()
        male_yellow_human.get_color()
        male_yellow_human.talk()
        male_yellow_human.get_sex()
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")


if __name__ == '__main__':
    nv_wa = NvWa()
    nv_wa.main()
