# -*- coding:utf-8 -*-
import pandas as pd

DOCUMENT_URL = 'https://pandas.pydata.org/docs/getting_started/intro_tutorials/10_text_data.html'

titanic = pd.read_csv("data/titanic.csv")
print(titanic)
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('使所有名称字符小写。')
print(titanic["Name"].str.lower())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('通过提取逗号前的部分，创建包含乘客姓氏的新列 Surname。')
print(titanic["Name"].str.split(","))

print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')
# titanic["Surname"] = titanic["Name"].str.split(",").str.get(0)
titanic["Surname"] = titanic["Name"].str.split(",").str[0]
print(titanic["Surname"])
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('提取泰坦尼克号上关于 countesses 的乘客数据。')
print(titanic["Name"].str.contains("Countess"))
print('* * * * * *')
print(titanic[titanic["Name"].str.contains("Countess")])
print('取 第一条数据的 Name')
print(titanic[titanic["Name"].str.contains("Countess")].iloc[0]['Name'])  # str
print('修改 第一条数据的 Name')
titanic.loc[titanic["Name"].str.contains("Countess"), 'Name'] = 'Countess 123'
print(titanic.loc[titanic["Name"].str.contains("Countess"), 'Name'])
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('泰坦尼克号上哪位乘客的名字最长?')
print(titanic["Name"].str.len())
print('获取 最长名字所在的 索引')
print(titanic["Name"].str.len().idxmax())

print('获取 最长名字')
# 基于行(307)和列(name)，我们可以使用loc操作符进行选择，该操作符在关于子集的教程中介绍过。
print(titanic.loc[titanic["Name"].str.len().idxmax(), "Name"])
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('在"Sex"栏中，将"male"的值替换为"M"，"female"的值替换为"F"。')
titanic["Sex_short"] = titanic["Sex"].replace({"male": "M", "female": "F"})
print(titanic["Sex_short"])
print(titanic['Sex'])
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('还有一个replace()方法可用来替换一组特定的字符')
titanic["Sex_short"] = titanic["Sex_short"].str.replace("F", "FF")
titanic["Sex_short"] = titanic["Sex_short"].str.replace("M", "MM")
print(titanic["Sex_short"])
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

'''
REMEMBER
● String methods are available using the `str` accessor.
● String methods work element-wise and can be used for conditional indexing.
● The `replace` method is a convenient method to convert values according to a given dictionary.
'''
