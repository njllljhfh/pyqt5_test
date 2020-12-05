# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》 --- 单例模式的扩展-有上限的多例模式 --- P-79"
import random
import threading
import time

# NUM = 0  # 测试代码
# LOCK = threading.Lock()  # 测试代码


class Singleton(object):
    """单例模式（线程安全）：固定个数实例"""
    _instance_lock = threading.Lock()
    _instances = dict()
    _instance_max_num = 3

    def __new__(cls, *args, **kwargs):
        with cls._instance_lock:
            key = len(cls._instances)
            if key < cls._instance_max_num:
                # time.sleep(1)  # 测试代码
                cls._instances[key] = super().__new__(cls)
                # with LOCK:  # 测试代码
                #     global NUM  # 测试代码
                #     NUM += 1  # 测试代码
            else:
                key = random.randint(0, cls._instance_max_num - 1)
        return cls._instances[key]

    def __init__(self):
        pass

    def do_something(self):
        print(f"{id(self)}, Do something.")

    @classmethod
    def instance_num(cls):
        print(f"实例个数 = {len(cls._instances)}")
        for key in (cls._instances.keys()):
            print(cls._instances[key])


def worker():
    s = Singleton()
    s.do_something()


if __name__ == '__main__':

    task_list = []
    for one in range(10):
        t = threading.Thread(target=worker)
        task_list.append(t)

    for one in task_list:
        one.start()

    for one in task_list:
        one.join()

    # print(f"NUM = {NUM}")  # 测试代码

    Singleton.instance_num()
