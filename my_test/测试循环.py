# -*- coding:utf-8 -*-

class Asd(object):
    def __init__(self):
        print(f"__init__")

    def __iter__(self):
        print(f"__iter__")
        # return iter(range(10))
        return (x for x in range(10))


if __name__ == '__main__':

    for i in Asd():
        a = 1
        print(i)
