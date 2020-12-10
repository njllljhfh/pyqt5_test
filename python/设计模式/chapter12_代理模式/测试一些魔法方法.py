# -*- coding:utf-8 -*-
import time
from types import MethodType

COUNTER = 0


class Dragon(object):
    def __new__(cls, *args, **kwargs):
        """
        :param args: __init__()方法的位置参数。
        :param kwargs: __init__()方法的命名参数。
        :return:
        """
        print(f"__new__(): args={args}, kwargs={kwargs}")
        return super().__new__(cls)

    def __init__(self, name):
        """构造器：当一个实例被创建的时候，调用的初始化方法。"""
        self.name = name

    def __del__(self):
        """析构器：当该类的一个实例被销毁的时候，调用该方法。"""
        print("__del__(): 析构器")

    def __call__(self, *args, **kwargs):
        """允许一个类的实例，像函数一样被调用："""
        print(f"__call__(): args={args}, kwargs={kwargs}")

    def __len__(self):
        """定义被len()调用时的行为"""
        print(f"__len__(): ")
        return 66

    def __repr__(self):
        """定义被repr()调用时的行为"""
        print(f"__repr__():")
        return f"repr-{self.__class__.__name__}"

    def __str__(self):
        """定义被str()调用时的行为"""
        # print(f"__str__():")
        return f"str-{self.name}"

    """ - - - """

    def __getattr__(self, item):
        """定义当用户试图获取一个不存在的属性时的行为"""
        global COUNTER
        COUNTER += 1
        print(f"__getattr__(): type(item)={type(item)}, item={item}")
        return print

    def __getattribute__(self, item):
        """
        需要注意的是，正式由于它拦截对所有属性的访问（包括对__dict__的访问），
        在使用中要十分小心地避开无限循环的陷阱。在__getattribute__方法中访问当前实例的属性时，
        唯一安全的方式是使用基类（超类） 的方法__getattribute__（使用super）
        """
        print(f"__getattribute__(): item={item}")
        if item == "name":
            print("拦截：name")
        return super().__getattribute__(item)

    def do_something(self):
        print(f"do_something")


if __name__ == '__main__':
    zgl = Dragon("诸葛亮")

    print(zgl.name)

    print(zgl.nihao)

    # zgl.run("hello")

    # zgl.do_something()
    #
    # zgl("a", b="B")
    #
    # res = len(zgl)
    # print(f"{res}")
    #
    # print(f"repr(zgl) = {repr(zgl)}")
    #
    # print(f"str(zgl) = {str(zgl)}")
    #
    # del zgl
    #
    # print(f"COUNTER = {COUNTER}")
