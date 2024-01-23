# -*- coding:utf-8 -*-
import asyncio
import time

import aiohttp

now = lambda: time.time()


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def main():
    urls = [
        'https://www.example.com',
        'https://www.example.org',
        'https://www.example.net',
    ]

    tasks = [fetch(url) for url in urls]

    # 等待所有异步任务完成
    responses = await asyncio.gather(*tasks)

    # 处理异步请求的结果
    for url, response in zip(urls, responses):
        print(f"Response from {url}: {len(response)} bytes")


if __name__ == "__main__":
    # 运行主协程
    # asyncio.run(main())

    start = now()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    print('TIME: ', now() - start)
