# -*- coding:utf-8 -*-
import functools
import time
import asyncio

"""
绑定回调，在 task 执行完毕的时候可以获取执行的结果，
回调的`最后一个参数`是 future 对象，通过该对象可以获取协程返回值。
如果回调需要多个参数，可以通过偏函数导入。
"""
now = lambda: time.time()


async def do_some_work(x):
    print('Waiting: ', x)
    return 'Done after {}s'.format(x)


def callback(future):
    print('Callback: ', future.result())


def callback2(t, future):
    print('Callback2:', t, future.result())


start = now()

coroutine = do_some_work(11)
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(coroutine)
task.add_done_callback(callback)
task.add_done_callback(functools.partial(callback2, 3))
loop.run_until_complete(task)

print('TIME: ', now() - start)

"""
可以看到，coroutine 执行结束时候会调用回调函数。
并通过参数 future 获取协程执行的结果。
我们创建的 task 和回调里的 future 对象，实际上是同一个对象。
"""
