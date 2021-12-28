# -*- coding:utf-8 -*-
import asyncio
import time
from threading import Thread

"""
很多时候，我们的事件循环用于注册协程，而有的协程需要动态的添加到事件循环中。
一个简单的方式就是使用多线程。在当前线程创建一个事件循环，然后在新建一个线程，在新建的线程中启动事件循环。当前线程不会被block。
"""
now = lambda: time.time()


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def more_work(x):
    print('More work {}'.format(x))
    time.sleep(x)
    print('Finished more work {}'.format(x))


start = now()
new_loop = asyncio.new_event_loop()
t = Thread(target=start_loop, args=(new_loop,))
t.start()
print('主线程-TIME: {}'.format(time.time() - start))

# 两次调用 call_soon_threadsafe 是同步执行的，即执行完第一次call_soon_threadsafe之后才会执行第二次call_soon_threadsafe。
new_loop.call_soon_threadsafe(more_work, 6)  # 不阻塞主线程
new_loop.call_soon_threadsafe(more_work, 3)  # 不阻塞主线程

print('主线程-x')


"""
启动上述代码之后，当前线程不会被block，新线程中会按照顺序执行call_soon_threadsafe方法注册的more_work方法，
后者因为time.sleep操作是同步阻塞的，因此运行完毕more_work需要大致6 + 3
"""
