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
也可以使用asyncio的as_completed方法
"""


async def main():
    coroutine1 = do_some_work(1)
    coroutine2 = do_some_work(2)
    coroutine3 = do_some_work(4)

    tasks = [
        asyncio.ensure_future(coroutine1),
        asyncio.ensure_future(coroutine2),
        asyncio.ensure_future(coroutine3),
    ]
    for task in asyncio.as_completed(tasks):
        result = await task
        print('Task ret: {}'.format(result))


start = now()

loop = asyncio.get_event_loop()
done = loop.run_until_complete(main())
print('TIME: ', now() - start)

"""
由此可见，协程的调用和组合十分灵活，尤其是对于结果的处理，
如何返回，如何挂起，需要逐渐积累经验和前瞻的设计。
"""
