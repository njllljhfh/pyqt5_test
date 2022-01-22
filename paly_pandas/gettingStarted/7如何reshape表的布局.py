# -*- coding:utf-8 -*-
import pandas as pd

DOCUMENT_URL = 'https://pandas.pydata.org/docs/getting_started/intro_tutorials/07_reshape_table_layout.html'
titanic = pd.read_csv("data/titanic.csv")
print(titanic.head())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

air_quality = pd.read_csv("data/air_quality_long.csv", index_col="date.utc", parse_dates=True)
print(air_quality.head())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

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
