# -*- coding:utf-8 -*-
import pandas as pd

DOCUMENT_URL = 'https://pandas.pydata.org/docs/getting_started/intro_tutorials/04_plotting.html'

# 使用 read_csv 函数的 index_col 和 parse_dates 参数,
# 将第一列(index=0的列)定义为结果 DataFrame 的索引，并将列中的日期分别转换为 Timestamp 对象。
air_quality = pd.read_csv("data/air_quality_no2.csv", index_col=0, parse_dates=True)
print(air_quality.head())

print(f"""
###########################################################################################
#                             如何从 DataFrame 中选择特定的行和列?                             #
###########################################################################################
""")
print('我要快速查看一下可视化数据。')
air_quality.plot()

print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')
