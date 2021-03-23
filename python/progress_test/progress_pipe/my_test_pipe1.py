# -*- coding:utf-8 -*-
import multiprocessing
import os
from multiprocessing import Process, Pipe
import time
from multiprocessing.connection import Connection


def producer(conn: Connection, count):
    for i in range(1, count + 1):
        print(f"进程({multiprocessing.current_process().pid})put数据：{i}")
        # print(f"进程({os.getpid()})put数据：{i}")
        conn.send(i)
        time.sleep(0.5)
        # - - -

        # conn.close()  # Close input pipe.
        # break


def consumer(conn: Connection, count):
    counter = 0
    try:
        while counter < count:
            print(f"进程({multiprocessing.current_process().pid})get数据：{conn.recv()}")
            counter += 1
    except EOFError:
        print(f"end consumer : EOFError")


if __name__ == '__main__':
    count = 10
    s = time.time()
    conn1, conn2 = Pipe(True)
    p1 = Process(target=producer, args=(conn2, count))
    p2 = Process(target=consumer, args=(conn1, count))

    p1.start()
    p2.start()

    conn2.close()  # TODO: If doesn't close here, the consumer will block.

    for i in range(2):
        time.sleep(1)
        print(f"主进程-----{i}")

    # The main process will finish when no code can be executed in it.
    p1.join()
    p2.join()

    print(f"耗时：{time.time() - s}")
    print("主进程，最后一行代码")
