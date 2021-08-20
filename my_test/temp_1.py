# -*- coding:utf-8 -*-
# stitch_argsi = {'line_num': 'M11-L1', 'det_point': 'CH', 'detection_type': 'Module', 'weilding_machine_num': 1,
#                 'gpu_id': 0, 'image_type': 'EL', 'product_type': 'Poly', 'product_shape': [6, 24], 'cell_type': 'half',
#                 'cell_height': 166.0, 'cell_width': 83.0, 'inner_line_num': None, 'shift_camera_1': [0, 0, 0, 0],
#                 'shift_camera_2': [0, 0, 0, 0], 'shift_camera_3': [0, 0, 0, 0], 'shift_camera_4': [0, 0, 0, 0],
#                 'bright_adjust': None,
#                 'stitch_model_seg': './stitching_el/module_models/unet_for_stitching_module_el.h5',
#                 'stitch_model_cls': None, 'camera_param': './stitching_el/module_models/camera_param_module_el.pkl',
#                 'split_middle': True, 'split_all': True, 'cell_num_split': [6, 6, 6, 6],
#                 'scale_ratio_el': [3.5542168674698793, None, None, None, None, None],
#                 'scale_ratio_vi': [7.228915662650603, None, None, None, None, None], 'camera_number': 4}
# image_stitch_args = {'line_num': 'M11-L1', 'det_point': 'CH', 'detection_type': 'Module', 'weilding_machine_num': 1,
#                      'gpu_id': 0, 'image_type': 'EL', 'product_type': 'Poly', 'product_shape': [6, 24],
#                      'cell_type': 'half', 'cell_height': 166.0, 'cell_width': 83.0, 'inner_line_num': None,
#                      'shift_camera_1': [0, 0, 0, 0], 'shift_camera_2': [0, 0, 0, 0], 'shift_camera_3': [0, 0, 0, 0],
#                      'shift_camera_4': [0, 0, 0, 0], 'bright_adjust': None,
#                      'stitch_model_seg': './stitching_el/module_models/unet_for_stitching_module_el.h5',
#                      'stitch_model_cls': None,
#                      'camera_param': './stitching_el/module_models/camera_param_module_el.pkl', 'split_middle': True,
#                      'split_all': True, 'cell_num_split': [6, 6, 6, 6],
#                      'scale_ratio_el': [3.5542168674698793, None, None, None, None, None],
#                      'scale_ratio_vi': [7.228915662650603, None, None, None, None, None], 'camera_number': 4,
#                      'gpu_mem_ratio': 0.7}
#
# print(len(stitch_argsi))
# print(len(image_stitch_args))
# lost_k = list()
# not_equal_k = list()
# for k, v in image_stitch_args.items():
#     if k not in stitch_argsi:
#         lost_k.append(k)
#         continue
#
#     if v != stitch_argsi[k]:
#         not_equal_k.append(k)
#
# print(f"lost_k = {lost_k}")
# print(f"not_equal_k = {not_equal_k}")
# = =======================================

# setting_vi = {
#     # 'stitch_model_seg': './stitching_vi/module_models/sti_module_vi.0609.xml',  # 拼图算法依赖的分割模型路径
#     'stitch_model_seg': './stitching_vi/module_models/unet_for_stitching_module_vi.h5',  # 拼图算法依赖的分割模型路径
#     # 'stitch_model_cls': './stitching_vi/models/cls_for_stitch.xml',  # 拼图算法依赖的分类模型路径
#     'stitch_model_cls': None,  # 拼图算法依赖的分类模型路径
#     # 'stitch_model_sub_seg': './stitching_vi/module_models/sti_module.vi.sub.0608.h5',
#     'stitch_model_sub_seg': './stitching_vi/module_models/det_corner_points_module_vi.h5',  # 组件VI的角点模型
#     'camera_param': './stitching_vi/module_models/camera_param_module_vi.pkl',  # 相机参数路径，用于做畸变校正
#     # 'scale_ratio_vi': [1370 / 166, 1370 / 166, 1370 / 166, 1370 / 166, 1370 / 166, 1370 / 166],    # 这个是串检的
#     # 'scale_ratio_vi': [590 / 166],  # 该比例相机调整好后就不会变了，各个相机不一样，采用默认值即可
#     'scale_ratio_vi': [1200 / 166, None, None, None, None, None],
#     'gpu_mem_ratio': 0.7,
# }
#


