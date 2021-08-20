# -*- coding:utf-8 -*-
from play_redis.redis_connection import redis_mg

if __name__ == '__main__':
    # 这些操作是原子（atomic）性的，不会引起资源竞争。
    # incr, incrby, decr, decrby
    print(f"对整数型字符串的一些方便的操作：")
    key_name = "counter"
    redis_mg.conn.set(key_name, 100)  # 设置值为 100
    print(redis_mg.conn.incr(key_name))  # +1
    print(redis_mg.conn.incrby(key_name, 100))  # +100
    print(redis_mg.conn.decr(key_name))  # -1
    print(redis_mg.conn.decrby(key_name, 100))  # -100
    print("- " * 30)

    # getset
    print(f"应用举例: 每小时统计一次web的访问次数，并初始化下一小时的访问次数为0.")
    print(f"当前值为: {redis_mg.conn.getset(key_name, 0)}")
    print(f"重置值为: {redis_mg.conn.get(key_name)}")
    print("- " * 30)

    # mset and mget
    print(f"一条命令设置多个key-value，或取出多个key的对应的value列表")
    mset_data = {"a": 10, "b": 20, "c": 30}
    redis_mg.conn.mset(mset_data)
    print(redis_mg.conn.mget(list(mset_data.keys())))
    print("- " * 30)

    # exists, del, type
    key_name = "mykey"
    print(f'设置键 "{key_name}": {redis_mg.conn.set(key_name, "hello")}')
    print(f'删除前，是否存在键 "{key_name}"，返回值: {redis_mg.conn.exists(key_name)}')
    print(f'删除键 "{key_name}"，返回值: {redis_mg.conn.delete(key_name)}')
    print(f'删除后，是否存在键 "{key_name}"，返回值: {redis_mg.conn.exists(key_name)}')
    # - - -
    print(f'获取键 "{key_name}" 的对应的值类型：{redis_mg.conn.type(key_name)}')
    redis_mg.conn.set(key_name, "hello")
    print(f'获取键 "{key_name}" 的对应的值类型：{redis_mg.conn.type(key_name)}')
    print("- " * 30)

    #
