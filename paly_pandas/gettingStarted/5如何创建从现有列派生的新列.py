# -*- coding:utf-8 -*-
import pandas as pd

DOCUMENT_URL = 'https://pandas.pydata.org/docs/getting_started/intro_tutorials/05_add_columns.html'

air_quality = pd.read_csv("data/air_quality_no2.csv", index_col=0, parse_dates=True)
print(air_quality.head())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('用单位 毫克/立方米 表示NO2的浓度')
# (If we assume temperature of 25 degrees Celsius and pressure of 1013 hPa, the conversion factor is 1.882)
air_quality["london_mg_per_cubic"] = air_quality["station_london"] * 1.882
print(air_quality.head())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('检查 Paris 和 Antwerp 的值的比率，并将结果保存在一个新的列')
air_quality["ratio_paris_antwerp"] = (air_quality["station_paris"] / air_quality["station_antwerp"])
print(air_quality.head())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print(f'使用 apply() 方法自定义处理函数:')


def xxx(value):
    return value / 100


air_quality["station_antwerp_divide_100"] = air_quality["station_antwerp"].apply(xxx)
print(air_quality.head())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('重命名列:')
air_quality_renamed = air_quality.rename(
    columns={
        "station_antwerp": "BETR801",
        "station_paris": "FR04014",
        "station_london": "London Westminster",
    }
)
print(air_quality.head())
print(air_quality_renamed.head())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('映射不应该只局限于固定名称，也可以是映射函数。例如，将列名转换为小写字母也可以使用函数来完成:')
air_quality_renamed = air_quality_renamed.rename(columns=str.lower)
print(air_quality_renamed.head())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

"""
REMEMBER
● Create a new column by assigning the output to the DataFrame with a new column name in between the [].
● Operations are element-wise, no need to loop over rows.
● Use rename with a dictionary or function to rename row labels or column names.
"""
