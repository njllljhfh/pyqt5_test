# -*- coding:utf-8 -*-
"""
读取存在空行的文件，删除其中的空行，并将其保存到新的文件中
"""
source_path = "./大数据分析.py"
target_path = "./大数据分析_new.py"

with open(source_path, 'r', encoding='utf-8') as fr, open(target_path, 'w', encoding='utf-8') as fd:
    for text in fr.readlines():
        line = text.split()
        # print(line)
        if line and not line[0].startswith("#"):
            if "#" in line:
                print(line)
                i = (text.index("#"))
                text = text[:i] + "\n"
            fd.write(text)
    print('输出成功....')