# log_file_vi = {
#     'line_num': 'M11-L2',
#     'det_point': 'CH',  # 应该是: 'CQ'
#     'detection_type': 'Module',
#     'weilding_machine_num': 1,  # 应该是: None
#     'gpu_id': 0,
#     'image_type': 'VI',
#     'product_type': 'Single',
#     'product_shape': [6, 24],
#     'cell_type': 'half',
#     'cell_height': 158.75,  # 应该是: 166
#     'cell_width': 26.46,  # 应该是: 83
#     'inner_line_num': None,
#     'shift_camera_1': [0, 0, 0, 0],
#     'shift_camera_2': [0, 0, 0, 0],
#     'shift_camera_3': [0, 0, 0, 0],
#     'shift_camera_4': [0, 0, 0, 0],
#     'bright_adjust': None,  # 应该是: [False, False, False, False]
#     'stitch_model_seg': './stitching_vi/module_models/unet_for_stitching_module_vi.h5',
#     'stitch_model_cls': None,
#     'camera_param': './stitching_vi/module_models/camera_param_module_vi.pkl',
#     'split_middle': True,
#     'split_all': True,
#     'cell_num_split': [6, 6, 6, 6],
#     'scale_ratio_el': [3.5542168674698793, None, None, None, None, None],  # 应该是: [590 / 166, None, None, None, None, None]
#     'scale_ratio_vi': [7.228915662650603, None, None, None, None, None],  # 应该是: [590 / 166, None, None, None, None, None]
#     'camera_number': 4,
#     'gpu_mem_ratio': 0.7,
#     'stitch_model_sub_seg': './stitching_vi/module_models/det_corner_points_module_vi.h5'
# }
#
# not_equal_k_list = list()
# for k, v in setting_vi.items():
#     if v != log_file_vi[k]:
#         not_equal_k_list.append(k)
#
# print(f"not_equal_k_list = {not_equal_k_list}")


# ===============================================================

# x = {
#     'line_num': 'M11-L1',
#     'det_point': 'CQ',
#     'detection_type': 'Module',
#     'weilding_machine_num': 1,
#     'gpu_id': 0,
#     'image_type': 'VI',
#     'product_type': 'Single',
#     'product_shape': [6, 24],
#     'cell_type': 'half',
#     'cell_height': 166.0,
#     'cell_width': 83.0,
#     'inner_line_num': None,
#     'shift_camera_1': [0, 0, 0, 0],
#     'shift_camera_2': [0, 0, 0, 0],
#     'shift_camera_3': [0, 0, 0, 0],
#     'shift_camera_4': [0, 0, 0, 0],
#     'bright_adjust': [False, False, False, False],
#     'stitch_model_seg': './stitching_vi/module_models/unet_for_stitching_module_vi.h5',
#     'stitch_model_cls': None,
#     'camera_param': './stitching_vi/module_models/camera_param_module_vi.pkl',
#     'split_middle': True,
#     'split_all': True,
#     'cell_num_split': [6, 6, 6, 6],
#     'scale_ratio_el': [3.5542168674698793, None, None, None, None, None],
#     'scale_ratio_vi': [3.5542168674698793, None, None, None, None, None],
#     'camera_number': 4,
#     'gpu_mem_ratio': 0.7,
#     'stitch_model_sub_seg': './stitching_vi/module_models/det_corner_points_module_vi.h5'
# }
#
# import os
#
# a = '/home/being/Project/JN2000/WD4/matrixsolar_ats/dl_modules/half_cell_pv_module_inspection/'
# b = 'stitching_vi/module_models/det_corner_points_module_vi.h5'
#
# print(os.path.join(a, b))
#
# c = '/home/being/Project/JN2000/WD4/matrixsolar_ats/dl_modules/half_cell_pv_module_inspection\stitching_vi/module_models/det_corner_points_module_vi.h5'

# =========================================
# import time
#
# import requests
# from multiprocessing import Process, Pool
#
#
# def asdfg():
#     for i in range(10000):
#         r = requests.get('http://10.1.0.157:8080/ping')
#         # print(f"{r.text}")
#
#
# if __name__ == '__main__':
#     t = lambda: time.time()
#     s = t()
#     pool = Pool(processes=10)
#     for i in range(10):
#         pool.apply_async(asdfg)
#     pool.close()
#     pool.join()
#
#     print(f"consumed_time = {t() - s}")


# ================================

