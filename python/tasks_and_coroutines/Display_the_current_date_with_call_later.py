# -*- coding:utf-8 -*-

# 官网(https://docs.python.org/3.6/library/asyncio-eventloop.html#display-the-current-date-with-call-later)

# Example of callback displaying the current date every second.
# The callback uses the `AbstractEventLoop.call_later()` method
# to reschedule itself during 5 seconds, and then stops the event loop:
import asyncio
import datetime


def display_date(end_time, loop):
    print(datetime.datetime.now())
    if (loop.time() + 1.0) < end_time:
        # 官网(https://docs.python.org/3.6/library/asyncio-eventloop.html#asyncio.AbstractEventLoop.call_later)
        loop.call_later(1, display_date, end_time, loop)
    else:
        loop.stop()


loop = asyncio.get_event_loop()

# Schedule the first call to display_date()
end_time = loop.time() + 5.0
loop.call_soon(display_date, end_time, loop)

# Blocking call interrupted by loop.stop()
loop.run_forever()
loop.close()
