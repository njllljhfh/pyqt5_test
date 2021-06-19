# -*- coding:utf-8 -*-
from time import sleep
import multiprocessing as mp
import time
import os


def x_main(sec):
    sleep(sec)
    print("Child process start")
    sleep(sec)


if __name__ == '__main__':

    p = mp.Process(name="child", target=x_main, args=(10,))
    '''
    daemon¶
        The process’s daemon flag, a Boolean value. This must be set before start() is called.
        The initial value is inherited from the creating process.
        When a process exits, it attempts to terminate all of its daemonic child processes.
        
        Note that a daemonic process is not allowed to create child processes.
        Otherwise a daemonic process would leave its children orphaned 
        if it gets terminated when its parent process exits. 
        Additionally, these are not Unix daemons or services, 
        they are normal processes that will be terminated (and not joined) if non-daemonic processes have exited.
    '''
    p.daemon = True

    print("Main process", os.getpid())
    p.start()

    print("child PID:", p.pid)
    print("-----------------")
    print("End")
