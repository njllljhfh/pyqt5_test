# -*- coding:utf-8 -*-
import pandas as pd

DOCUMENT_URL = 'https://pandas.pydata.org/docs/getting_started/intro_tutorials/06_calculate_statistics.html'
titanic = pd.read_csv("data/titanic.csv")
print(titanic.head())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print(f"""
###########################################################################################
#                             聚合数据(Aggregating statistics)                             #
###########################################################################################
""")
# 默认情况下，操作通常会排除丢失的数据，并跨行操作。
print('泰坦尼克号旅客的平均年龄')
print(titanic["Age"].mean())
print('泰坦尼克号旅客的年龄中位数(二分之一分位数)')
print(titanic["Age"].median())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('泰坦尼克号乘客年龄的中位数和票价的中位数是多少?')
print(titanic[["Age", "Fare"]].median())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('describe()函数：')
print(titanic[["Age", "Fare"]].describe())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('可以使用DataFrame.agg()方法为给定的列定义聚合统计信息的 自定义组合')
print(titanic.agg(
    {
        "Age": ["min", "max", "median", "skew"],
        "Fare": ["min", "max", "median", "mean"],
    }
))
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print(f"""
###########################################################################################
#                                    汇总按类别分组的统计信息                                 #
###########################################################################################
""")
print('泰坦尼克号男女乘客的平均年龄是多少:')
print(titanic[["Sex", "Age"]].groupby("Sex").mean())  # DataFrame
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('在前面的示例中，我们首先显式地选择了这2列。如果不是，则对包含数字列的每一列应用 mean 方法:')
print(titanic.groupby("Sex").mean())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('如果我们只对每个性别的平均年龄感兴趣，已分组的数据也支持选择列')
print(titanic.groupby("Sex")["Age"].mean())  # Series
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('Pclass 列的值设为 categories 类型')
titanic['Pclass'] = titanic['Pclass'].astype('category')
print(titanic.groupby("Sex").mean())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('自定义 categories 类型的列的排序顺序')
document_url = 'https://pandas.pydata.org/docs/user_guide/categorical.html#sorting-and-order'
s = pd.Series([1, 2, 3, 1], dtype="category")
s = s.cat.set_categories([2, 3, 1], ordered=True)
print(s)
print('* * * * * ')
s.sort_values(inplace=True)
print(s)
print('* * * * * ')
print(f's.min()={s.min()}, s.max()={s.max()}')
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('每个 性别和舱位组合 的平均票价是多少')
print(titanic.groupby(["Sex", "Pclass"])["Fare"].mean())  # <class 'pandas.core.series.Series'>
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print(f"""
###########################################################################################
#                                      按类别统计记录的数量                                  #
###########################################################################################
""")
# value_counts()方法计算列中每个类别的记录数量。
print(titanic["Pclass"].value_counts())
print('* * * * *')
# value_counts()该函数是一种快捷方式，因为它实际上是一种分组操作，并结合对每组中记录的数量进行计数:
print(titanic.groupby("Pclass")["Pclass"].count())
# size和count都可以与groupby结合使用。size包含NaN值，并且只提供行数(表的大小)，而count不包含缺少的值。
# 在value_counts方法中，使用dropna参数来设置包含或排除NaN值。
print(titanic.groupby("Pclass")["Pclass"].size())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

'''
split-apply-combine pattern
● Split the data into groups
● Apply a function to each group independently
● Combine the results into a data structure
'''
