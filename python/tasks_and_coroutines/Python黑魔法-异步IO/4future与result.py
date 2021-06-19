# -*- coding:utf-8 -*-
import time
import asyncio

"""
回调一直是很多异步编程的恶梦，
程序员更喜欢使用同步的编写方式写异步代码，以避免回调的恶梦。
回调中我们使用了 future 对象的 result 方法。
前面不绑定回调的例子中，我们可以看到 task 有 finished 状态。在那个时候，可以直接读取 task 的 result 方法。
"""
now = lambda: time.time()


async def do_some_work(x):
    print('Waiting {}'.format(x))
    return 'Done after {}s'.format(x)


start = now()

coroutine = do_some_work(2)
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(coroutine)
loop.run_until_complete(task)

print('Task ret: {}'.format(task.result()))
print('TIME: {}'.format(now() - start))
