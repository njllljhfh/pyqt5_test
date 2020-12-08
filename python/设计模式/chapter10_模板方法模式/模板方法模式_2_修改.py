# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 模板方法模式 --- P-108"

# TODO(注意): 在软件开发过程中，如果相同的一段代码拷贝过两次，就需要对设计产生怀疑，
#             架构师要明确地说明为什么相同的逻辑要出现两次或更多次。


# 抽象悍马模型
class HummerModel(object):

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
        # 先发动汽车
        self.start()
        # 引擎开始轰鸣
        self.engine_boom()
        # 然后就开始跑了，跑的过程中碰到一条狗挡路，就按喇叭
        self.alarm()
        # 到达目的地就停车
        self.stop()


# H1型号悍马模型
class HummerH1Model(HummerModel):

    def start(self):
        print("悍马H1发动...")

    def stop(self):
        print("悍马H1停车...")

    def alarm(self):
        print("悍马H1鸣笛...")

    def engine_boom(self):
        print("悍马H1引擎声音是这样的...")


# H2型号悍马模型
class HummerH2Model(HummerModel):

    def start(self):
        print("悍马H2发动...")

    def stop(self):
        print("悍马H2停车...")

    def alarm(self):
        print("悍马H2鸣笛...")

    def engine_boom(self):
        print("悍马H2引擎声音是这样的...")


# 场景类
class Client(object):

    @staticmethod
    def main():
        # XX公司要H1型号的悍马
        h1 = HummerH1Model()
        # H1模型演示
        h1.run()


if __name__ == '__main__':
    client = Client()
    client.main()
