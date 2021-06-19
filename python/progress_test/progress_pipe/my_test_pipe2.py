# -*- coding:utf-8 -*-

import multiprocessing
import os
import time

"""
在consumer中，conn2.close()了，在单独进程cons_p中执行，但producer中conn2还能发送数据.
在main中，conn1.close()了，在但是在单独进程cons_p的consumer中，conn1还能接收数据.
"""


def consumer(pipe):
    conn1, conn2 = pipe
    print('consumer conn1 id', id(conn1))
    print('consumer conn2 id', id(conn2))
    print("process consumer id", os.getpid())

    conn2.close()  # input pipe close 1
    while True:
        try:
            item = conn1.recv()
        except EOFError:
            print('EOFError')
            break
        print(item)
    print('consumer done')
    # conn1.close()


def producer(listArr, conn2):
    for item in listArr:
        conn2.send(item)
        time.sleep(0.3)


if __name__ == '__main__':
    (conn1, conn2) = multiprocessing.Pipe(True)
    cons_p = multiprocessing.Process(target=consumer, args=((conn1, conn2),))
    cons_p.start()

    conn1.close()  # output pipe close

    arr = [1, 2, 3, 4, 5]
    producer(arr, conn2)
    print('   main conn1 id', id(conn1))
    print('   main conn2 id', id(conn2))
    conn2.close()  # input pipe close

    cons_p.join()
