# -*- coding:utf-8 -*-
import re


#
#
# # 自定义排序函数，提取字符串的尾部数字并作为关键字排序
# def sort_by_numeric_suffix(s):
#     # 使用正则表达式匹配字符串末尾的数字或数字序列
#     match = re.search(r'(\d+)$', s)
#     return int(match.group())
#
#
# # 待排序的字符串列表
# string_list = ["apple3", "apple12", "apple1", "apple0", "apple42", "apple100"]
#
# # 使用自定义的排序函数对字符串列表进行排序
# sorted_list = sorted(string_list, key=sort_by_numeric_suffix)
#
# # 打印排序后的结果
# for s in sorted_list:
#     print(s)
#
# print('-' * 30)
#
# import re
#
# # 原始字符串
# # text = "apple,banana;cherry|date"
# # text = "VI_VI_362307271161687_1_1.jpg"
# text = "VI_VI_PE01202308220616_10.jpg"
#
# # 使用正则表达式匹配多种分隔符
# # 此示例中的分隔符包括逗号、分号和竖线
# split_pattern = r'[-_]'
#
# # 使用 re.split() 方法来分割字符串
# result = re.split(split_pattern, text.split('.')[0])
#
# # 打印分割后的结果
# print(result)
# print(result[-2:])
# print(result[-2].isdigit())
# print(result[-1].isdigit())
import time


def sort_image_file_path(string, split_pattern=r'[-_]'):
    # 去掉后缀
    string = string.split('.')[0]
    # 用指定的字符分割
    result = re.split(split_pattern, string)
    # 取最后两个元素
    e_ls = result[-2:]

    # 转成int用于排序
    num_str = ''
    for e in e_ls:
        if e.isdigit():
            num_str += e
    if num_str.count("0") == len(num_str):
        num_str = "0"
    else:
        num_str = num_str.lstrip("0")
    return int(num_str)


if __name__ == '__main__':
    file_path_ls = ['D:/光伏组件数据/算法联调VI拼图/1/1/VI_VI_PE01202308220616_0.jpg',
                    'D:/光伏组件数据/算法联调VI拼图/1/1/VI_VI_PE01202308220616_1.jpg',
                    'D:/光伏组件数据/算法联调VI拼图/1/1/VI_VI_PE01202308220616_10.jpg',
                    'D:/光伏组件数据/算法联调VI拼图/1/1/VI_VI_PE01202308220616_11.jpg',
                    'D:/光伏组件数据/算法联调VI拼图/1/1/VI_VI_PE01202308220616_2.jpg',
                    'D:/光伏组件数据/算法联调VI拼图/1/1/VI_VI_PE01202308220616_3.jpg',
                    'D:/光伏组件数据/算法联调VI拼图/1/1/VI_VI_PE01202308220616_4.jpg',
                    'D:/光伏组件数据/算法联调VI拼图/1/1/VI_VI_PE01202308220616_5.jpg',
                    'D:/光伏组件数据/算法联调VI拼图/1/1/VI_VI_PE01202308220616_6.jpg',
                    'D:/光伏组件数据/算法联调VI拼图/1/1/VI_VI_PE01202308220616_7.jpg',
                    'D:/光伏组件数据/算法联调VI拼图/1/1/VI_VI_PE01202308220616_8.jpg',
                    'D:/光伏组件数据/算法联调VI拼图/1/1/VI_VI_PE01202308220616_9.jpg']

    file_path_ls_2 = ['D:/光伏组件数据/算法联调VI拼图/images_vi_1/VI_VI_PE01202308220616_0_0.jpg',
                      'D:/光伏组件数据/算法联调VI拼图/images_vi_1/VI_VI_PE01202308220616_0_1.jpg',
                      'D:/光伏组件数据/算法联调VI拼图/images_vi_1/VI_VI_PE01202308220616_0_2.jpg',
                      'D:/光伏组件数据/算法联调VI拼图/images_vi_1/VI_VI_PE01202308220616_0_3.jpg',
                      'D:/光伏组件数据/算法联调VI拼图/images_vi_1/VI_VI_PE01202308220616_1_0.jpg',
                      'D:/光伏组件数据/算法联调VI拼图/images_vi_1/VI_VI_PE01202308220616_1_1.jpg',
                      'D:/光伏组件数据/算法联调VI拼图/images_vi_1/VI_VI_PE01202308220616_1_2.jpg',
                      'D:/光伏组件数据/算法联调VI拼图/images_vi_1/VI_VI_PE01202308220616_1_3.jpg',
                      'D:/光伏组件数据/算法联调VI拼图/images_vi_1/VI_VI_PE01202308220616_2_0.jpg',
                      'D:/光伏组件数据/算法联调VI拼图/images_vi_1/VI_VI_PE01202308220616_2_1.jpg',
                      'D:/光伏组件数据/算法联调VI拼图/images_vi_1/VI_VI_PE01202308220616_2_2.jpg',
                      'D:/光伏组件数据/算法联调VI拼图/images_vi_1/VI_VI_PE01202308220616_2_3.jpg']

    file_path_ls.sort(key=sort_image_file_path)
    for i in file_path_ls:
        print(i)
    print("- " * 30)

    file_path_ls_2.sort(key=sort_image_file_path)
    for i in file_path_ls_2:
        print(i)
    print("- " * 30)


    import datetime

    # 获取当前的 GMT 时间
    current_time_gmt = datetime.datetime.utcnow()
    print(datetime.datetime.utcnow().timestamp())

    # 获取 GMT 时间的时间戳（UNIX 时间戳，以秒为单位）
    timestamp_gmt = int(current_time_gmt.timestamp())

    # 原始字符串
    text = "example"

    # 添加 GMT 时间戳
    result = text + "_" + str(timestamp_gmt)

    print(result)
    for i in range(10):
        print(text+f"{time.time()}")
