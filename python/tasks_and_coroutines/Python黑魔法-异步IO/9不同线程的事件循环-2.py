import asyncio
import time
import threading


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()
    print("线程结束了。。。。。")


async def more_work(x):
    print('More work {}'.format(x))
    await asyncio.sleep(x)
    print('Finished more work {}'.format(x))
    return x


async def stop_loop(loop, stop_event):
    # 等待设置停止事件
    print(555555555)
    res = await asyncio.get_event_loop().run_in_executor(None, stop_event.wait)
    print(f"res = {res}")
    asyncio.gather(*asyncio.all_tasks()).cancel()
    # for task in asyncio.all_tasks():
    #     print(task.cancel())
    print(6666666666)
    loop.stop()
    print(7777777777)


start = time.time()
new_loop = asyncio.new_event_loop()
stop_event = threading.Event()  # 用于通知事件循环停止的事件

t = threading.Thread(target=start_loop, args=(new_loop,))
# t.daemon = True  # 主线程不等待 daemon 为 True 的子线程执行结束
t.start()
print('主线程-TIME: {}'.format(time.time() - start))

# 使用 asyncio.run_coroutine_threadsafe 来运行异步任务
task1 = asyncio.run_coroutine_threadsafe(more_work(6), new_loop)
task2 = asyncio.run_coroutine_threadsafe(more_work(3), new_loop)

# 启动一个协程来停止事件循环
asyncio.run_coroutine_threadsafe(stop_loop(new_loop, stop_event), new_loop)

# 主线程等待线程结束
time.sleep(4)
print(111)
stop_event.set()
print(222)
# t.join()

print(333)

# 获取异步任务的结果，如果任务没有执行完，会阻塞
# result1 = task1.result()
# result2 = task2.result()
# print(f"result1 = {result1}")
# print(f"result2 = {result2}")

print('主线程-x')
