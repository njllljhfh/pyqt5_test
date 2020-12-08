# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 建造者模式_3_添加导演类 --- P-123"

from enum import unique, Enum
from typing import List


# run顺序枚举类
@unique
class RunOrder(Enum):
    start = 0  # 开始
    stop = 1  # 停止
    alarm = 2  # 喇叭
    engine_boom = 3  # 引擎


# TODO(tip): 抽象模板类（模板方法模式）
# 抽象车辆模型类
class CarModel(object):

    def __init__(self):
        self.sequence: List[int] = list()

    def start(self):
        """首先，这个模型要能被发动起来，别管是手摇发动，还是电力发动，反正是要能发动起来，那这个实现要在实现类里了"""
        pass

    def stop(self):
        """能发动，还要能停下来，那才叫真本事"""
        pass

    def alarm(self):
        """喇叭会出声音，是滴滴叫，还是哗哗叫"""
        pass

    def engine_boom(self):
        """引擎会轰隆隆的响，不响那是假的"""
        pass

    def run(self):
        """模型应该会跑吧，别管是人推的，还是电力驱动的，总之要会跑"""
        for action in self.sequence:
            if action == RunOrder.start.value:
                self.start()
            elif action == RunOrder.stop.value:
                self.stop()
            elif action == RunOrder.alarm.value:
                self.alarm()
            elif action == RunOrder.engine_boom.value:
                self.engine_boom()

    def set_sequence(self, sequence):
        """设置顺序"""
        self.sequence = sequence


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# TODO(tip): 抽象建造者
# 抽象汽车组装者
class CarBuilder(object):

    def set_sequence(self, sequence):
        """设置顺序：建造一个模型，你要给我一个顺序"""
        pass

    def get_car_model(self):
        """设置完毕顺序，就可以直接拿到这个模型"""
        pass


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# TODO(tip): 具体产品
# 奔驰模型
class BenzModel(CarModel):

    def start(self):
        print("奔驰车跑起来是这个样子的...")

    def stop(self):
        print("奔驰应该这样停车...")

    def alarm(self):
        print("奔驰的喇叭声音是这个样子的...")

    def engine_boom(self):
        print("奔驰车引擎声音是这样的...")


# 宝马模型
class BMWModel(CarModel):

    def start(self):
        print("宝马车跑起来是这个样子的...")

    def stop(self):
        print("宝马应该这样停车...")

    def alarm(self):
        print("宝马的喇叭声音是这个样子的...")

    def engine_boom(self):
        print("宝马车引擎声音是这样的...")


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# TODO(tip): 具体建造者
# 奔驰车组装者
class BenzBuilder(CarBuilder):

    def __init__(self):
        self.benz = BenzModel()

    def set_sequence(self, sequence):
        self.benz.set_sequence(sequence)

    def get_car_model(self):
        return self.benz


# 宝马车组装者
class BMWBuilder(CarBuilder):

    def __init__(self):
        self.bmw = BMWModel()

    def set_sequence(self, sequence):
        self.bmw.set_sequence(sequence)

    def get_car_model(self):
        return self.bmw


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# TODO(tip): 导演类
class Director(object):
    """导演类：负责按照指定的顺序生产模型"""

    def __init__(self):
        self.sequence = list()
        self.benz_builder = BenzBuilder()
        self.bmw_builder = BMWBuilder()

    def get_a_benz_model(self):
        """A类型的奔驰车，先start，然后stop，其他什么引擎了，喇叭了一概没有"""
        # 清理场景类
        self.sequence.clear()  # TODO(tip): 这里是一些初级程序员不注意的地方
        # 这只ABenzModel的执行顺序
        self.sequence.append(RunOrder.start.value)
        self.sequence.append(RunOrder.stop.value)
        # 按照顺序返回一个奔驰车
        self.benz_builder.set_sequence(self.sequence)
        return self.benz_builder.get_car_model()

    def get_b_benz_model(self):
        """B类型的奔驰车，先发动引擎，然后start，然后stop，没有喇叭"""
        self.sequence.clear()
        self.sequence.append(RunOrder.engine_boom.value)
        self.sequence.append(RunOrder.start.value)
        self.sequence.append(RunOrder.stop.value)
        self.benz_builder.set_sequence(self.sequence)
        return self.benz_builder.get_car_model()

    def get_c_bmw_model(self):
        """C类型的宝马车，是先按下喇叭（炫耀嘛），然后start，然后stop"""
        self.sequence.clear()
        self.sequence.append(RunOrder.alarm.value)
        self.sequence.append(RunOrder.start.value)
        self.sequence.append(RunOrder.stop.value)
        self.bmw_builder.set_sequence(self.sequence)
        return self.bmw_builder.get_car_model()

    def get_d_bmw_model(self):
        """D类型的宝马车，只有一个功能，就是跑，启动起来就跑，永远不停止"""
        self.sequence.clear()
        self.sequence.append(RunOrder.start.value)
        self.bmw_builder.set_sequence(self.sequence)
        return self.bmw_builder.get_car_model()


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# 场景类
class Client(object):

    @staticmethod
    def main():
        # XX公司要A类型的奔驰车1辆，B类型的奔驰车2两，C类型的宝马车3辆，D类型的车不要。
        director = Director()
        for i in range(1):
            a_benz = director.get_a_benz_model()
            a_benz.run()
            print("* * * ")
        print("- - - - - - - - - - - - - - - - - - - - - - - - ")

        for i in range(2):
            b_benz = director.get_b_benz_model()
            b_benz.run()
            print("* * * ")
        print("- - - - - - - - - - - - - - - - - - - - - - - - ")

        for i in range(3):
            c_bmw = director.get_c_bmw_model()
            c_bmw.run()
            print("* * * ")
        print("- - - - - - - - - - - - - - - - - - - - - - - - ")


if __name__ == '__main__':
    client = Client()
    client.main()
