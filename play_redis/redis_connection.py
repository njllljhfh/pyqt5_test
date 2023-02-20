# -*- coding:utf-8 -*-
import redis


class RedisManagement(object):
    """ redis 管理类 """

    def __init__(self, ip='127.0.0.1', port=6379, db=0):
        self._ip = ip
        self._port = port
        # self._pool = redis.ConnectionPool(host=ip, port=port, password='123')
        self._pool = redis.ConnectionPool(host=ip, port=port, db=db)
        self._conn = redis.Redis(connection_pool=self._pool)

    @property
    def conn(self):
        return self._conn


# redis_mg = RedisManagement(ip='10.0.1.110', port=6379)
redis_mg = RedisManagement(ip='10.0.2.20', port=6379, db=0)
