# -*- coding:utf-8 -*-
import os
import shutil

ROOT_USER = 'mc5k'

# 目录挂载
# timestamp = str(aoi_machine_info.create_date)
remote_path = '/home/dev/adc5000/data/changdian'
remote_root_dir_name = os.path.split(remote_path)[1]
remote_ip = "192.168.10.101"
home_dir = os.path.expanduser("~")
local_path = f'{home_dir}/sharedir/{remote_ip}/adc5000/{remote_root_dir_name}'
print(f'远程目录: "{remote_path}"')
print(f'本地目录: "{local_path}"')
# if not os.path.ismount(local_path):
#     if os.path.exists(local_path):
#         shutil.rmtree(local_path)
#
#     # if not os.path.exists(local_path):
#     # 新建目录
#     create_cmd = f"sudo mkdir -p {local_path}"
#     print(f'新建目录命令：{create_cmd}')
#     cmd_code = os.system("echo %s | sudo -S %s" % (ROOT_USER, create_cmd))
#     if cmd_code != 0:
#         print(f'新建目录: code={cmd_code}')
#
#     # 挂载目录
#     mount_cmd = f'sudo mount -t nfs -o rw {remote_ip}:{remote_path} {local_path}'
#     print(f'挂载目录命令：{mount_cmd}')
#     cmd_code = os.system("echo %s | sudo -S %s" % (ROOT_USER, mount_cmd))
#     if cmd_code != 0:
#         print(f'挂载目录失败: code={cmd_code}')
# else:
#     print(f'目录已挂载: 远程目录="{remote_path}", 本地目录="{local_path}"')
# --------------------------------------

if not os.path.ismount(local_path):
    if os.path.exists(local_path):
        print(f'本地目录存在，删除本地目录：{local_path}')
        shutil.rmtree(local_path)

    # 新建目录
    create_cmd = f"mkdir -p {local_path}"
    print(f'新建目录命令：{create_cmd}')
    cmd_code = os.system(create_cmd)
    if cmd_code != 0:
        print(f'新建目录: code={cmd_code}')

    # 挂载目录
    mount_cmd = f'sudo mount -t nfs -o rw {remote_ip}:{remote_path} {local_path}'
    print(f'挂载目录命令：{mount_cmd}')
    cmd_code = os.system("echo %s | sudo -S %s" % (ROOT_USER, mount_cmd))
    if cmd_code != 0:
        print(f'挂载目录失败: code={cmd_code}')
else:
    print(f'目录已挂载: 远程目录="{remote_path}", 本地目录="{local_path}"')

