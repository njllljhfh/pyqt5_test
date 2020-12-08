# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》 --- 单例模式(Singleton Pattern) --- P-75"

import threading
import time

NUM = 0
LOCK = threading.Lock()


# def synchronized(func):
#     func.__lock__ = threading.Lock()
#
#     def lock_func(*args, **kwargs):
#         with func.__lock__:
#             return func(*args, **kwargs)
#
#     return lock_func
#
#
# class Singleton(object):
#     """
#     单例模式(线程安全)
#     """
#     _instance = None
#
#     @synchronized
#     def __new__(cls, *args, **kwargs):
#         if cls._instance is None:
#             time.sleep(1)
#             cls._instance = super().__new__(cls, *args, **kwargs)
#             with LOCK:
#                 global NUM
#                 NUM += 1
#         return cls._instance
#
#     def do_something(self):
#         print(f"{id(self)}, Do something.")


# - - - - - -
class Singleton(object):
    """单例模式（线程安全）"""
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            # time.sleep(1)
            with cls._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = object.__new__(cls)
                    # with LOCK:
                    #     global NUM
                    #     NUM += 1
        return Singleton._instance

    def do_something(self):
        print(f"{id(self)}, Do something.")


# - - - - - -

# class Singleton(object):
#     """线程不安全"""
#     _instance = None
#
#     def __new__(cls):
#         if cls._instance is None:
#             time.sleep(1)
#             cls._instance = super().__new__(cls)
#             with LOCK:
#                 global NUM
#                 NUM += 1
#         return cls._instance
#
#     def do_something(self):
#         print(f"{id(self)}, Do something.")


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

    print(f"NUM = {NUM}")
