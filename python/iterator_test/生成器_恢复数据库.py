# -*- coding:utf-8 -*-
# 补充：
# 日常工作中使用generator处理大文件是比较常见的场景，因为可以不用一次性读取整个文件，使用generator也可以极大的减少代码量。
# 这里贴一个某次使用generator进行基于mysql binlog恢复的脚本，使用此脚本读取一个300多G的flashback sql文件，占用极小的内存完成了恢复：

import pymysql
import sys
import os
import time

file = sys.argv[1]
mysql_conn = pymysql.connect(host="xxx", port=3306, user="leo", passwd="xxx", db="xxx", charset='utf8')


def get_sql_batch(open_file, batch_size, file_size):
    cur_pos = 0
    open_file.seek(0, os.SEEK_SET)
    while cur_pos < file_size:
        sql_batch = []
        for i in range(batch_size):
            sql_line = open_file.readline()
            if 'xxx' in sql_line:
                sql_batch.append(sql_line)
        cur_pos = f.tell()
        # cur_pos = open_file.tell()
        yield sql_batch, cur_pos


f = open(file)
f.seek(0, os.SEEK_END)
filesize = f.tell()
f.seek(0, os.SEEK_SET)
with mysql_conn.cursor() as cur:
    for batch, pos in get_sql_batch(f, 1000, filesize):
        for sql in batch:
            cur.execute(sql)
        mysql_conn.commit()
        print('%s: Current pos: %s,Current percent: %.2f%%' % (time.ctime(), pos, pos * 100 / filesize))
f.close()
