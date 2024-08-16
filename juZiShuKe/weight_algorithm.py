# -*- coding:utf-8 -*-
from pprint import pprint


# def weightCombinations(m: int, cur_combination: list, remaining_sum: float, count: int = 10):
#     """
#     权重组合生成器
#     :param m: 每个权重组合中，权重的个数
#     :param cur_combination: 权重组合
#     :param remaining_sum: 当前组合中，剩余可分配的权重最大值
#     :param count: count * 权重增量 = 1
#     :return:
#     """
#     if len(cur_combination) == m:
#         if round(remaining_sum, 2) <= 0:
#             yield tuple(cur_combination)
#         return
#
#     for i in range(1, count):
#         next_value = round(i / count, 2)
#         if next_value <= round(remaining_sum, 2):
#             yield from weightCombinations(m, cur_combination + [next_value], remaining_sum - next_value, count=count)
#         else:
#             break


def weightCombinations(m: int, count: int = 10):
    """
    权重组合生成器 (非递归版本)
    :param m: 每个权重组合中，权重的个数
    :param count: count * 权重增量 = 1
    :return:
    """
    assert m >= 2, f"m must >= 2, received m = {m}"
    stack = [(0, [], 1.0)]  # 初始化栈，元素为 (当前索引, 当前组合, 剩余可分配权重)

    while stack:
        index, cur_combination, remaining_sum = stack.pop()

        if len(cur_combination) == m:
            if round(remaining_sum, 2) <= 0:
                yield tuple(cur_combination)
            continue

        # 模拟递归，获取下一个可能的权重值
        max_valid_value = round(1.0 - (m - index - 1) * (1 / count) - sum(cur_combination), 2)
        for i in range(1, count):
            next_value = round(i / count, 2)
            if next_value <= max_valid_value:
                # 特殊处理最后一个权重
                if index == m - 1:
                    if next_value == round(1 - sum(cur_combination), 2):
                        stack.append((index + 1, cur_combination + [next_value], round(remaining_sum - next_value, 2)))
                        break
                    else:
                        continue
                else:
                    stack.append((index + 1, cur_combination + [next_value], round(remaining_sum - next_value, 2)))
            else:
                break


if __name__ == '__main__':
    minWeight = 0.1
    count_ = int(1 / minWeight)
    print(f"count = {count_}")

    res_ls = list(weightCombinations(3, count=count_))
    res_ls.sort()
    print(f"len(res_ls) = {len(res_ls)}")
    pprint(res_ls)
    res_set = set(res_ls)
    print(f"len(res_set) == len(res_ls)：{len(res_set) == len(res_ls)}")
    print("- " * 10)

    # res_ls = list(weightCombinations(2, count=count_))
    # print(f"len(res_ls) = {len(res_ls)}")
    # pprint(res_ls)
    # res_set = set(res_ls)
    # print(f"len(res_set) == len(res_ls)：{len(res_set) == len(res_ls)}")
    # print("- " * 10)
