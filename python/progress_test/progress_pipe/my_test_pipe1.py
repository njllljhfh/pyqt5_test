# -*- coding:utf-8 -*-
"""
测试不关闭主进程的生产者用的pipe。
"""
import multiprocessing
import os
from multiprocessing import Process, Pipe
import time
from multiprocessing.connection import Connection


def producer(conn: Connection, count):
    print('producer conn2 id', id(conn))
    for i in range(1, count + 1):
        print(f"进程({multiprocessing.current_process().pid})put数据：{i}")
        # print(f"进程({os.getpid()})put数据：{i}")
        conn.send(i)
        time.sleep(0.3)
        # - - -

        # conn.close()  # Close input pipe.
        # break


def consumer(conn: Connection, count):
    counter = 0
    try:
        print('consumer conn1 id', id(conn))
        # while counter < count:
        while True:
            # The recv() function:
            # Return an object sent from the other end of the connection using send().
            # Blocks until there is something to receive.
            # Raises EOFError if there is nothing left to receive and the other end was closed.
            print(f"进程({multiprocessing.current_process().pid})get数据：{conn.recv()}")
            counter += 1
    except EOFError:
        #
        print(f"end consumer : EOFError")


if __name__ == '__main__':
    count = 10
    s = time.time()
    conn1, conn2 = Pipe(True)
    p1 = Process(target=producer, args=(conn2, count))
    p2 = Process(target=consumer, args=(conn1, count))
    print('main conn1 id', id(conn1))
    print('main conn2 id', id(conn2))

    p1.start()
    conn2.close()  # TODO: If doesn't close here, the consumer will block when the producer progress completes.

    p2.start()

    for i in range(2):
        time.sleep(1)
        print(f"主进程-----{i}")

    # The main process will finish when no code can be executed in it.
    p1.join()
    p2.join()

    print('*  ' * 30)
    print(f"耗时：{time.time() - s}")
    print("主进程，最后一行代码")
