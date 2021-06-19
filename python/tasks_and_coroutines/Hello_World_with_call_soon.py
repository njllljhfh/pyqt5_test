# -*- coding:utf-8 -*-

# 官网(https://docs.python.org/3.6/library/asyncio-eventloop.html#hello-world-with-call-soon)

# Example using the `AbstractEventLoop.call_soon()` method to schedule a callback.
# The callback displays "Hello World" and then stops the event loop:
import asyncio


# njl: Note that this is not coroutine. It's just a ordinary function.
def hello_world(loop, i: int, is_last: bool = False):
    print(f'Hello World {i}')
    if is_last:
        loop.stop()


loop = asyncio.get_event_loop()

# Schedule a call to hello_world()
# 官网(https://docs.python.org/3.6/library/asyncio-eventloop.html#asyncio.AbstractEventLoop.call_soon)
loop.call_soon(hello_world, loop, 1)
loop.call_soon(hello_world, loop, 2, True)

# Blocking call interrupted by loop.stop()
loop.run_forever()
loop.close()
