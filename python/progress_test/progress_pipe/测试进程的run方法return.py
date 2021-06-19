# -*- coding:utf-8 -*-
from multiprocessing import Process
import time


class Task(Process):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print(f"{self.name} is running")
        i = 0
        while True:
            print(f"i = {i}")
            if i >= 2:
                print(f"{self.name} is gone")
                return
            i += 1
            time.sleep(0.5)


if __name__ == "__main__":
    p = Task(name="常辛")  # 创建一个进程对象
    p.start()

    for j in range(10):
        print(f'=========主进程========={j}')
        print(f'{p} is alive =', p.is_alive())  # 判断子进程是否活着
        time.sleep(1)
