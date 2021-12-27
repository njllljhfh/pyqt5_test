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

key_name = "my_ls"
redis_mg.conn.delete(key_name)
if __name__ == '__main__':
    redis_mg.conn.rpush(key_name, "A")
    print(redis_mg.conn.lrange(key_name, 0, -1))
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")

    redis_mg.conn.rpush(key_name, "B")
    print(redis_mg.conn.lrange(key_name, 0, -1))
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")

    redis_mg.conn.lpush(key_name, "first")
    print(redis_mg.conn.lrange(key_name, 0, -1))
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")

    # 一次添加多个元素
    redis_mg.conn.delete(key_name)
    redis_mg.conn.rpush(key_name, *[1, 2, 3])
    print(redis_mg.conn.lrange(key_name, 0, -1))
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")

    print(redis_mg.conn.rpop(key_name))
    print(redis_mg.conn.lpop(key_name))
    print(redis_mg.conn.rpop(key_name))
    print(redis_mg.conn.rpop(key_name))  # 列表为空时，返回 nil
    redis_mg.conn.delete(key_name)
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")

    print(f"Capped lists")
    # The LTRIM command is similar to LRANGE,
    # but instead of displaying the specified range of elements
    # it sets this range as the new list value.
    # All the elements outside the given range are removed.

    # Note: while LRANGE is technically an O(N) command,
    # accessing small ranges towards the head or the tail of the list is a constant time operation.
    redis_mg.conn.rpush(key_name, *[1, 2, 3, 4, 5])
    print(redis_mg.conn.lrange(key_name, 0, -1))

    redis_mg.conn.ltrim(key_name, 0, 2)
    print(redis_mg.conn.lrange(key_name, 0, -1))
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")
