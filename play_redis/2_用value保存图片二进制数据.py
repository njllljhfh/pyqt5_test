# -*- coding:utf-8 -*-
from play_redis.redis_connection import redis_mg

"""
redis的key和values都是二进制安全的
"""

if __name__ == '__main__':
    print(redis_mg.conn.get("mykey"))
    redis_mg.conn.set("mykey", "hello world")

    img_source_path = "用value保存图片二进制数据.png"
    img_key = "myImage"
    # 用 value 保存图片二进制数据。
    with open(img_source_path, "rb") as f:
        context = f.read()
    res = redis_mg.conn.set(img_key, context)
    print(f"res={res}")

    # 从 value 中读取图像二进制数据。
    img_store_path = "./用value保存图片二进制数据-从redis读出来的图像.png"
    context = redis_mg.conn.get(img_key)
    with open(img_store_path, "wb") as f:
        f.write(context)

    # 这些操作是原子（atomic）性的，不会引起资源竞争。
    print(redis_mg.conn.incr("counter"))  # +1
    print(redis_mg.conn.incrby("counter", 100))  # +100
    print(redis_mg.conn.decr("counter"))  # -1
    print(redis_mg.conn.decrby("counter", 100))  # -100
