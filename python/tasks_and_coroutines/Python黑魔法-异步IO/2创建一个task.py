# -*- coding:utf-8 -*-
import asyncio
import time

now = lambda: time.time()

"""
协程对象不能直接运行，在注册事件循环的时候，
其实是 run_until_complete 方法将协程包装成为了一个任务（task）对象。
所谓 task 对象是 Future 类的子类。保存了协程运行后的状态，用于未来获取协程的结果。
"""


async def do_some_work(x):
    print('Waiting: ', x)


start = now()

coroutine = do_some_work(2)
loop = asyncio.get_event_loop()

# task = asyncio.ensure_future(coroutine)
task = loop.create_task(coroutine)  # 创建 task 后，task 在加入事件循环之前是 pending 状态
print(task)
print(f"task 的类型是 asyncio.Future: {isinstance(task, asyncio.Future)}")
print("---------------------------------------------")
loop.run_until_complete(task)
print(task)  # 因为 do_some_work 中没有耗时的阻塞操作，task 很快就执行完毕了。此处打印的 finished 状态。

print('TIME: ', now() - start)

"""
创建 task 后，task 在加入事件循环之前是 pending 状态，
因为 do_some_work 中没有耗时的阻塞操作，task 很快就执行完毕了。
后面打印的 finished 状态。

asyncio.ensure_future(coroutine) 和 loop.create_task(coroutine) 都可以创建一个task，
run_until_complete 的参数是一个 future 对象。
当传入一个协程，其内部会自动封装成task，task是Future的子类。
isinstance(task, asyncio.Future) 将会输出 True。
"""
