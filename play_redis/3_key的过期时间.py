# -*- coding:utf-8 -*-
import time

from play_redis.redis_connection import redis_mg

"""
关于过期的信息被复制并保存在磁盘上，即使你的Redis服务器保持停止服务的状态，
时间实际上也是流逝的（这意味着 Redis 保存了一个key的过期日期）。
"""

key_name = "x"
print(f"先设置 key 的值，再设置该 key 的超时时间（s）")
redis_mg.conn.set(key_name, 111)
redis_mg.conn.expire(key_name, 10)  # 设置过期时间（s）
time.sleep(1)
print(redis_mg.conn.ttl(key_name))  # 查看过期剩余时间（s）
print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")

print(f"先设置 key 的值，再设置该 key 的超时时间（ms）")
redis_mg.conn.pexpire(key_name, 3000)  # 设置过期时间（ms）
time.sleep(1)
print(redis_mg.conn.pttl(key_name))  # 查看过期剩余时间（ms）
print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")

print(f"设置 key 的值，同时设置该 key 的超时时间（s）")
redis_mg.conn.set(key_name, 111, ex=20)
time.sleep(1)
print(f"剩余超时时间：{redis_mg.conn.ttl(key_name)}")

print(f"重新设置 key 的值，并保持超时时间不变")
redis_mg.conn.set(key_name, 222, keepttl=True)
time.sleep(1)
print(f"剩余超时时间：{redis_mg.conn.ttl(key_name)}")
print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")
