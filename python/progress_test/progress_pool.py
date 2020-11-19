# -*- coding:utf-8 -*-
from multiprocessing import Manager, Pool
import time


def producer(q: Manager().Queue, count):
    for i in range(1, count + 1):
        q.put(i)
        time.sleep(0.5)


def consumer(q: Manager().Queue, count):
    counter = 0
    while counter < count:
        print(f"q.get() = {q.get()}")
        counter += 1


if __name__ == '__main__':
    count = 10
    # q = Queue() # 用这个Queue代码不工作
    q = Manager().Queue()

    pool = Pool(3)
    pool.apply_async(producer, (q, count))
    pool.apply_async(consumer, (q, count))

    pool.close()  # 主进不会等待进程池中的进程执行完毕

    for i in range(2):
        time.sleep(1.1)
        print(f"主进程---{i}")
    print("主进程，最后一行代码")
