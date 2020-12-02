# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》 --- 迪米特法则-符合迪米特法则_朋友类间低耦合 --- P-58"

import random


# TODO: 将三个步骤的访问权限改为私有的，把 install_wizard 方法移动到 Wizard 中，对外只公布这一个方法。即使要修改 _first 方法
#       的方返回值，影响的也仅仅是方法 Wizard 本身，其他类不受影响，这显示了类的高内聚性。

# TODO: 在实际应用中，经常会出现这样一个方法：放在本类中也可以，放在其他类中也没错，那怎么去衡量呢？
#       可以坚持这样一个原则：如果一个方法放在本类中，既不增加类间关系，也对本类不产生负面影响，就放在本类中。

# TODO: 迪米特法则的核心观念就是类间解耦合，弱耦合，只有弱耦合了以后，类的复用率才可以提高（高内聚低耦合）。

# 向导类
class Wizard(object):

    @property
    def rand(self):
        return random.randint(1, 100)

    def _first(self):
        print("执行第一个方法...")
        return self.rand

    def _second(self):
        print("执行第二个方法...")
        return self.rand

    def _third(self):
        print("执行第三个方法...")
        return self.rand

    def install_wizard(self):
        """封装软件安装过程"""
        first = self._first()
        # 根据first的返回结果，看是否需要执行second
        if first > 50:
            second = self._second()
            if second > 50:
                third = self._third()
                if third > 50:
                    self._first()


# InstallSoftware类
class InstallSoftware(object):

    @staticmethod
    def install_wizard(wizard: Wizard):
        # 直接调用
        wizard.install_wizard()


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
