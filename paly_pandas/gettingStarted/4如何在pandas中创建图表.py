# -*- coding:utf-8 -*-
from io import BytesIO

import pandas as pd
import matplotlib.pyplot as plt

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
plt.show()
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('将图像写入文件')
ax = air_quality.plot()
print(f'type(ax) = {type(ax)}')
fig = ax.get_figure()
print(f'type(fig) = {type(fig)}')
fig.savefig('fig.png')
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('将图像二进制写入变量')
buffer = BytesIO()
plt.savefig(buffer)
plot_data = buffer.getvalue()
print(f'type(plot_data) = {type(plot_data)}')
with open('x.png', 'wb') as f:
    f.write(plot_data)
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')
