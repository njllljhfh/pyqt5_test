# -*- coding:utf-8 -*-
"""
测试在进程的run方法中return。
"""
import multiprocessing
import os
from multiprocessing import Process, Pipe
import time
from multiprocessing.connection import Connection

class Producer(Process):

    def __init__(self, conn:Connection, count, name):
        super().__init__()
        self.conn = conn
        self.count = count
        self.name = name

    def run(self):
        print('producer conn2 id', id(self.conn))
        for i in range(1, self.count + 1):
            print('-  ' * 20)
            print(f"{self.name}  进程({self.pid})-生产数据：{i}")
            self.conn.send(i)
            time.sleep(0.3)
            if i == 2:
                return  # 返回后，进程就结束了


class Consumer(Process):

    def __init__(self, conn:Connection, name):
        super().__init__()
        self.conn = conn
        self.name = name

    def run(self):
        try:
            print(f'{self.name}  consumer conn1 id', id(self.conn))
            while True:
                # The recv() function:
                # Return an object sent from the other end of the connection using send().
                # Blocks until there is something to receive.
                # Raises EOFError if there is nothing left to receive and the other end was closed.
                print(f"{self.name}  进程({self.pid})-消费数据：{self.conn.recv()}")
        except EOFError:
            #
            print(f"{self.name}  end consumer : EOFError")


if __name__ == '__main__':
    count = 10
    s = time.time()
    conn1, conn2 = Pipe(True)
    p1 = Producer(conn2, count, "producer")
    c1 = Consumer(conn1, "consumer_1")
    c2 = Consumer(conn1, "consumer_2")
    print('main conn1 id', id(conn1))
    print('main conn2 id', id(conn2))

    p1.start()
    conn2.close()  # If doesn't close here, the consumer will block when the producer progress completes.

    # The two consumers compete the data in the cnn2.
    c1.start()
    c2.start()

    for i in range(2):
        time.sleep(1)
        print(f"主进程-----{i}")

    print(f'生产者进程是否还在运行:{p1.is_alive()}')

    # The main process will finish when no code can be executed in it.
    p1.join()
    c1.join()
    c2.join()

    print('*  ' * 30)
    print(f"耗时：{time.time() - s}")
    print("主进程，最后一行代码")
