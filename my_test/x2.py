# -*- coding:utf-8 -*-
import copy
import time

import requests
import json


class A(object):
    pass


if __name__ == '__main__':
    # res = requests.head("https://www.baidu.com")
    # print(res.headers)
    # print(res.status_code)
    #
    # max()
    # ---

    # a = [(A(), A()), 3]
    # print(f"id(a[0])={id(a[0])}, id(a[1])={id(a[1])}, id(a[0][0])={id(a[0][0])}")
    # b = copy.deepcopy(a)
    # print(f"id(b[0])={id(b[0])}, id(b[1])={id(b[1])}, id(b[0][0])={id(b[0][0])}")
    #
    # print(copy.__doc__)
    # ---

    # ls = [i for i in range(10000000)]
    #
    # t1 = time.time()
    # print(ls.index(5))
    # t2 = time.time()
    #
    # print(ls.index(9999995))
    # t3 = time.time()
    #
    # print(f"t2-t1={t2 - t1}")
    # print(f"t3-t2={t3 - t2}")
    # ---

    n = 10000000
    t1 = time.time()
    ls = [0 for i in range(n)]
    t2 = time.time()

    ls2 = [0] * n
    t3 = time.time()

    print(f"t2-t1={t2 - t1}")
    print(f"t3-t2={t3 - t2}")
