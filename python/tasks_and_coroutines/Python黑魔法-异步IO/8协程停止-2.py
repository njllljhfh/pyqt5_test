# -*- coding:utf-8 -*-
import asyncio
import time

"""
上面见识了协程的几种常用的用法，都是协程围绕着事件循环进行的操作。future对象有几个状态：
- Pending
- Running
- Done
- Cancelled

创建future的时候，task为pending，事件循环调用执行的时候当然就是running，
调用完毕自然就是done，如果需要停止事件循环，就需要先把task取消。
可以使用asyncio.Task获取事件循环的task
"""

"""
启动事件循环之后，马上ctrl+c，会触发run_until_complete的执行异常 KeyBorardInterrupt。然后通过循环asyncio.Task取消future。
"""

now = lambda: time.time()


async def do_some_work(x):
    print('Waiting: ', x)

    await asyncio.sleep(x)
    return 'Done after {}s'.format(x)


"""
循环task，逐个cancel是一种方案，可是正如上面我们把task的列表封装在main函数中，main函数外进行事件循环的调用。
这个时候，main相当于最外出的一个task，那么处理包装的main函数即可。
"""


async def main():
    coroutine1 = do_some_work(1)
    coroutine2 = do_some_work(2)
    coroutine3 = do_some_work(2)

    tasks = [
        asyncio.ensure_future(coroutine1),
        asyncio.ensure_future(coroutine2),
        asyncio.ensure_future(coroutine3)
    ]
    done, pending = await asyncio.wait(tasks)
    for task in done:
        print('Task ret: ', task.result())


start = now()

loop = asyncio.get_event_loop()
task = asyncio.ensure_future(main())
try:
    loop.run_until_complete(task)
except KeyboardInterrupt as e:
    print(asyncio.Task.all_tasks())
    print()
    print(asyncio.gather(*asyncio.Task.all_tasks()).cancel())
    loop.stop()
    loop.run_forever()
finally:
    loop.close()
