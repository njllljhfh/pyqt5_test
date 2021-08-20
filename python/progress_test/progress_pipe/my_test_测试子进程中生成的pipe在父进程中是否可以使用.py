# -*- coding:utf-8 -*-
import time
from multiprocessing import Process, Pipe, connection


class SubProcess(Process):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.__quit_pipe__ = Pipe()
        print(f"pip_id in SubProcess= {[id(self.__quit_pipe__[0]), id(self.__quit_pipe__[1])]}")

    @property
    def pipe0(self):
        """ 外部使用的管道
        发送信号格式 [(name,pid), code, data]
        """
        return self.__quit_pipe__[0]

    @property
    def pipe1(self):
        """ 内部使用的管道
        发送信号格式 [(name,pid), code, data]
        """
        return self.__quit_pipe__[1]

    def run(self):
        while True:
            if connection.wait([self.pipe1], timeout=0):
                print(f"work = {self.pipe1.recv()}")
            if connection.wait([self.pipe0], timeout=0):
                print(f"结束了")
                if self.pipe0.recv() == "END":
                    return


if __name__ == '__main__':
    p1 = SubProcess("p1")
    p1.start()

    print(f"pip_id in parent process = {[id(p1.pipe0), id(p1.pipe1)]}")

    for i in range(10):
        p1.pipe0.send(i)
        time.sleep(0.15)
    else:
        p1.pipe1.send("END")
