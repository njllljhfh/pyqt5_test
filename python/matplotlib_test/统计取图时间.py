# -*- coding:utf-8 -*-
# Count the time of loading images.

total_num = 0
loading_img_num = 0
with open("./logging2021-04-26.log", encoding='utf-8') as f:
    for line in f:
        if "取图总耗时" in line:
            loading_img_num += 1
        total_num += 1

print(f'total_num = {total_num}')
print(f'loading_img_num = {loading_img_num}')
