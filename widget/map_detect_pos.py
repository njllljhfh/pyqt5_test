# -*- coding:utf-8 -*-
import math
import re


def map_pos(pos_origin, row, column, per=1):
    """"""

    res = column / per
    column_shown: int = math.ceil(res)  # 向上取整
    print(f"column_shown = {column_shown}")

    re_match = re.match(r"([a-zA-Z]*)(\d*)", pos_origin)

    row_name_origin = re_match.group(1)
    column_name_origin = re_match.group(2)
    print(f"row_name_origin = {row_name_origin}")
    print(f"column_name_origin = {column_name_origin}")

    map_row = {}


if __name__ == '__main__':
    map_pos("A40", 6, 80, per=1)
