# -*- coding:utf-8 -*-
import pandas as pd

DOCUMENT_URL = 'https://pandas.pydata.org/docs/getting_started/intro_tutorials/02_read_write.html'

print('我想分析泰坦尼克号的乘客数据，数据以 CSV文件 的形式提供:')
# 在读取数据之后，一定要检查数据。当显示一个DataFrame时，默认情况下将显示第一个和最后5行:
titanic = pd.read_csv("data/titanic.csv")
print(titanic)
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('我想看 pandas DataFrame 的前8行:')
print(titanic.head(8))
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('我想看 pandas DataFrame 的后10行:')
print(titanic.tail(10))
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('通过 pandas 的 dtypes 属性，可以检查 pandas 是如何解释每个列数据类型的:')
# dtypes 是 DataFrame 和 Series 的一个属性。
print(titanic.dtypes)
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('把泰坦尼克号的数据做成电子表格:')
# 没有行index
titanic.to_excel("data/titanic.xlsx", sheet_name="passengers", index=False)
# 有行index
titanic.to_excel("data/titanic_has-row-index.xlsx", sheet_name="passengers", index=True)
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('函数read_excel() 读取excel文件, 加载数据到DataFrame:')
titanic = pd.read_excel("data/titanic.xlsx", sheet_name="passengers", engine='openpyxl')
print(titanic.head())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('我对 DataFrame 的 技术总结(technical summary) 感兴趣')
print(titanic.info())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

'''
REMEMBER
● Getting data in to pandas from many different file formats or data sources is supported by read_* functions.
● Exporting data out of pandas is provided by different to_*methods.
● The head/tail/info methods and the dtypes attribute are convenient for a first check.
'''
