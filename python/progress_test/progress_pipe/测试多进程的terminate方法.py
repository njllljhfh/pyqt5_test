# -*- coding:utf-8 -*-
from multiprocessing import Process
import time


class Task(Process):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print(f"{self.name} is running")
        time.sleep(2)
        print(f"{self.name} is gone")


if __name__ == "__main__":
    # 在windows环境下，开启进程必须在__name__ == "__main__"下面
    p = Task(name="常辛")  # 创建一个进程对象
    p.start()

    p.terminate()  # 杀死子进程
    # time.sleep(1)
    p.join()
    print(p.is_alive())  # 判断子进程是否活着
    print(p, p.is_alive())
    print("主开始")
