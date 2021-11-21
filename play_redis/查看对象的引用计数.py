# -*- coding:utf-8 -*-
from sys import getrefcount


class A(object):
    pass


if __name__ == '__main__':
    a = A()
    # b = a
    print(getrefcount(a))
