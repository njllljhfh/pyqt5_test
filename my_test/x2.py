# -*- coding:utf-8 -*-
import copy
import time

import requests
import json
import hashlib

if __name__ == '__main__':
    x = lambda args, kwargs: f"串件复检任务 '{args[0]}' 迭代查询产品列表信息总耗时"

    args_ = [111, 222]
    kwargs_ = {"a": "a"}

    print(x(args_, kwargs_))


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

    # n = 10000000
    # t1 = time.time()
    # ls = [0 for i in range(n)]
    # t2 = time.time()
    #
    # ls2 = [0] * n
    # t3 = time.time()
    #
    # print(f"t2-t1={t2 - t1}")
    # print(f"t3-t2={t3 - t2}")

    # import  datetime
    # d_data = datetime.datetime.now()
    # print(d_data)
    # print(type(d_data))
    # print(int(d_data.strftime('%Y%m%d')))
    #
    # datetime_str='2021-07-20 14:55:53'
    # print(datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S'))

    source = ['https://www.cnblogs.com/royfans/p/14875565.html', 'https://www.cnblogs.com/royfans/p/14875565.html',
              "8a683566bcc7801226b3d8b0cf35fd97"]
    for url in source:
        res = hashlib.md5(url.encode(encoding='UTF-8')).hexdigest()
        print(res, type(res), len(res))


    def demo(sequence, k):
        return sequence[k:] + sequence[:k]


    a = '11110111'

    print(demo(a, -3))
