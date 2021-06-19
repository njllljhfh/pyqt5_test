# -*- coding:utf-8 -*-

# 官网(https://docs.python.org/3.6/library/asyncio-task.html#example-chain-coroutines)

# Example chaining coroutines:

import asyncio


async def compute(x, y):
    print("Compute %s + %s ..." % (x, y))
    await asyncio.sleep(4.0)
    return x + y


async def print_sum(x, y):
    result = await compute(x, y)
    print("%s + %s = %s" % (x, y, result))


loop = asyncio.get_event_loop()
loop.run_until_complete(print_sum(1, 2))
loop.close()
