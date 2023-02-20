# -*- coding:utf-8 -*-
import plotly.express as px

df = px.data.tips()

# fig = px.histogram(df, x="total_bill")

# Here we use a column with categorical data
fig = px.histogram(df, x="day")

fig.show()

# 转换为 html 文件格式
# html_context = fig.to_html()
# html_path = './ploty.html'
# with open(html_path, 'w') as f:
#     f.write(html_context)
