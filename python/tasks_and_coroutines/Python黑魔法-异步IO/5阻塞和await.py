# -*- coding:utf-8 -*-
import asyncio
import time

"""
使用 async 可以定义协程对象，使用 await 可以针对耗时的操作进行挂起，就像生成器里的 yield 一样，
函数让出控制权。协程遇到 await，事件循环将会挂起该协程，执行别的协程，
直到其他的协程也挂起或者执行完毕，再进行下一个协程的执行。

耗时的操作一般是一些 IO 操作，例如网络请求，文件读取等。
我们使用 asyncio.sleep 函数来模拟 IO 操作。协程的目的也是让这些 IO 操作异步化。
"""

now = lambda: time.time()


async def do_some_work(x):
    print('Waiting: ', x)
    await asyncio.sleep(x)
    return 'Done after {}s'.format(x)


start = now()

coroutine = do_some_work(2)
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(coroutine)
loop.run_until_complete(task)

print('Task ret: ', task.result())
print('TIME: ', now() - start)

"""
在 sleep的时候，使用await让出控制权。
即当遇到阻塞调用的函数的时候，
使用await方法将协程的控制权让出，以便loop调用其他的协程。
现在我们的例子就用耗时的阻塞操作了。
"""