# -*- coding:utf-8 -*-
import time
import asyncio

now = lambda: time.time()

"""
通过 async 关键字定义一个协程（coroutine），协程也是一种对象。
协程不能直接运行，需要把协程加入到事件循环（loop），由后者在适当的时候调用协程。
asyncio.get_event_loop 方法可以创建一个事件循环，
然后使用 run_until_complete 将协程注册到事件循环，并启动事件循环。
"""


async def do_some_work(x):
    print('Waiting: ', x)


start = now()

coroutine = do_some_work(2)

loop = asyncio.get_event_loop()
loop.run_until_complete(coroutine)  # run_until_complete 方法是 阻塞 的

print('TIME: ', now() - start)
