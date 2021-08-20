# -*- coding:utf-8 -*-
# 官网（https://docs.python.org/3.6/library/queue.html#queue.Queue.task_done）
"""
q = queue.Queue()
q.join()
测试 q 和 q.join()
"""
import queue
import threading
import time

num_worker_threads = 2

do_work = lambda x: print(x)


def source():
    return [i for i in range(10)]


def worker(num):
    while True:
        item = q.get()
        if item is None:
            print(f"work_{num}:退出")
            break
        do_work(f"work_{num}:{item}")
        time.sleep(0.3)
        q.task_done()


q = queue.Queue()
threads = []
for i in range(num_worker_threads):
    t = threading.Thread(target=worker, args=(i,))
    t.start()
    threads.append(t)

for item in source():
    q.put(item)

print(f"block until all tasks are done")
q.join()

print(f"stop workers")
for i in range(num_worker_threads):
    q.put(None)
for t in threads:
    t.join()
