# -*- coding:utf-8 -*-


class Aaa(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y


a_ls = [Aaa(i, i * 10) for i in range(10)]
print(a_ls)

print('x_min: ', min([a.x for a in a_ls]))
print('y_min: ', min([a.y for a in a_ls]))
print('x_max: ', max([a.x for a in a_ls]))
print('y_max: ', max([a.y for a in a_ls]))
print('- ' * 40)


x_min = 0  # 没有缩放的值
x_max = 0
y_min = 0
y_max = 0
for a in a_ls:
    x_min = min([x_min, a.x])
    x_max = max([x_max, a.x])
    y_min = min([y_min, a.y])
    y_max = max([y_max, a.y])
print(f'x_min: {x_min}')
print(f'y_min: {y_min}')
print(f'x_max: {x_max}')
print(f'y_max: {y_max}')