# import multiprocessing
# import time
#
# import requests
#
#
# def req():
#     for i in range(10000):
#         requests.get('http://10.0.1.12:8080/ping')
#
#
# if __name__ == '__main__':
#     start = time.time()
#     pool = multiprocessing.Pool(processes=10)
#     for i in range(10):
#         pool.apply_async(req)
#     pool.close()
#     pool.join()
#     end = time.time()
#
#     print(end - start)

# ==================================================
# import datetime
# from threading import Timer
# MonitorSystem = lambda :print(f"cpu:1.4%, mem:93.2%")
# MonitorNetWork = lambda :print(f"bytessent=171337324, bytesrecv=1109002349")
# #记录当前时间
# print(datetime.datetime.now())
# #3S执行一次
# sTimer = Timer(3, MonitorSystem)
# #1S执行一次
# nTimer = Timer(1, MonitorNetWork)
# #使用线程方式执行
# sTimer.start()
# nTimer.start()
# #等待结束
# sTimer.join()
# nTimer.join()
# #记录结束时间
# print(datetime.datetime.now())
# ===================================
# import time
# import _thread
# import threading
# from contextlib import contextmanager
#
#
# @contextmanager
# def time_limit(seconds):
#     """ 限制执行的时间 with """
#     timer = threading.Timer(seconds, lambda: _thread.interrupt_main())
#     timer.start()
#     try:
#         yield
#     except KeyboardInterrupt:
#         raise TimeoutError(f"Timed out: {seconds}s")
#     finally:
#         # if the action ends in specified time, timer is canceled
#         timer.cancel()
#
#
# if __name__ == '__main__':
#     try:
#         with time_limit(3) as a:
#             time.sleep(4)
#     except TimeoutError as e:
#         print(e)

# =====================================

import time
from multiprocessing import Process, process, Pipe, connection

STOP = "STOP"
SUB_PROCESS_STOP_SUCCESS = "SUB_PROCESS_STOP_SUCCESS"


class MG(Process):

    def __init__(self, name, sub_process_ls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self._sub_process_ls = sub_process_ls
        self._sub_process_pipe_ls = list()
        for sub_process in self._sub_process_ls:
            self._sub_process_pipe_ls.append(sub_process.pipe0)

        self._pipes = Pipe()

    @property
    def pipe0(self):
        return self._pipes[0]

    @property
    def pipe1(self):
        return self._pipes[1]

    def run(self):
        while True:
            if connection.wait([self.pipe1], timeout=0):
                msg = self.pipe1.recv()
                if msg == STOP:
                    if self._quit():
                        return
                print(f"[{self.name}] msg = {msg}")

            for sub_pipe in connection.wait(self._sub_process_pipe_ls, timeout=0):
                msg = sub_pipe.recv()
                print(f"[{self.name}] 收到子进程信息：{msg}")

    def _quit(self):
        # for sub_pipe in self._sub_process_pipe_ls:
        #     print(f"[{self.name}] 发送停止信号")
        #     sub_pipe.send(STOP)
        for sub_pipe in self._sub_process_pipe_ls:
            sub_pipe.quit()

        stopped_sub = 0
        while True:
            if stopped_sub == len(self._sub_process_pipe_ls):
                return True

            for sub_pipe in connection.wait(self._sub_process_pipe_ls, timeout=0):
                msg = sub_pipe.recv()
                if msg == SUB_PROCESS_STOP_SUCCESS:
                    print(f"[{self.name}] 收到子进程信息：{msg}")
                    stopped_sub += 1


class Worker(Process):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self._pipes = Pipe()

    @property
    def pipe0(self):
        return self._pipes[0]

    @property
    def pipe1(self):
        return self._pipes[1]

    def run(self):
        i = 0
        while True:
            if connection.wait([self.pipe1], timeout=0):
                msg = self.pipe1.recv()
                if msg == STOP:
                    print(f"[{self.name}] 子进程收到管理进程信息：{msg}")
                    self.pipe1.send(SUB_PROCESS_STOP_SUCCESS)
                    return
            self.pipe1.send(f"[{self.name}] {self.pid}---{i}")
            i += 1
            time.sleep(1)

    def quit(self):

        pass


def main():
    worker1 = Worker("work1")
    worker2 = Worker("work2")
    mg = MG("mg", [worker1, worker2])

    mg.start()
    worker1.start()
    worker2.start()

    time.sleep(3)

    mg.pipe0.send(STOP)


if __name__ == '__main__':
    main()
