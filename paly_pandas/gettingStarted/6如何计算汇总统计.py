# -*- coding:utf-8 -*-
import pandas as pd

DOCUMENT_URL = 'https://pandas.pydata.org/docs/getting_started/intro_tutorials/06_calculate_statistics.html'
titanic = pd.read_csv("data/titanic.csv")
print(titanic.head())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('聚合数据(Aggregating statistics)')
# 默认情况下，操作通常会排除丢失的数据，并跨行操作。
print('泰坦尼克号旅客的平均年龄')
print(titanic["Age"].mean())
print('泰坦尼克号旅客的平均年龄')
print(titanic["Age"].median())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('泰坦尼克号乘客年龄的中位数和票价的中位数是多少?')
print(titanic[["Age", "Fare"]].median())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('describe()函数：')
print(titanic[["Age", "Fare"]].describe())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('可以使用DataFrame.agg()方法为给定的列定义聚合统计信息的特定组合')
print(titanic.agg(
    {
        "Age": ["min", "max", "median", "skew"],
        "Fare": ["min", "max", "median", "mean"],
    }
))
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('汇总按类别分组的统计信息')
print(titanic[["Sex", "Age"]].groupby("Sex").mean())
