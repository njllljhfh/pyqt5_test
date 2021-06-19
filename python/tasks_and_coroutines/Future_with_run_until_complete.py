# -*- coding:utf-8 -*-

# 官网(https://docs.python.org/3.6/library/asyncio-task.html#example-future-with-run-until-complete)

# Example combining a Future and a coroutine function:
import asyncio


# The coroutine function is responsible for the computation (which takes 1 second) and
# it stores the result into the future.
# The `run_until_complete()` method waits for the completion of the future.
async def slow_operation(future):
    await asyncio.sleep(1)
    future.set_result('Future is done!')


loop = asyncio.get_event_loop()

future = asyncio.Future()
asyncio.ensure_future(slow_operation(future))

loop.run_until_complete(future)
print(future.result())
loop.close()
