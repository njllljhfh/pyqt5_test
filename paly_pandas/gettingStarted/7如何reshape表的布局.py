# -*- coding:utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt

DOCUMENT_URL = 'https://pandas.pydata.org/docs/getting_started/intro_tutorials/07_reshape_table_layout.html'
titanic = pd.read_csv("data/titanic.csv")
print(titanic.head())
# print(titanic.info())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

air_quality = pd.read_csv("data/air_quality_long.csv", index_col="date.utc", parse_dates=True)
print(air_quality.head())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')
print(air_quality.info())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')
print(f'air_quality.index.is_unique = {air_quality.index.is_unique}')

print(f"""
###########################################################################################
#                                        对行进行排序                                       #
###########################################################################################
""")
print('我想根据乘客的年龄对泰坦尼克号的数据进行排序。')
print(titanic.sort_values(by="Age").head())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('我想按照船舱等级和年龄降序排列泰坦尼克号的数据。')
print(titanic.sort_values(by=['Pclass', 'Age'], ascending=False).head())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print(f"""
###########################################################################################
#                             Long to wide table format                                   #
###########################################################################################
""")
print('让我们使用空气质量数据集的一小部分。我们关注的是NO2的数据，并且只使用每个位置的前两个测量值(即每组的头部)')
no2 = air_quality[air_quality["parameter"] == "no2"]
no2_subset = no2.sort_index().groupby(["location"]).head(2)  # 按时间升序排序，并取每个分组中的前2行数据
print(no2_subset)
# print(air_quality["location"].value_counts())  # 数据集中的 location 列只有3种值
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('我想要三个站点的值作为单独的列彼此相邻')
# 注意：no2_subset 中只有6行数据
print(no2_subset.pivot(columns="location", values="value"))
# no2_subset.pivot(columns="location", values="value").plot()
# plt.show()
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('由于 pandas 支持多列绘图(参见绘图教程)开箱即用，从长表格式到宽表格式的转换允许在同一时间绘制不同的时间序列:')
print(no2.head())
# 如果没有定义index参数，则使用现有的索引(行标签)。
no2.pivot(columns="location", values="value").plot()
plt.show()
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print(f"""
###########################################################################################
#                                        Pivot table                                      #
###########################################################################################
""")
print('我想要查看 NO2和PM2.5 分别在 各个地点的平均值')
# 在pivot()的情况下，数据只是重新排列。
# 当需要聚合多个值时(在这个特定的例子中，是不同时间步上的值)，
# 可以使用pivot_table()，提供一个聚合函数(例如mean)来说明如何组合这些值。
x = air_quality.pivot_table(values="value", index="location", columns="parameter", aggfunc="mean")
print(x)
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('透视表(pivot table)是电子表格软件中一个众所周知的概念。当对每个变量的汇总列感兴趣时，将margin参数设置为True:')
x1 = air_quality.pivot_table(
    values="value",
    index="location",
    columns="parameter",
    aggfunc="mean",
    margins=True,
)
print(x1)
print('* * * * * * *')
print('取指定的列，行')
print(x['no2']['BETR801'])
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print(f"""
###########################################################################################
#                                   Wide to long format                                   #
###########################################################################################
""")
no2_pivoted = no2.pivot(columns="location", values="value").reset_index()
print(no2_pivoted.head())
print(no2_pivoted.shape)
print(no2_pivoted.index.is_unique)
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

no_2 = no2_pivoted.melt(id_vars="date.utc")
print(no_2.head())
print(no_2.shape)
print(no_2.index.is_unique)
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('panda.melt()方法可以定义得更详细:')
no_2 = no2_pivoted.melt(
    id_vars="date.utc",
    value_vars=["BETR801", "FR04014", "London Westminster"],
    value_name="NO_2",
    var_name="id_location",
)
print(no_2.head())
print(no_2.shape)
print(no_2.index.is_unique)
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

'''
REMEMBER
● Sorting by one or more columns is supported by `sort_values`
● The `pivot` function is purely restructuring of the data, `pivot_table` supports aggregations
● The reverse of `pivot` (long to wide format) is `melt` (wide to long format)
'''
