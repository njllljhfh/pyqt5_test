# -*- coding:utf-8 -*-
"""
测试3层进程通讯，通过逐层的进程通信，来停止进程。
测试结果：
"""
import multiprocessing
import os
import random
from multiprocessing import Process, Pipe
import time
from multiprocessing import connection
from multiprocessing.connection import Connection

STOP_SUCCESSFULLY = "STOP_SUCCESSFULLY"
STOP = "STOP"

SLEEP_TIME = 0.3

# END_IMG = '图像-6'


class DetectProcessManager(Process):

    def __init__(self, manager_pipe_in: Connection, manager_agent_pipe_in_manager: Connection, name):
        super().__init__()
        self.manager_pipe_in = manager_pipe_in
        self.manager_agent_pipe_in_manager = manager_agent_pipe_in_manager
        self.name = name
        # - - -
        self.worker_process_ls = list()
        self.worker_pipe_out_ls = list()
        self.free_worker_pipe_out_ls = list()
        # - - -
        self.flag_stop = False

    def _start_worker_processes(self):
        for i in range(1, 1 + 2):
            worker_pipe_out, worker_pipe_in = Pipe(True)  # 外部用 pipe/ 内部用 pipe
            worker_process = DetectProcess(worker_pipe_in, f"DetectProcess_{i}")
            self.worker_process_ls.append(worker_process)
            self.worker_pipe_out_ls.append(worker_pipe_out)
            self.free_worker_pipe_out_ls.append(worker_pipe_out)
            worker_process.start()
            worker_pipe_in.close()
        print(f'self.worker_pipe_out_ls = {self.worker_pipe_out_ls}')

    def _stop_worker_processes(self):
        for worker_out_pipe in self.worker_pipe_out_ls:
            worker_out_pipe.send(STOP)

    def _worker_processes_are_alive(self):
        """判断自己成是否存活"""
        for worker_process in self.worker_process_ls:
            worker_process_is_alive = worker_process.is_alive()
            print(f"进程{worker_process.name}-是否存活：{worker_process_is_alive}")
            if worker_process_is_alive:
                return True

        return False

    def _join_worker_processes(self):
        print(f"用join()等待子进程结束。")
        for worker_process in self.worker_process_ls:
            worker_process.join()

    def run(self):
        self._start_worker_processes()

        while True:
            print(f'self.manager_pipe_in.poll(): {self.manager_pipe_in.poll()}')
            if self.manager_pipe_in.poll():
                message = self.manager_pipe_in.recv()
                if message == STOP:
                    """
                    管理进程收到停止时：
                        1.记录下来停止请求。
                        2.执行完当前正在检测的产品。
                        3.通知Agent停止
                        4.停止子进程
                        5.通知主进程，停止成功
                    """
                    print(f'进程{self.name}: manager_pipe_in收到主进程的 STOP 信号: {message}')
                    self.flag_stop = True
                    # - - -

            print(1111111111111111111111111111111111)

            # 处理 worker 子进程的结果数据, 发给 Agent.
            for worker_pipe_out in connection.wait(self.worker_pipe_out_ls, timeout=0):
                message = worker_pipe_out.recv()
                print(f'{self.name}: manager进程收到 子进程处理的结果数据: {message}')
                if worker_pipe_out not in self.free_worker_pipe_out_ls:
                    self.free_worker_pipe_out_ls.append(worker_pipe_out)
                self.manager_agent_pipe_in_manager.send(message)
                # - - -

                if message == "worker处理完的数据新任务(图像-6)" and self.flag_stop:  # 模拟最后一条产品数据(END)
                    # 给Agent发 STOP
                    self.manager_agent_pipe_in_manager.send(STOP)

                    # 给 worker 子进程发停止。
                    self._stop_worker_processes()
                    print(f'等待子进程关闭')
                    for i in range(30):
                        if not self._worker_processes_are_alive():
                            print(4444444444444444444444444444444444)
                            # 给主进程发停止
                            self.manager_pipe_in.send(STOP_SUCCESSFULLY)

                            self.manager_agent_pipe_in_manager.close()
                            self.manager_pipe_in.close()
                            return
                        time.sleep(0.5)

            print(2222222222222222222222222222222222)

            # 处理Agent数据, 发给 worker 子进程
            if self.manager_agent_pipe_in_manager.poll():
                message = self.manager_agent_pipe_in_manager.recv()
                print(f'进程{self.name}: manager_agent_pipe_in_manager收到ImageAgent数据: {message}')

                if self.free_worker_pipe_out_ls:
                    index = random.randint(0, len(self.free_worker_pipe_out_ls) - 1)
                    worker_pipe_out = self.free_worker_pipe_out_ls.pop(index)
                    worker_pipe_out.send(f"新任务({message})")

            print(3333333333333333333333333333333333)

            time.sleep(SLEEP_TIME)


