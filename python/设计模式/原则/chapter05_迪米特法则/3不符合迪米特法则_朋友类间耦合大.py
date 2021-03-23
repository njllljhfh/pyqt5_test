# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》 --- 迪米特法则-不符合迪米特法则-朋友类间耦合过大 --- P-56"

import random


# TODO(问题): Wizard 类把太多的方法暴露给 InstallSoftware 类，两者的朋友关系太亲密了，耦合关系变的异常牢固。
# 向导类
class Wizard(object):

    @property
    def rand(self):
        return random.randint(1, 100)

    def first(self):
        print("执行第一个方法...")
        return self.rand

    def second(self):
        print("执行第二个方法...")
        return self.rand

    def third(self):
        print("执行第三个方法...")
        return self.rand


# InstallSoftware类
class InstallSoftware(object):

    @staticmethod
    def install_wizard(wizard: Wizard):
        first = wizard.first()
        # 根据first的返回结果，看是否需要执行second
        if first > 50:
            second = wizard.second()
            if second > 50:
                third = wizard.third()
                if third > 50:
                    wizard.first()


# 场景类（模拟人工选择安装过程的操作）
class Client(object):

    @staticmethod
    def main():
        invoker = InstallSoftware()
        wizard = Wizard()
        invoker.install_wizard(wizard)


if __name__ == '__main__':
    client = Client()
    client.main()
