import time


class Group(object):
    def __init__(self, group_id, super_group_id):
        self.GROUP_ID = group_id
        self.SUPER_GROUP_ID = super_group_id


I = 0


def recursion_retrieve(input_super_group_id_ls: list, group_obj_ls: list, sub_group_id_ls: list):
    """
    递归查询子组
    :param input_super_group_id_ls: 最上层组的id列表
    :param group_obj_ls: 全部组对象的列表
    :param sub_group_id_ls: 传入一个空列表，保存子组对象
    :return:
    """
    global I
    I += 1
    start_count = len(group_obj_ls)
    for group in group_obj_ls[:]:
        if group.SUPER_GROUP_ID in input_super_group_id_ls:
            sub_group_id_ls.append(group.GROUP_ID)
            group_obj_ls.remove(group)

    end_count = len(group_obj_ls)
    print(f"start_count = {start_count}")
    print(f"end_count = {end_count}")
    if end_count == start_count:
        return
    else:
        recursion_retrieve(sub_group_id_ls, group_obj_ls, sub_group_id_ls)


if __name__ == '__main__':
    obj_ls = [
        Group(1, 0),
        Group(2, 1),  # is a sub group of the group with group_id = 1
        Group(3, 2),  # is a sub group of the group with group_id = 1
        Group(4, 1),  # is a sub group of the group with group_id = 1
        Group(5, 3),  # is a sub group of the group with group_id = 1
        Group(6, 1),  # is a sub group of the group with group_id = 1
        Group(7, 0),
        Group(8, 7),
        Group(9, 10),  # is a sub group of the group with group_id = 1
        Group(10, 4),  # is a sub group of the group with group_id = 1
        Group(11, 9),  # is a sub group of the group with group_id = 1
        Group(12, 11),  # is a sub group of the group with group_id = 1
    ]

    super_group_id_ls = [1, 10]
    # super_group_id_ls = [1, ]

    sub_group_ls = list()
    t1 = time.time()
    recursion_retrieve(super_group_id_ls, obj_ls, sub_group_ls)
    t2 = time.time()
    print("耗时：{}".format(t2 - t1))
    sub_group_ls.sort()
    print("sub_group_ls ={}".format(sub_group_ls))
    print("I = {}".format(I))

    print("all group_id_ls ={}".format(list(set(sub_group_ls + super_group_id_ls))))
