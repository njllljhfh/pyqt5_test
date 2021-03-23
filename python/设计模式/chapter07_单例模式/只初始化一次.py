# -*- coding:utf-8 -*-
class Singleton(object):
    """线程不安全"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if Singleton._instance._initialized:
            return

        self.a = 1
        self.b = 2

        Singleton._instance._initialized = True

    def do_something(self):
        print(f"{id(self)}, Do something-- {self.a}-{self.b}.")


if __name__ == '__main__':
    aaa = Singleton()
    aaa.do_something()
    aaa.a = 11
    aaa.b = 122
    aaa.do_something()

    bbb = Singleton()
    bbb.do_something()
