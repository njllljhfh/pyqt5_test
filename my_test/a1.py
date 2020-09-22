# -*- coding:utf-8 -*-
if __name__ == '__main__':
    # a = [tuple([1, 1]), tuple([1, 2]), tuple([1, 1]), tuple([1, 1])]
    # b = set(a)
    # c = list(b)
    # print(c)
    position = [[1, 1], [1, 2], [1, 1], [1, 2], [1, 3]]
    defect_position = list()
    for position_info in position:
        position_str = f"{chr(position_info[0] + 64)}" + str(position_info[1])
        if position_str not in defect_position:
            defect_position.append(position_str)

    print("defect_position = {}".format(defect_position))