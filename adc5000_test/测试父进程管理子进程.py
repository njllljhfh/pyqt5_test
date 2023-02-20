# -*- coding:utf-8 -*-
from __future__ import annotations

import time
from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection

STOP_FLAG = 'stop'


class Parent(Process):

    def __init__(self):
        super(Parent, self).__init__()
        self._is_stopped = False

    def run(self) -> None:
        p_cnn, s_cnn = Pipe(duplex=True)

        print(f'[父进程]启动子进程')
        son = Son(s_cnn)
        son.start()

        print(f'[父进程]监控停止符')
        j = 0
        while not self._is_stopped:
            time.sleep(0.5)
            if j == 10:
                print(f'[父进程]监控到停止符，停止子进程')
                # son.stop()  # 此方法无用，父进程无法在子进程的运行时，修改子进程中的变量
                # son.terminate()
                p_cnn.send(STOP_FLAG)
                son.join()
                self._is_stopped = True
            j += 1

        print(f'[父进程]退出监控进程')
        p_cnn.close()


class Son(Process):

    def __init__(self, s_cnn):
        super(Son, self).__init__()
        self._is_stopped = False
        self.s_cnn: Connection = s_cnn

    def run(self) -> None:
        i = 1
        while not self._is_stopped:
            print(f'[子进程] --------------- {i}, self._is_stopped={self._is_stopped}')
            i += 1
            time.sleep(1)
            if self.s_cnn.poll():
                s = self.s_cnn.recv()
                print(f'[子进程] --------------- {i}, s={s}')
                if s == STOP_FLAG:
                    self._is_stopped = True
                    break

        self.s_cnn.close()
        print(f'[子进程]子进程退出')

    def stop(self):
        self._is_stopped = True


if __name__ == '__main__':
    p = Parent()
    p.start()
