# -*- coding:utf-8 -*-
import multiprocessing
import time


class MyCustomProcess(multiprocessing.Process):
    def __init__(self, num):
        super().__init__()
        self.num = num

    def run(self):
        for i in range(self.num):
            time.sleep(1)
            print(f"{i}")


if __name__ == '__main__':
    n = 3
    p = MyCustomProcess(n)
    # 主进程默认会等待子进程结束

    # p.daemon = True  # daemon 为True 主进程不等待子进程结束

    p.start()

    # p.join()  # join()后的代码要等，p子进程结束后，才会执行

    print("main end")
