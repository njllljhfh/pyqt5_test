# -*- coding:utf-8 -*-
from play_redis.redis_connection import redis_mg

'''
Redis Sets are unordered collections of strings. 
'''

if __name__ == '__main__':
    key_name = 'set_njl'

    print(f"创建一个集合：")
    values = {1, 2, 3}
    redis_mg.conn.sadd(key_name, *values)
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")

    print(f'查看集合中的全部元素：')
    print(redis_mg.conn.smembers(key_name))
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")

    print(f'判断给定的元素是否在集合中：')
    print(redis_mg.conn.sismember(key_name, 1))
    print(redis_mg.conn.sismember(key_name, 30))
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")

    print(f"求多个集合的交集：")
    k1, k2, k3, k4 = 'tag:1:news', 'tag:2:news', 'tag:3:news', 'tag:4:news'
    redis_mg.conn.delete(*[k1, k2, k3, k4])
    redis_mg.conn.sadd(k1, 1000, 2000)
    redis_mg.conn.sadd(k2, 2000, 3000)
    redis_mg.conn.sadd(k3, 3000)
    redis_mg.conn.sadd(k4, 4000)
    print(redis_mg.conn.sinter([k1, k2]))
    print(redis_mg.conn.sinter([k1, k2, k3]))
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")

    '''
    In addition to intersection you can also perform unions, difference, extract a random element, and so forth.
    除了求多个集合的交集，还可以求并集、差集、随机从集合中抽取元素等等。
    '''
    # 52张扑克牌(Imagine we use a one-char prefix for (C)lubs, (D)iamonds, (H)earts, (S)pades:)
    deck = 'deck'
    redis_mg.conn.delete(deck)
    poker_ls = [
        'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'CJ', 'CQ', 'CK',
        'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'DJ', 'DQ', 'DK',
        'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'HJ', 'HQ', 'HK',
        'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'SJ', 'SQ', 'SK',
    ]
    redis_mg.conn.sadd(deck, *poker_ls)

    print(f'为每次游戏，复制一幅纸牌：')
    key_name = 'game:1:deck'
    redis_mg.conn.sunionstore(key_name, [deck, ])  # sunionstore 求多个结合的并集，并保存到一个新的集合。
    print(f'集合"{key_name}"中元素的个数：{redis_mg.conn.scard(key_name)}')

    num = 5
    print(f'从集合"{key_name}"中随机抽取{num}个元素：{redis_mg.conn.spop(key_name, num)}')
    print(f'集合"{key_name}"中元素的个数：{redis_mg.conn.scard(key_name)}')
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")
