# -*- coding:utf-8 -*-
# import time
#
#
# def gen():
#     value = 0
#     while True:
#         receive = yield value
#         if receive == 'e':
#             break
#         value = 'got: %s' % receive
#
#
# g = gen()
# print(g.send(None))
# time.sleep(.5)
#
# print(g.send('hello'))
# time.sleep(.5)
#
# print(g.send(123456))
# time.sleep(.5)
#
# print(g.send('e'))

# # - - - - - -

# def g1():
#     yield range(5)
#
#
# def g2():
#     yield from range(5)
#
#
# it1 = g1()
# it2 = g2()
# for x in it1:
#     print(x)
#
# for x in it2:
#     print(x)

# # - - - - - -

def fab(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        # print b
        a, b = b, a + b
        n = n + 1


f = fab(5)


# def f_wrapper(fun_iterable):
#     print('start')
#     for item in fun_iterable:
#         yield item
#     print('\nend')
#
#
# wrap = f_wrapper(fab(5))
# for i in wrap:
#     print(i, end=' ')


# 现在使用yield from代替for循环
def f_wrapper2(fun_iterable):
    print('start')
    yield from fun_iterable  # 再强调一遍：yield from后面必须跟iterable对象(可以是生成器，迭代器)
    print('\nend')


wrap = f_wrapper2(fab(5))
for i in wrap:
    print(i, end=' ')
