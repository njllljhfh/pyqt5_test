# -*- coding:utf-8 -*-

# 官网(https://docs.python.org/3.6/library/asyncio-task.html#example-coroutine-displaying-the-current-date)

# Example of coroutine displaying the current date
# every second during 5 seconds using the sleep() function:


import asyncio
import datetime


async def display_date(loop):
    end_time = loop.time() + 5.0
    while True:
        print(datetime.datetime.now())
        if (loop.time() + 1.0) >= end_time:
            break
        await asyncio.sleep(1)


loop = asyncio.get_event_loop()
# Blocking call which returns when the display_date() coroutine is done
loop.run_until_complete(display_date(loop))
loop.close()
