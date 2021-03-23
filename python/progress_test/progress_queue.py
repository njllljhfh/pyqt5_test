# -*- coding:utf-8 -*-
import multiprocessing
from multiprocessing import Process, Queue
import time


def producer(q, count):
    for i in range(1, count + 1):
        # print(f"producer---id(q) = {id(q)}")
        print(f"进程({multiprocessing.current_process().pid})put数据：{i}")
        q.put(i)
        time.sleep(0.5)


def consumer(q, count):
    counter = 0
    while counter < count:
        # print(f"consumer---id(q) = {id(q)}")
        print(f"进程({multiprocessing.current_process().pid})get数据：{q.get()}")
        counter += 1


if __name__ == '__main__':
    count = 10
    s = time.time()
    q = Queue()
    print(f"main---id(q) = {id(q)}")
    p1 = Process(target=producer, args=(q, count))
    p2 = Process(target=consumer, args=(q, count))

    p1.start()
    p2.start()

    for i in range(2):
        time.sleep(1)
        print(f"主进程-----{i}")

    # 主进程会等到所有子进程都结束后，如果主进程中没有后续的可执行代码，主进程才会结束。
    p1.join()
    p2.join()

    print(f"耗时：{time.time() - s}")
    print("主进程，最后一行代码")
