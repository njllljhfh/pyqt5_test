# -*- coding:utf-8 -*-
import json

from play_redis.redis_connection import redis_mg

'''
You can find the full list of hash commands in the documentation. (https://redis.io/commands#hash)

It is worth noting that small hashes (i.e., a few elements with small values) 
are encoded in special way in memory that make them very memory efficient.
'''

if __name__ == '__main__':
    key_name = 'hash_njl'
    print(f"创建hash：")
    data = {
        'name': 'njl',
        'age': 18,
        'skill': json.dumps([1, 2, 3]),
    }
    redis_mg.conn.hset(key_name, mapping=data)
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")

    print(f"同过获取 hash 的 一个key 获取对应的value：")
    print(redis_mg.conn.hget(key_name, 'name'))
    print(redis_mg.conn.hget(key_name, 'skill'))
    print(redis_mg.conn.hgetall(key_name))
    print(type(redis_mg.conn.hgetall(key_name)))
    for k in redis_mg.conn.hgetall(key_name):
        string = k.decode('utf-8')
        print(string, type(string))
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")

    print(f"获取 hash 的多个 key 对应的 value：")
    key_ls = ['name', 'age', 'no-such-field']
    print(redis_mg.conn.hmget(key_name, key_ls))
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")