class DetectProcess(Process):

    def __init__(self, worker_pipe_in: Connection, name):
        super().__init__()
        self.worker_pipe_in = worker_pipe_in
        self.name = name

    def run(self):
        try:
            i = 1
            while True:
                # print(f"worker进程：{self.name}, working-{i}")
                print(f'worker进程：{self.name}, self.worker_pipe_in.poll()={self.worker_pipe_in.poll()}')

                if self.worker_pipe_in.poll():
                    message = self.worker_pipe_in.recv()
                    print(f"{self.name}  进程({self.pid})  worker收到的管理进程信息 - {message}")
                    if message == STOP:
                        # self.worker_pipe_in.send((STOP_SUCCESSFULLY, self.pid))
                        self.worker_pipe_in.close()
                        print(f"{self.name}  进程({self.pid})  return")
                        return
                    else:
                        self.worker_pipe_in.send(f"worker处理完的数据{message}")

                time.sleep(SLEEP_TIME)
                i += 1
        except EOFError:
            print(f"{self.name}  end consumer : EOFError")


class ImageAgent(Process):
    """模拟Grpc Agent 服务器"""

    def __init__(self, manager_agent_pipe_in_agent: Connection, name):
        super().__init__()
        self.manager_agent_pipe_in_agent = manager_agent_pipe_in_agent
        self.name = name

    def run(self):
        i = 1
        while True:
            image = f"图像-{i}"
            if i <= 6:
                print(f'{self.name} 生产图像 {image}')
                self.manager_agent_pipe_in_agent.send(image)
            else:
                pass

            if self.manager_agent_pipe_in_agent.poll():
                message = self.manager_agent_pipe_in_agent.recv()
                print(f"{self.name}  进程({self.pid})  ImageAgent收到的管理进程信息 - {message}")
                if message == STOP:
                    self.manager_agent_pipe_in_agent.close()
                    print(f"{self.name}  进程({self.pid})  ImageAgent 进程 return。")
                    return

            time.sleep(0.2)
            i += 1


if __name__ == '__main__':
    count = 10
    s = time.time()
    manager_pipe_out, manager_pipe_in = Pipe(True)  # 外部用 pipe/ 内部用 pipe

    manager_agent_pipe_in_agent, manager_agent_pipe_in_manager = Pipe(True)  # Agent 与 manager 进程通信使用的pipe.

    # 启动管理进程
    detect_process_manager = DetectProcessManager(manager_pipe_in, manager_agent_pipe_in_manager,
                                                  "detect_process_manager")
    detect_process_manager.start()
    manager_pipe_in.close()
    manager_agent_pipe_in_manager.close()

    # 启动Agent进程
    image_agent = ImageAgent(manager_agent_pipe_in_agent, "ImageAgent")
    image_agent.start()
    manager_agent_pipe_in_agent.close()

    for i in range(2):
        time.sleep(SLEEP_TIME)
        print(f"主进程-----{i}")

    print(f'-  -  -  -  -  -  -  -  -  -  -  -  停止检测任务 -  -  -  -  -  -  -  -  -  -  -  -  ')
    manager_pipe_out.send(STOP)

    # 停止任务等待10s.
    for i in range(10):
        if manager_pipe_out.poll():
            result = manager_pipe_out.recv()
            print(f"-----停止检测任务结果----- result = {result}")
            manager_pipe_out.close()

            # detect_process_manager.join()
            # image_agent.join()

            print(f"进程{detect_process_manager.name}-是否存活：{detect_process_manager.is_alive()}")
            print(f"进程{image_agent.name}-是否存活：{image_agent.is_alive()}")
            break
        time.sleep(SLEEP_TIME)

    print('*  ' * 30)
    print(f"耗时：{time.time() - s}")
    print("主进程，最后一行代码")
