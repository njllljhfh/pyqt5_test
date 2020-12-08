# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 建造者模式_2_添加建造者 --- P-120"

from enum import unique, Enum


# run顺序枚举类
@unique
class RunOrder(Enum):
    start = 0
    stop = 1
    alarm = 2
    engine_boom = 3


# 车辆模型的抽象类
class CarModel(object):

    def __init__(self):
        self.sequence = list()

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


# 抽象汽车组装者
class CarBuilder(object):

    def set_sequence(self, sequence):
        """设置顺序：建造一个模型，你要给我一个顺序"""
        pass

    def get_car_model(self):
        """设置完毕顺序，就可以直接拿到这个模型"""
        pass


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


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


# 场景类
class Client(object):

    @staticmethod
    def main():
        # 存放run方法的顺序
        sequence = list()
        sequence.append(RunOrder.engine_boom.value)  # 客户要求，run的时候先发动引擎
        sequence.append(RunOrder.start.value)  # 启动起来
        sequence.append(RunOrder.stop.value)  # 开了一段就停下来

        # 要一个奔驰车
        benz_builder = BenzBuilder()
        # 把顺序给这个builder类，制造出这样一个车出来
        benz_builder.set_sequence(sequence)
        benz = benz_builder.get_car_model()
        benz.run()
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")

        # 按照同样的顺序，我再要一个宝马车
        bmw_builder = BMWBuilder()
        bmw_builder.set_sequence(sequence)
        bmw = bmw_builder.get_car_model()
        bmw.run()


if __name__ == '__main__':
    client = Client()
    client.main()
