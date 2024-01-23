# -*- coding:utf-8 -*-
import time

import requests

url = 'https://www.example.com'
now = lambda: time.time()


def fetch(url):
    # 发送 GET 请求
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 获取响应内容
        content = response.text
        # print(content)
        return content
    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")


if __name__ == '__main__':
    urls = [
        'https://www.example.com',
        'https://www.example.org',
        'https://www.example.net',
    ]

    start = now()

    for url in urls:
        print(f"Response from {url}: {len(fetch(url))} bytes")

    print('TIME: ', now() - start)
