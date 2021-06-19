# -*- coding:utf-8 -*-
import os
from pprint import pprint

import numpy as np

nfs_path = '/data/public'
small_base_path = '1/20210406/883333/4175/small'
small_image_save_path = os.path.join(nfs_path, small_base_path)
print(f'small_image_save_path\t = {small_image_save_path}')

file_save_path = os.path.dirname(small_image_save_path)
print(f'file_save_path\t\t\t = {file_save_path}')
print('-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ')

path_root = os.path.dirname(os.path.abspath(__file__))
path_1 = os.path.join(path_root, 'dl_modules/huansheng_inspection_pipeline')
print(path_1)

print(os.path.dirname(path_1))

file_path_without_prefix = (os.sep + os.path.relpath(small_image_save_path, nfs_path)).replace("\\", "/")
print(f'file_path_without_prefix = {file_path_without_prefix}')
print('-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ')
xxx = 'a/b/c'
print(os.path.relpath(xxx, 'a'))
print('-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ')

a = '\\1\\2\\3'
print(a)
a = a.replace("\\", "/")
print(a)
print('-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ')

stage = "VI_TP_3"
stage_num = stage.rsplit("_", 1)[-1]  # NJL: stage_num=3 (如stage=VI_TP_3)
print(f'stage_num = {stage_num}')
print('-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ')

import random
a_ls = ["process_0", "process_1"]
index = random.randint(0, len(a_ls) - 1)
print(f'index = {index}')
print(f'a_ls.pop(index) = {a_ls.pop(index)}')
print('-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ')

merge_array = np.zeros([0, 0, 3], np.uint8)  # TP横图
pprint(merge_array)
print('-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ')

stage = "VI_TP_3"
row_num = int(stage.rsplit("_", 1)[-1])
print(f'row_num = {row_num}')
print('-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ')

# --模拟接口定义的图片名称
step = 3
img_name = ""
for i in range(step):
    img_name += chr(65 + i)
img_name += ".jpg"
print(f'img_name = {img_name}')
print('-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ')

stage = "VI_STITCH_1_2"
prev_stage_stitched = stage.rsplit("_", 1)[0]  # 已经有的纵向拼图
print(f'prev_stage_stitched = {prev_stage_stitched}')
print('-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  ')

# Agent 模拟发送异常数据
# # TODO:njl
# logger.info("TP1 VI 拍照 {}".format(MSG[Code.PLC_SCANNER_SIGNAL_ERROR]))
# time.sleep(1)
# return b'\x07\x21', PhotoResponse(code=Code.PLC_SCANNER_SIGNAL_ERROR, msg=MSG[Code.PLC_SCANNER_SIGNAL_ERROR])
# # TODO:njl
# --------------------------------------
