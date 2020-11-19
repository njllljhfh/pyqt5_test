# -*- coding:utf-8 -*-
from multiprocessing import Process
import time

NUM = 0


def work(x, num):
    for i in range(10):
        print(f"work: {x}---{num}")
        time.sleep(0.5)
        num += 1
    print(f"{x}执行结束了。")


if __name__ == '__main__':
    p1 = Process(target=work, args=("x", NUM))
    NUM += 10
    p2 = Process(target=work, args=("y", NUM))

    p1.start()
    p1.join(2)  # 表示后续代码最多等待2秒
    p2.start()
