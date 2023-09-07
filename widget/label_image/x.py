# -*- coding:utf-8 -*-
import re

# 匹配0到20之间的数字
pattern = r"^(0|1?\d|20)$"

# 测试输入的字符串
# test_strings = ["0", "5", "10", "15", "20", "21", "-1"]
test_strings = [str(i) for i in range(22)]
test_strings.append("-1")
test_strings.append("22")

for string in test_strings:
    if re.match(pattern, string):
        print(f"'{string}' 匹配成功")
    else:
        print(f"'{string}' 匹配失败")
