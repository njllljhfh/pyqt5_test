# -*- coding:utf-8 -*-


if __name__ == '__main__':
    x = lambda args, kwargs: f"串件复检任务 '{args[0]}' 迭代查询产品列表信息总耗时"

    args_ = [111, 222]
    kwargs_ = {"a": "a"}

    print(x(args_, kwargs_))
