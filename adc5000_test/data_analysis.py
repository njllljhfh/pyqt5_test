# -*- coding:utf-8 -*-
import os
import time


def walk_dir(root_dir):
    wafer_count = 0

    for root, dirs, files in os.walk(root_dir):
        # print(f'root: {root}')
        # print(f'dirs: {dirs}')
        # print(f'files: {files}')

        jpg_num = 0
        jpg_num_in_klarf = 0
        has_klarf = False
        for file in files:
            if file.endswith('.klarf'):
                has_klarf = True
                klarf_file_path = os.path.join(root, file)
                # print(f'klarf_file_path: {klarf_file_path}')
                with open(klarf_file_path, 'r') as f:
                    line_data = f.readline()
                    while line_data:
                        line_data = line_data.strip()
                        # print(f'line_data: {line_data}')
                        if line_data.endswith('.jpg;'):
                            jpg_num_in_klarf += 1
                        line_data = f.readline()
            elif file.endswith(('.jpg', 'jpeg')):
                jpg_num += 1

        if has_klarf:
            print(f'jpg_num={jpg_num}')
            print(f'jpg_num_in_klarf={jpg_num_in_klarf}')
            if jpg_num_in_klarf == jpg_num:
                print(f'{root}: wafer目录中数据已经保存完整')
                for file in files:
                    print(f'file = {file}')
                    file_path = os.path.join(root, file)
                    with open(file_path, 'rb') as f:
                        print(f'file_path={file_path}')
                        print(f'file_size={len(f.read())/1024/1024} MB')
                        # print(f'file_size={os.path.getsize(file_path)}')
                wafer_count += 1
                return wafer_count  # 测试
            # todo: 发送wafer_dir到消费队列
            else:
                print(f'{root}: wafer目录中数据尚未保存完整，请稍后...')
                # todo：等待一段时间后继续检查数据完整性
            print(f'- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ')

        for sub_dir in dirs:
            wafer_count += walk_dir(sub_dir)

    return wafer_count


if __name__ == '__main__':
    # wafer所在目录
    # data_root_dir = 'D:\\ADC Data\\TIH2449540\\2AI08K9M1\\B222449540-01A0'

    # 长电数据根目录
    data_root_dir = 'D:\\ADC Data'
    total_wafer_count = walk_dir(data_root_dir)
    print(f'total_wafer_count={total_wafer_count}')
