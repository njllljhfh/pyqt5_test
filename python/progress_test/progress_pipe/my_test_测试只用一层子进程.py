# -*- coding:utf-8 -*-
"""
测试3层进程通讯，通过逐层的进程通信，来停止进程。
测试结果：
"""
import multiprocessing
import os
from multiprocessing import Process, Pipe
import time
from datetime import datetime
from multiprocessing import connection
from multiprocessing.connection import Connection

STOP_SUCCESSFULLY = "STOP_SUCCESSFULLY"
STOP = "STOP"

SLEEP_TIME = 0.5


class DetectProcessManager(Process):

    def __init__(self, manager_pipe_in: Connection, manager_worker_pipe_in_manager_ls: [Connection, ...], name):
        super().__init__()
        self.manager_pipe_in = manager_pipe_in
        self.name = name

        self.manager_worker_pipe_in_manager_ls = manager_worker_pipe_in_manager_ls

    def _close_worker_pipe(self):
        for worker_pipe in self.manager_worker_pipe_in_manager_ls:
            worker_pipe.close()

    def run(self):
        # self._start_worker_processes()

        i = 1
        while True:
            if self.manager_pipe_in.poll():
                print(f'self.manager_pipe_in.poll(): {self.manager_pipe_in.poll()}')
                message = self.manager_pipe_in.recv()
                if message == STOP:
                    print(f'self.manager_pipe_in.recv(): {message}')
                    print(f"GRPC进程停止")
                    self._close_worker_pipe()
                    return

            for worker_pipe in self.manager_worker_pipe_in_manager_ls:
                print(f"{self.name}  进程({self.pid}) 分配工作给子进程.")
                worker_pipe.send(f"开始干活啦{datetime.now()}。。。")

            time.sleep(SLEEP_TIME)
            i += 1


class DetectProcess(Process):

    def __init__(self, worker_pipe_in: Connection, manager_worker_pipe_in_worker: Connection, name):
        super().__init__()
        self.worker_pipe_in = worker_pipe_in
        self.manager_worker_pipe_in_worker = manager_worker_pipe_in_worker
        self.name = name

    def run(self):
        try:
            while True:
                # print(f'self.worker_pipe_in.poll() = {self.worker_pipe_in.poll()}')

                if self.worker_pipe_in.poll():
                    message = self.worker_pipe_in.recv()
                    print(f"{self.name}  进程({self.pid})  收到的管理进程信息-{message}")
                    if message == STOP:
                        self.worker_pipe_in.send((STOP_SUCCESSFULLY, self.pid))
                        self.worker_pipe_in.close()
                        print(f"{self.name}  进程({self.pid})  return")
                        return

                if self.manager_worker_pipe_in_worker.poll():
                    message = self.manager_worker_pipe_in_worker.recv()
                    print(f"worker进程：{self.name}, 收到新工作-{message}")

                    self.manager_worker_pipe_in_worker.send(f"{self.name}: 处理完工作({message})")

        except EOFError:
            print(f"{self.name}  end consumer : EOFError")


