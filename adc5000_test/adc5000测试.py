# -*- coding:utf-8 -*-

from play_redis.redis_connection import redis_mg

"""
redis 的列表是用 链表(linked list)数据结构实现的，而不是用数组(array)。
"""

'''
redis 中 kye 的自动创建和删除(Automatic creation and removal of keys)

Basically we can summarize the behavior with three rules:
    1.When we add an element to an aggregate data type, if the target key does not exist, 
      an empty aggregate data type is created before adding the element.
    2.When we remove elements from an aggregate data type, if the value remains empty, 
      the key is automatically destroyed. The Stream data type is the only exception to this rule.
    3.Calling a read-only command such as LLEN (which returns the length of the list), 
      or a write command removing elements, with an empty key, always produces the same result 
      as if the key is holding an empty aggregate type of the type the command expects to find.
'''

task_id = 1314520
key_name = f'atq_{task_id}'  # auto task queue
redis_mg.conn.delete(key_name)
if __name__ == '__main__':
    redis_mg.conn.rpush(key_name, "A")
    print(redis_mg.conn.lrange(key_name, 0, -1))
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")
