# -*- coding:utf-8 -*-
import asyncio

# 官网(https://docs.python.org/3.6/library/asyncio-task.html#example-future-with-run-forever)

# In this example,
# the future is used to link `slow_operation()` to `got_result()`:
# when `slow_operation()` is done, `got_result()` is called with the result.
from asyncio import Task


async def slow_operation(future):
    await asyncio.sleep(1)
    future.set_result('Future is done!')


def got_result(future):
    print(future.result())
    loop.stop()


loop = asyncio.get_event_loop()
future = asyncio.Future()

# 官网(https://docs.python.org/3.6/library/asyncio-task.html#asyncio.ensure_future)
asyncio.ensure_future(slow_operation(future))
future.add_done_callback(got_result)

try:
    loop.run_forever()
finally:
    loop.close()