class Task(object):

    def __init__(self):
        # - - -
        self.worker_process_ls = list()
        self.worker_pipe_out_ls = list()

    # def _start_worker_processes(self):
    #     for i in range(1, 1 + 2):
    #         worker_pipe_out, worker_pipe_in = Pipe(True)  # 外部用 pipe/ 内部用 pipe
    #         worker_process = DetectProcess(worker_pipe_in, f"DetectProcess_{i}")
    #         self.worker_process_ls.append(worker_process)
    #         self.worker_pipe_out_ls.append(worker_pipe_out)
    #         worker_process.start()
    #         worker_pipe_in.close()
    #     print(f'self.worker_pipe_out_ls = {self.worker_pipe_out_ls}')

    def _stop_worker_processes(self):
        """停止检测任务"""
        for worker_out_pipe in self.worker_pipe_out_ls:
            worker_out_pipe.send(STOP)

        # self._whether_processes_are_alive()
        print(f'等待子进程关闭')
        stopped_worker_id_ls = list()
        worker_pipe_out_ls_duplicate = self.worker_pipe_out_ls[:]
        while True:
            for worker_out_pipe in connection.wait(self.worker_pipe_out_ls):
                if worker_out_pipe in worker_pipe_out_ls_duplicate:
                    worker_result, worker_pid = worker_out_pipe.recv()

                    # 子进程的停止信号收到后，不在去接收该子进程信号。
                    worker_pipe_out_ls_duplicate.remove(worker_out_pipe)

                    if worker_result == STOP_SUCCESSFULLY:
                        stopped_worker_id_ls.append(worker_pid)

                # 判断全部worker进程都结束了。
                if len(stopped_worker_id_ls) == len(self.worker_process_ls):
                    s = time.time()
                    self._join_worker_processes()
                    print(f"_join_worker_processes 耗时：{time.time() - s}")
                    self._whether_processes_are_alive()
                    self.manager_pipe_in.close()
                    print(
                        f'stopped_worker_id_ls = {stopped_worker_id_ls}, len: {len(stopped_worker_id_ls)}')
                    return

    def _whether_processes_are_alive(self):
        """判断子进程是否存活"""
        for worker_process in self.worker_process_ls:
            print(f"进程{worker_process.name}-是否存活：{worker_process.is_alive()}")

    def _join_worker_processes(self):
        print(f"用join()等待子进程结束。")
        for worker_process in self.worker_process_ls:
            worker_process.join()

    def _close_worker_pipe(self):
        for worker_pipe_out in self.worker_pipe_out_ls:
            worker_pipe_out.close()

    def begin_detecting(self):
        s = time.time()

        print("1.启动检测拼图子进程")
        # self._start_worker_processes()
        manager_worker_pipe_in_manager_ls = []

        for i in range(1, 1 + 2):
            worker_pipe_out, worker_pipe_in = Pipe(True)  # 外部用 pipe/ 内部用 pipe
            manager_worker_pipe_in_manager, manager_worker_pipe_in_worker = Pipe(True)  # 外部用 pipe/ 内部用 pipe
            worker_process = DetectProcess(worker_pipe_in,manager_worker_pipe_in_worker, f"DetectProcess_{i}")
            self.worker_process_ls.append(worker_process)
            self.worker_pipe_out_ls.append(worker_pipe_out)
            manager_worker_pipe_in_manager_ls.append(manager_worker_pipe_in_manager)
            worker_process.start()
            worker_pipe_in.close()
            manager_worker_pipe_in_worker.close()


        print("2.启动管理进程")
        self.manager_pipe_out, self.manager_pipe_in = Pipe(True)  # 外部用 pipe/ 内部用 pipe
        self.detect_process_manager = DetectProcessManager(self.manager_pipe_in, manager_worker_pipe_in_manager_ls,
                                                           "detect_process_manager")
        self.detect_process_manager.start()
        self.manager_pipe_in.close()

        print('*  ' * 10)
        print(f"耗时：{time.time() - s}")
        print("主进程: 检测任务开始成功.")
        print('*  ' * 30)

    def stop_detection(self):
        """停止检测"""
        print(f'-  -  -  -  -  -  -  -  -  -  -  -  停止检测任务 -  -  -  -  -  -  -  -  -  -  -  -  ')
        self._stop_worker_processes()

        self.manager_pipe_out.send(STOP)
        self.detect_process_manager.join()

        # 停止任务等待10s.
        for i in range(10):
            worker_process_status_ls = list()
            for worker_process in self.worker_process_ls:
                # print(f"进程{worker_process.name}-是否存活：{worker_process.is_alive()}")
                worker_process_status_ls.append(worker_process.is_alive())

            print(f"self.detect_process_manager.is_alive() = {self.detect_process_manager.is_alive()}")
            print(f"worker_process_status_ls = {worker_process_status_ls}")
            if (not self.detect_process_manager.is_alive()) and (True not in worker_process_status_ls):
                print(f"检测任务------停止任务成功")
                self.manager_pipe_out.close()
                self._close_worker_pipe()
                return
            time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    task = Task()
    task.begin_detecting()

    time.sleep(2)
    task.stop_detection()
