# -*- coding:utf-8 -*-
import time
from threading import Thread, Timer

from datetime import datetime, timedelta

a = "2020-12-25 15:41:00"
last_product_date = datetime(2020, 12, 25, 15, 42, 59)


# date_2 = datetime.now()
# print(f"date_1 = {date_1}")

# print(f"{type(date_2 - date_1)}")
# print(f"{date_2 - date_1}")

# print(f"{timedelta(minutes=3)}")


def alert(timeout: timedelta = timedelta(minutes=3)):
    if datetime.now() - last_product_date > timeout:
        print(f"超时：{timeout}")


class AlertThread(Thread):

    def __init__(self, func, func_kwargs={}):
        super().__init__()
        self.func = func
        self.func_kwargs = func_kwargs
        # self.timeout = 3 * 60
        self.timeout = 5
        self._quit = True

    def run(self):
        self._quit = False
        for i in range(self.timeout):
            if not self._quit:
                time.sleep(1)
            else:
                break
        else:
            self.func(**self.func_kwargs)

    def stop(self):
        self._quit = True


if __name__ == '__main__':
    kwargs = {
        "timeout": timedelta(minutes=3),
    }
    a = AlertThread(alert, kwargs)
    a.start()
    for i in range(10):
        print(f"i = {i}")
        time.sleep(1)
        if i == 2:
            print(f"停止定时器")
            a.stop()
            a.join()

    a.start()
    print(f"主进程结束")

    # alert_timer = Timer(3, alert)
    # alert_timer.start()
    # for i in range(5):
    #     print(f"{i}")
    #     time.sleep(1)
    #     if i == 0:
    #         print("关闭")
    #         alert_timer.cancel()
    #
    # alert_timer.start()

    # def MonitorNetWork():
    #     print(f"xxx")
    #     # 启动定时器任务，每秒执行一次
    #     Timer(1, MonitorNetWork).start()
    # MonitorNetWork()
