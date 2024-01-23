# -*- coding:utf-8 -*-
import threading
import time


class MyThread(threading.Thread):

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        for i in range(3):
            time.sleep(1)
            print(f"{i}")


if __name__ == '__main__':
    t = MyThread()

    # 主线程不等待 daemon 为 True 的子线程执行结束
    t.daemon = True

    # 默认情况下，主线程会等待子线程执行结束
    t.start()

    # t.join() # 与主线程同步

    print(f"main end")
