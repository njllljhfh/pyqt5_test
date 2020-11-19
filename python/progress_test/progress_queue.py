# -*- coding:utf-8 -*-
from multiprocessing import Process, Queue
import time


def producer(q: Queue, count):
    for i in range(1, count + 1):
        q.put(i)
        time.sleep(0.5)


def consumer(q: Queue, count):
    counter = 0
    while counter < count:
        print(f"q.get() = {q.get()}")
        counter += 1


if __name__ == '__main__':
    count = 10
    q = Queue()
    p1 = Process(target=producer, args=(q, count))
    p2 = Process(target=consumer, args=(q, count))

    p1.start()
    p2.start()

    for i in range(2):
        time.sleep(1)
        print(f"主进程-----{i}")
    # 主进程会等到所有子进程都结束后，如果主进程中没有后续的可执行代码，主进程才会结束。
    print("主进程，最后一行代码")
