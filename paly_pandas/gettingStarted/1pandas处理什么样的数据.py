# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np

DOCUMENT_URL = 'https://pandas.pydata.org/docs/getting_started/intro_tutorials/01_table_oriented.html'

print(f"""
###########################################################################################
#                                   pandas data table                                     #
###########################################################################################
""")
df = pd.DataFrame(
    {
        "Name": [
            "Braund, Mr. Owen Harris",
            "Allen, Mr. William Henry",
            "Bonnell, Miss. Elizabeth",
        ],
        "Age": [22, 35, 58],
        "Sex": ["male", "male", "female"],
    }
)
print(df)
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('我只是对 Age 这一栏的数据感兴趣:')
# DataFrame 中的单独一列的数据类型是：pandas Series.
print(df["Age"])
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('也可以从零开始创建 Series:')
# pandas Series 没有列标签，因为它只是 DataFrame 中的一个列。 Series 有行标签。
ages = pd.Series([22, 35, 58], name="Age")
print(ages)
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print(f"""
###########################################################################################
#                        Do something with a DataFrame or Series                          #
###########################################################################################
""")
print('我想知道乘客的最大年龄:')
max_age = df["Age"].max()
print(max_age)
print(type(max_age))
print('*** 或者 ***')
print(ages.max())
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

print('对数据表中的 数字 数据进行一些基本的统计操作')
# 因为 Name 和 Sex 列是文本数据，所以 describe() 方法默认情况下不会考虑到它们。
print(df.describe())
# print(type(df.describe()))  # <class 'pandas.core.frame.DataFrame'>
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n')

"""
REMEMBER
● Import the package, aka `import pandas as pd`
● A table of data is stored as a pandas `DataFrame`
● Each column in a DataFrame is a `Series`
● You can do things by applying a method to a `DataFrame` or `Series`
"""
