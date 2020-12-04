# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 模板方法模式-模板方法的扩展(钩子方法) --- P-112"


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
        # TODO: 喇叭可响，也可不响
        if self.is_alarm():
            self.alarm()
        # 到达目的地就停车
        self.stop()

    # TODO: Hook Method（钩子方法）
    # TODO: is_alarm 方法的返回值影响了模板方法 run 的执行结果。
    def is_alarm(self):
        """钩子方法，默认喇叭是会的。"""
        return True


# 扩展后的H1悍马
class HummerH1Model(HummerModel):

    def __init__(self):
        # 喇叭要响
        self._alarm_flag = True

    def start(self):
        print("悍马H1发动...")

    def stop(self):
        print("悍马H1停车...")

    def alarm(self):
        print("悍马H1鸣笛...")

    def engine_boom(self):
        print("悍马H1引擎声音是这样的...")

    def is_alarm(self):
        """钩子方法，默认喇叭是会的"""
        return self._alarm_flag

    # TODO:喇叭要不要响，是由客户来决定的
    def set_alarm(self, is_alarm: bool):
        self._alarm_flag = is_alarm


# 扩展后的H2悍马
class HummerH2Model(HummerModel):

    def start(self):
        print("悍马H2发动...")

    def stop(self):
        print("悍马H2停车...")

    def alarm(self):
        print("悍马H2鸣笛...")

    def engine_boom(self):
        print("悍马H2引擎声音是这样的...")

    # TODO:默认没有喇叭的
    def is_alarm(self):
        return False


# 场景类
class Client(object):

    @staticmethod
    def main():
        print("- - - - - - - H1型号悍马 - - - - - - -")
        num = input(f"H1型号的悍马是否需要叭声响？ 0-不需要    1-需要")
        h1 = HummerH1Model()
        if num == "0":
            h1.set_alarm(False)
        else:
            h1.set_alarm(True)
        h1.run()

        print("- - - - - - - H2型号悍马 - - - - - - -")
        h2 = HummerH2Model()
        h2.run()


if __name__ == '__main__':
    client = Client()
    client.main()
