# -*- coding:utf-8 -*-
import pandas as pd

DOCUMENT_URL = 'https://pandas.pydata.org/docs/getting_started/intro_tutorials/08_combine_dataframes.html'

air_quality_no2 = pd.read_csv("data/air_quality_no2_long.csv", parse_dates=True)
air_quality_no2 = air_quality_no2[["date.utc", "location", "parameter", "value"]]
print(air_quality_no2.head())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

air_quality_pm25 = pd.read_csv("data/air_quality_pm25_long.csv", parse_dates=True)
air_quality_pm25 = air_quality_pm25[["date.utc", "location", "parameter", "value"]]
print(air_quality_pm25.head())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print(f"""
###########################################################################################
#                                 Concatenating objects                                   #
###########################################################################################
""")
print('我想将两个具有类似结构的 NO2 和 PM25 的测量表组合在一个表中:')
air_quality = pd.concat([air_quality_pm25, air_quality_no2], axis=0)
print(air_quality.head())
print('* * * * * * *')
# 默认情况下，连接是沿着 轴0 进行的，因此生成的表将合并输入表的行。让我们检查原始表和连接后表的形状来验证上述操作:
print('Shape of the ``air_quality_pm25`` table: ', air_quality_pm25.shape)
print('Shape of the ``air_quality_no2`` table: ', air_quality_no2.shape)
print('Shape of the resulting ``air_quality`` table: ', air_quality.shape)
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print(f'根据datetime信息对表进行排序也说明了这两个表的合并，'
      f'参数列定义表的来源(no2来自表air_quality_no2，pm25来自表air_quality_pm25):')
air_quality = air_quality.sort_values("date.utc")
print(air_quality.head())

print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')
print(f'在这个特定的示例中，数据提供的参数列确保可以识别每个原始表。但情况并非总是如此。'
      f'concat函数用keys参数提供了一个方便的解决方案，它添加了一个附加的(分层的)行索引。例如:')
air_quality_ = pd.concat([air_quality_pm25, air_quality_no2], keys=["PM25", "NO2"])
print(air_quality_.head(air_quality_.shape[0]))
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')
