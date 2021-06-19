# -*- coding:utf-8 -*-
import asyncio


# 官网(https://docs.python.org/3.6/library/asyncio-task.html#example-hello-world-coroutine)

# Example of coroutine displaying "Hello World":
async def hello_world():
    print("Hello World!")


loop = asyncio.get_event_loop()
# Blocking call which returns when the hello_world() coroutine is done
loop.run_until_complete(hello_world())
loop.close()
