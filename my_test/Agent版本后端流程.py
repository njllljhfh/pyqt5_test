# -*- coding:utf-8 -*-


# detect_progress.py 往 detect_manager.py 发的信号
stage1 = [
    ('DETECT_START', True or False, 'int类型的进程id'),  # 开始检测: 检测子进程开始成功时、检测子进程开始失败时
    (stage, True, (merge_array, cut_box, detect_res_msg, res_point)),  # '横向拼图和检测'完成时。第二个参数 True 表示 finished
    (stage, True, (image_array, cut_box)),  # '纵向拼图和检测'完成时。第二个参数 True 表示 finished
    (stage, True, (big_defect_info, quantize_all_defect_info)),  # '最终拼图和检测'完成时。第二个参数 True 表示 finished
]
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# detect_manager.py 往 camera.py 发的信号
stage2 = [
    ('DETECT_START', True or False),  # 开始检测: 开始成功时、开始失败时
    ('STOP', True),  # 停止：检测子进程报错时、
    # - - - 检测过程中的信号 - - -
    ("PRODUCT_CODE", True),  # 收到 产品条码
    ("END", ok_ng_err),  # detect_manager.py正在执行产品最终步骤。通知外部结果，先出板，再保存数据
]
# camera.py 往 detect_manager.py 发的信号
stage3 = [
    ("STOP", None),  # 客户端请求 停止检测任务
    # - - - 检测过程中的信号 - - -
    ("PRODUCT_CODE", item.bar_code),  # 产品条形码
    ("VI_TP_1", image_list),  # 某个TP的4个图像(已按照相机位置排序的图像)。 例如VI图的TP1阶段
    ("END", None),  # 当前检测的产品所有阶段的图像都发送结束后,会收到该信号。
]
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# camera.py 往 monitor_agent.py 发的信号
stage4 = [
    ('TASK_START', True),  # 检测任务启动成功时
]

# monitor_agent.py 往 camera.py 发的信号
stage5 = [
    'STOP',  # 客户端请求 停止检测任务  # 这个信号去掉。
]
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# camera.py 的 stop() 有问题
pass

# 客户端请求停止检测任务, camera.py 与 detect_manager.py 间的信号传递有问题。
pass
