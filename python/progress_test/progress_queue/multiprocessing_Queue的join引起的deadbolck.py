# -*- coding:utf-8 -*-
# 官网（https://docs.python.org/3.6/library/multiprocessing.html#programming-guidelines）
"""
Joining processes that use queues
Bear in mind that a process that has put items in a queue will wait
before terminating until all the buffered items are fed by the “feeder” thread
to the underlying pipe. (The child process can call
the Queue.cancel_join_thread method of the queue to avoid this behaviour.)

This means that whenever you use a queue you need to make sure
that all items which have been put on the queue will eventually be removed
before the process is joined. Otherwise you cannot be sure
that processes which have put items on the queue will terminate.
Remember also that non-daemonic processes will be joined automatically.

An example which will deadlock is the following:
"""
from multiprocessing import Process, Queue


def f(q):
    q.put('X' * 1000000)


if __name__ == '__main__':
    queue = Queue()
    p = Process(target=f, args=(queue,))
    p.start()
    p.join()  # this deadlocks
    obj = queue.get()

"""
A fix here would be to swap the last two lines (or simply remove the p.join() line).
"""
