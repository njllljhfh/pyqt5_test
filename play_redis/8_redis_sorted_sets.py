# -*- coding:utf-8 -*-
from play_redis.redis_connection import redis_mg

'''
Sorted sets are a data type which is similar to a mix between a Set and a Hash. 
Like sets, sorted sets are composed of unique, non-repeating string elements, 
so in some sense a sorted set is a set as well.

score is a floating point value.

They are ordered according to the following rule:
1.If A and B are two elements with a different score, then A > B if A.score is > B.score.
2.If A and B have exactly the same score, then A > B if the A string is lexicographically greater than the B string. 
  A and B strings can't be equal since sorted sets only have unique elements.


Implementation note: 
  Sorted sets are implemented via a dual-ported data structure containing both a skip list and a hash table, 
  so every time we add an element Redis performs an O(log(N)) operation. 
  That's good, but when we ask for sorted elements Redis does not have to do any work at all, it's already all sorted.
'''

if __name__ == '__main__':
    hackers = 'hackers'

    print(f"创建有序集合，元素为人名，score为生日年份：")
    elements = {
        "Alan Kay": 1940,
        "Sophie Wilson": 1957,
        "Richard Stallman": 1953,
        "Anita Borg": 1949,
        "Yukihiro Matsumoto": 1965,
        "Hedy Lamarr": 1914,
        "Claude Shannon": 1916,
        "Linus Torvalds": 1969,
        "Alan Turing": 1912,
    }
    length = len(elements)
    redis_mg.conn.zadd(hackers, elements)
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")

    print(f"从有序集合中读取全部元素（score升序）：")
    print(redis_mg.conn.zrange(hackers, 0, -1))
    print(redis_mg.conn.zrange(hackers, 0, -1, withscores=True))
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - -")

    print(f"从有序集合中读取全部元素（score降序）：")
    print(redis_mg.conn.zrevrange(hackers, 0, -1))
    print(redis_mg.conn.zrevrange(hackers, 0, -1, withscores=True))
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - -\n")

    print(f"================== Operating on ranges ==================")
    print(f'获取出生年份小于等于1950年的黑客：')
    print(redis_mg.conn.zrangebyscore(hackers, '-inf', 1950, withscores=True))
    print('- - -')
    print(f'从有序集合中移除出生年份在1940-1960之间的黑客：')
    print(f'移除前集合中的元素个数：{redis_mg.conn.zcard(hackers)}')
    redis_mg.conn.zremrangebyscore(hackers, 1940, 1960)
    print(f'移除后集合中的元素个数：{redis_mg.conn.zcard(hackers)}')
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - -\n")

    print(f"================== Lexicographical scores ==================")
    '''
    The main commands to operate with lexicographical ranges are 
    ZRANGEBYLEX, ZREVRANGEBYLEX, ZREMRANGEBYLEX and ZLEXCOUNT.
    '''
    hackers = 'hackers2'
    elements = {
        "Alan Kay": 0,
        "Sophie Wilson": 0,
        "Richard Stallman": 0,
        "Anita Borg": 0,
        "Yukihiro Matsumoto": 0,
        "Hedy Lamarr": 0,
        "Claude Shannon": 0,
        "Linus Torvalds": 0,
        "Alan Turing": 0,
    }
    redis_mg.conn.zadd(hackers, elements)
    print(f"从有序集合中读取全部元素（Lexicographical score升序）：")
    print(redis_mg.conn.zrange(hackers, 0, -1))  # 见上述的，有序集合的排序规则2
    print('- - -')

    print(f"使用ZRANGEBYLEX，来从集合中获取一个字典序范围内的元素：")
    print(redis_mg.conn.zlexcount(hackers, '[B', '[P'))  # 在该字典序范围内的元素的个数
    print(redis_mg.conn.zrangebylex(hackers, '[B', '[P'))

    print(f"================== Updating the score: leader boards (更新分数:排行榜) ==================")
    '''
    Sorted sets' scores can be updated at any time. 
    Just calling ZADD against an element already included in the sorted set 
    will update its score (and position) with O(log(N)) time complexity. 
    As such, sorted sets are suitable when there are tons of updates.
    
    # 应用场景举例：
    Because of this characteristic a common use case is leader boards. 
    The typical application is a Facebook game 
    where you combine the ability to take users sorted by their high score, 
    plus the get-rank operation, 
    in order to show the top-N users, and the user rank in the leader board (e.g., "you are the #4932 best score here").
    '''
