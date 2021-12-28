# -*- coding:utf-8 -*-
import asyncio

import time

"""
使用async可以定义协程，协程用于耗时的io操作，
我们也可以封装更多的io操作过程，这样就实现了嵌套的协程，
即一个协程中await了另外一个协程，如此连接起来。
"""

now = lambda: time.time()


async def do_some_work(x):
    print('Waiting: ', x)

    await asyncio.sleep(x)
    return 'Done after {}s'.format(x)


"""
不在 main 协程函数里处理结果，直接返回 await 的内容，
那么最外层的 run_until_complete 将会返回 main 协程的结果。
或者返回使用 asyncio.wait 方式挂起协程。
"""


async def main():
    coroutine1 = do_some_work(1)
    coroutine2 = do_some_work(2)
    coroutine3 = do_some_work(4)

    tasks = [
        asyncio.ensure_future(coroutine1),
        asyncio.ensure_future(coroutine2),
        asyncio.ensure_future(coroutine3)
    ]

    return await asyncio.wait(tasks)


start = now()

loop = asyncio.get_event_loop()
dones, pendings = loop.run_until_complete(main())

print(f'pendings = {pendings}')

for task in dones:
    print('Task ret: ', task.result())
