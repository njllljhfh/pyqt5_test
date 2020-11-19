# -*- coding:utf-8 -*-
from collections import Iterator, Iterable, Generator

if __name__ == '__main__':

    # # 先看一个iterale对象
    # a = ['ShanXi', 'HuNan', 'HuBei', 'XinJiang', 'JiangSu', 'XiZang', 'HeNan', 'HeBei']
    # b = isinstance(a, Iterator), isinstance(a, Iterable), isinstance(a, Generator)
    # print(f"b = {b}")
    # # 可以看到这是一个可迭代对象但并不是迭代器，我们把它搞成一个迭代器试试看：
    # print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    #
    #
    # def generator_list(a):
    #     for e in a:
    #         yield 'Province:\t' + e
    #
    #
    # x = generator_list(a)
    # b = isinstance(x, Iterator), isinstance(x, Iterable), isinstance(x, Generator)
    # print(f"b = {b}")
    #
    # for province in x:
    #     print(province)
    # print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    #
    #
    # class iterator_list(object):
    #     def __init__(self, a):
    #         self.a = a
    #         self.len = len(self.a)
    #         self.cur_pos = -1
    #
    #     def __iter__(self):
    #         return self
    #
    #     def __next__(self):  # Python3中只能使用__next__()而Python2中只能命名为next()
    #         self.cur_pos += 1
    #         if self.cur_pos < self.len:
    #             return self.a[self.cur_pos]
    #         else:
    #             raise StopIteration()  # 表示至此停止迭代
    #
    #
    # x = iterator_list(a)
    # b = isinstance(x, Iterator), isinstance(x, Iterable), isinstance(x, Generator)
    # print(f"b = {b}")
    # # iterator当然是iterable，因为其本身含有__iter__方法。
    #
    # for province in x:
    #     print(province)
    # print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    #
    # # 简便起见这里只写python2的代码，想要在python3中运行将print修改下再把next()改名为__next__即可。
    # list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    #
    #
    # class iter_standard(object):
    #     """正序迭代"""
    #
    #     def __init__(self, list):
    #         self.list = list
    #         self.len = len(self.list)
    #         self.cur_pos = -1
    #
    #     def __iter__(self):
    #         return self
    #
    #     def __next__(self):
    #         self.cur_pos += 1
    #         if self.cur_pos < self.len:
    #             return self.list[self.cur_pos]
    #         else:
    #             raise StopIteration()
    #
    #
    # class iter_reverse(object):
    #     """逆序迭代"""
    #
    #     def __init__(self, list):
    #         self.list = list
    #         self.len = len(self.list)
    #         self.cur_pos = self.len
    #
    #     def __iter__(self):
    #         return self
    #
    #     def __next__(self):
    #         self.cur_pos -= 1
    #         if self.cur_pos >= 0:
    #             return self.list[self.cur_pos]
    #         else:
    #             raise StopIteration()
    #
    #
    # for e in iter_standard(list):
    #     print(e)
    # print("* " * 10)
    # for e in iter_reverse(list):
    #     print(e)
    #
    # print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    import time


    class BinLogStreamReader(object):
        def __init__(self):
            self.counter = 0

        def fetchone(self):
            while True:
                if self.counter < 10:
                    time.sleep(0.5)
                    j = self.counter
                    self.counter += 1
                    return j

        def __iter__(self):
            return iter(self.fetchone, 6)  # 当self.fetchone返回6时，抛出 StopIteration 异常。


    x = BinLogStreamReader()
    b = isinstance(x, Iterator), isinstance(x, Iterable), isinstance(x, Generator)
    print(f"b = {b}")
    for item in x:
        print(f"item = {item}")
    """
    因此这里可以对iterable对象做一个有别于文章开头的解释，
    非iterator的iterable对象其标志不仅仅是含有__iter__方法，
    他的__iter__方法还返回了一个迭代器对象（例如示例三中的iter(self.list)），
    但因为其本身不含__next__方法所以其可for循环但并不是iterator。
    """
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
