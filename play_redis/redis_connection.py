# -*- coding:utf-8 -*-
import redis


class RedisManagement(object):
    """ redis 管理类 """

    def __init__(self, ip='127.0.0.1', port=6379):
        self._ip = ip
        self._port = port
        self._pool = redis.ConnectionPool(host=ip, port=port)
        self._conn = redis.Redis(connection_pool=self._pool)

    @property
    def conn(self):
        return self._conn


redis_mg = RedisManagement()
