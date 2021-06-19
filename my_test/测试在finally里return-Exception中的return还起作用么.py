# -*- coding:utf-8 -*-

'''
测试在finally里return-Exception中的return还起作用么
'''


def stop():
    """ 停止任务 """
    # TODO-NJL:mlk代码
    try:
        a = 1/0
        return 'ok'
    except Exception as e:
        print(e)
        return 'Exception'
    finally:
        return 'finally'


if __name__ == '__main__':
    res = stop()
    print(res)
