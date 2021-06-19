# -*- coding:utf-8 -*-
"""
测试3层进程通讯，直接用terminate强杀进程。
测试结果：
"""
import multiprocessing
import os
from multiprocessing import Process, Pipe
import time
from multiprocessing.connection import Connection


class DetectProcessManager(Process):

    def __init__(self, manager_pipe_in: Connection, count, name):
        super().__init__()
        self.manager_pipe_in = manager_pipe_in
        self.count = count
        self.name = name
        # - - -
        self.worker_process_ls = list()
        self.worker_pipe_out_ls = list()

    def _start_worker_processes(self):
        for i in range(1, 1 + 2):
            worker_pipe_out, worker_pipe_in = Pipe(True)  # 外部用 pipe/ 内部用 pipe
            worker_process = DetectProcess(worker_pipe_out, f"DetectProcess_{i}")
            self.worker_process_ls.append(worker_process)
            self.worker_pipe_out_ls.append(worker_pipe_out)
            worker_process.start()
            worker_pipe_in.close()

    def _stop_worker_processes(self):
        for worker_process in self.worker_process_ls:
            worker_process: Process
            if worker_process.is_alive():
                worker_process.terminate()
                worker_process.join()

    def _whether_processes_are_alive(self):
        for worker_process in self.worker_process_ls:
            worker_process: Process
            print(f"进程{worker_process.name}-是否存活：{worker_process.is_alive()}")

    def run(self):
        self._start_worker_processes()

        while True:
            if self.manager_pipe_in.poll():
                message = self.manager_pipe_in.recv()
                if message == "STOP":
                    self._stop_worker_processes()
                    self.manager_pipe_in.send("STOP_SUCCESSFULLY")
                    self._whether_processes_are_alive()
                    return


class DetectProcess(Process):

    def __init__(self, worker_pipe_in: Connection, name):
        super().__init__()
        self.worker_pipe_in = worker_pipe_in
        self.name = name

    def run(self):
        try:
            i = 1
            while True:
                # The recv() function:
                # Return an object sent from the other end of the connection using send().
                # Blocks until there is something to receive.
                # Raises EOFError if there is nothing left to receive and the other end was closed.
                # if self.worker_pipe_in.poll():
                #     message = self.worker_pipe_in.recv()
                #     print(f"{self.name}  进程({self.pid})  收到的管理进程信息-{message}")
                #     if message == "STOP":
                #         self.worker_pipe_in.send("STOP_SUCCESSFULLY")
                #         return

                print(f"worker进程：{self.name}, working-{i}")
                time.sleep(1)
                i += 1
        except EOFError:
            print(f"{self.name}  end consumer : EOFError")


if __name__ == '__main__':
    count = 10
    s = time.time()
    manager_pipe_out, manager_pipe_in = Pipe(True)  # 外部用 pipe/ 内部用 pipe

    detect_process_manager = DetectProcessManager(manager_pipe_in, count, "detect_process_manager")
    detect_process_manager.start()
    manager_pipe_in.close()

    for i in range(2):
        time.sleep(1)
        print(f"主进程-----{i}")
    manager_pipe_out.send("STOP")

    # 停止任务等待10s.
    for i in range(10):
        if manager_pipe_out.poll():
            result = manager_pipe_out.recv()
            print(f"停止任务 ----- result={result}")
            manager_pipe_out.close()
            print(f"进程{detect_process_manager.name}-是否存活：{detect_process_manager.is_alive()}")
            break
        time.sleep(1)

    print('*  ' * 30)
    print(f"耗时：{time.time() - s}")
    print("主进程，最后一行代码")
