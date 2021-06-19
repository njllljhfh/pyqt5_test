# -*- coding:utf-8 -*-

# Fist implement.
def createCounter():
    def counter(x):
        # return next(o)
        return g.send(x)

    def generator():
        i = 0
        j = 0
        while True:
            i = i + j
            j = yield i

    g = generator()
    next(g)  # 激活
    return counter


# Second implement.
# def createCounter():
#     count = 0
#
#     def counter(x):
#         nonlocal count
#         count += x
#         return count
#
#     return counter


if __name__ == '__main__':
    c = createCounter()
    f = createCounter()
    for i in range(1, 11):
        print("c=", c(i))
        print("f=", f(i * 2))
