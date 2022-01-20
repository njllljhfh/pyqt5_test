# -*- coding:utf-8 -*-
import pandas as pd

DOCUMENT_URL = 'https://pandas.pydata.org/docs/getting_started/intro_tutorials/03_subset_data.html'
'''
This tutorial uses the Titanic data set, stored as CSV. The data consists of the following data columns:
    PassengerId: Id of every passenger.
    Survived: This feature have value 0 and 1. 0 for not survived and 1 for survived.
    Pclass: There are 3 classes: Class 1, Class 2 and Class 3.
    Name: Name of passenger.
    Sex: Gender of passenger.
    Age: Age of passenger.
    SibSp: Indication that passenger have siblings and spouse.
    Parch: Whether a passenger is alone or have family.
    Ticket: Ticket number of passenger.
    Fare: Indicating the fare.
    Cabin: The cabin of passenger.
    Embarked: The embarked category.
'''

titanic = pd.read_csv("data/titanic.csv")
print(titanic.head())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print(f"""
###########################################################################################
#                             如何从 DataFrame 中选择特定的列?                                #
###########################################################################################
""")
print('我对泰坦尼克号乘客的年龄很感兴趣:')
# DataFrame 中的每一列都是 Series。当选择单个列时，返回的对象是 panda Series。
ages = titanic["Age"]
print(ages.head())
# 返回 Series 和 DataFrame 包含行和列的数量:(行数, 列数)
# Series 是一维的，只返回行数。 本例中返回值为：(891,)
print(f'看看输出的shape: {ages.shape}。 shape的类型是: {type(ages.shape)}')
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('我对泰坦尼克号乘客的 年龄 和 性别 感兴趣。')
# 返回的数据类型是一个 pandas DataFrame
age_sex = titanic[["Age", "Sex"]]  # <class 'pandas.core.frame.DataFrame'>
print(age_sex.head())
# 记住，DataFrame 是二维的，有行维度和列维度
print(f'看看输出的shape: {age_sex.shape}')
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print(f"""
###########################################################################################
#                             如何从 DataFrame 中过滤特定的行?                                #
###########################################################################################
""")
print(f'我感兴趣的是35岁以上的乘客。')
above_35 = titanic[titanic["Age"] > 35]
print(above_35.head())
print(f'满足 Age > 35 的行数: {above_35.shape}')
print("* * * * * * * * * * * * * * * * * * ")
# 这样的一个布尔值 Series 可以用来过滤 DataFrame，方法是将它放在选择括号[]之间。只有值为True的行才会被选中。
print(titanic["Age"] > 35)  # 一个布尔值的 Series
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('我对泰坦尼克号2级和3级的乘客感兴趣。')
class_23 = titanic[titanic["Pclass"].isin([2, 3])]
print(class_23.head())
print("* * * * * * * * * * * * * * * * * * ")

# 上面的语法等价于下面的语法。
#   运算符`|` 是 `或运算`
#   运算符`&` 是 `与运算`
class_23 = titanic[(titanic["Pclass"] == 2) | (titanic["Pclass"] == 3)]
print(class_23.head())
print(f'看看输出的shape: {class_23.shape}')
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('我想研究已知年龄的乘客数据')
age_no_na = titanic[titanic["Age"].notna()]
print(age_no_na.head())
print(f'看看输出的shape: {age_no_na.shape}')
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print(f"""
###########################################################################################
#                             如何从 DataFrame 中选择特定的行和列?                             #
###########################################################################################
""")
print('我对35岁以上乘客的名字很感兴趣。')
# 逗号之前的部分是您想要的行，逗号之后的部分是您想要选择的列。
adult_names = titanic.loc[titanic["Age"] > 35, "Name"]
print(type(adult_names))
print(adult_names.head())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('我感兴趣的是 第10行到第25行 和 第3列到第5列。')
print(titanic.iloc[9:25, 2:5])
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('当使用loc或iloc选择特定的行 和/或 列时，可以为所选数据分配新值。例如，将名称anonymous赋给第三列的前3个元素:')
titanic.iloc[0:3, 3] = "anonymous"
print(titanic['Name'])
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

'''
REMEMBER
● When selecting subsets of data, square brackets [] are used.
● Inside these brackets, you can use a single column/row label, a list of column/row labels, a slice of labels, a conditional expression or a colon.
● Select specific rows and/or columns using loc when using the row and column names
● Select specific rows and/or columns using iloc when using the positions in the table
● You can assign new values to a selection based on loc/iloc.
'''
