# -*- coding:utf-8 -*-
import time
from multiprocessing import Process

from play_redis.redis_connection import RedisManagement

"""
redis 的列表是用 链表(linked list)数据结构实现的，而不是用数组(array)。
"""


class Producer(Process):
    def __init__(self, keys, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._redis_mg = None
        self._keys = keys

    def run(self) -> None:
        self._redis_mg = RedisManagement(ip='10.0.2.20', port=6379)
        self._redis_mg.conn.delete(*self._keys)
        s = 2
        ls_name = self._keys[0]
        print(f'[producer] {s}秒后，在redis列表 "{ls_name}" 的右边插入数据。')
        time.sleep(s)
        element = 1
        self._redis_mg.conn.rpush(ls_name, element)
        print(f'[producer] 已在redis列表 "{ls_name}" 的右边插入数据 {element}。')


class Consumer(Process):
    def __init__(self, keys, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._redis_mg = None
        self._keys = keys

    def run(self) -> None:
        self._redis_mg = RedisManagement(ip='10.0.2.20', port=6379)
        print(f'[consumer] 等待redis列表 "{self._keys}" 中的数据。')
        # 0 表示一直阻塞，直到获取到数据
        print(f'[consumer] 获取到的数据：{self._redis_mg.conn.brpop(self._keys, 0)}')


if __name__ == '__main__':
    # 列表的阻塞操作
    print(f"Blocking operations on lists")
    '''
    producer / consumer:
      ◆ To push items into the list, producers call LPUSH.
      ◆ To extract / process items from the list, consumers call RPOP.


    However it is possible that sometimes the list is empty and there is nothing to process, 
    so RPOP just returns NULL. In this case a consumer is forced to wait some time 
    and retry again with RPOP. This is called polling, 
    and is not a good idea in this context because it has several drawbacks:
        1.Forces Redis and clients to process useless commands (all the requests 
          when the list is empty will get no actual work done, they'll just return NULL).
        2.Adds a delay to the processing of items, since after a worker receives a NULL, it waits some time. 
          To make the delay smaller, we could wait less between calls to RPOP, 
          with the effect of amplifying problem number 1, i.e. more useless calls to Redis.


    A few things to note about BRPOP:
        1.Clients are served in an ordered way: 
            the first client that blocked waiting for a list, 
            is served first when an element is pushed by some other client, and so forth.
        2.The return value is different compared to RPOP: 
            it is a two-element array since it also includes the name of the key, 
            because BRPOP and BLPOP are able to block waiting for elements from multiple lists.
        3.If the timeout is reached, NULL is returned.
    '''
    key_name_1 = 'task1'
    key_name_2 = 'task2'
    key_ls = [key_name_1, key_name_2]

    p_producer = Producer(key_ls)
    p_consumer = Consumer(key_ls)

    p_producer.start()
    p_consumer.start()

    p_producer.join()
    p_consumer.join()

    print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")
