import time
from pprint import pprint


class Group(object):
    def __init__(self, group_id, super_group_id):
        self.GROUP_ID = group_id
        self.SUPER_GROUP_ID = super_group_id


# I = 0


def recursion_retrieve(group_obj_ls: list, sub_group_id_data: [dict, ...]):
    """
    递归查询子组
    :param group_obj_ls: 全部组对象的列表
    :param sub_group_id_data: 传入一个空列表，保存子组对象
    :return:
    """
    # global I
    # I += 1
    start_count = len(group_obj_ls)

    # input_super_group_id_ls = list()
    # for key in list(sub_group_id_data.keys()):
    #     input_super_group_id_ls.extend(list(sub_group_id_data[key].keys()))

    # map_ = {list(item.keys())[0]: list(item.values())[0] for item in sub_group_data}
    map_ = dict()
    for item in sub_group_id_data:
        for key in item.keys():
            map_[key] = item[key]
    input_super_group_id_ls = [list(x.keys())[0] for x in sub_group_id_data]

    for group in group_obj_ls[:]:
        if group.SUPER_GROUP_ID in input_super_group_id_ls:
            map_[group.SUPER_GROUP_ID][group.GROUP_ID] = dict()

            group_obj_ls.remove(group)

    end_count = len(group_obj_ls)
    print(f"start_count = {start_count}")
    print(f"end_count = {end_count}")
    if end_count == start_count:
        return
    else:
        _sub_group_id_data = list()
        for item in list(map_.values()):
            # item:dict
            for key in item.keys():
                _sub_group_id_data.append({key: item[key]})
        recursion_retrieve(group_obj_ls, _sub_group_id_data)


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

    super_group_id_dict = {1: dict()}  # 用户属于的组
    # super_group_id_dict = {10: dict()}  # 用户属于的组

    sub_group_data = [{key: super_group_id_dict[key]} for key in super_group_id_dict]

    t1 = time.time()
    recursion_retrieve(obj_ls, sub_group_data)
    t2 = time.time()
    print("- " * 30)
    print("耗时：{}".format(t2 - t1))
    print("super_group_id_dict = ")
    pprint(super_group_id_dict)
    # print("I = {}".format(I))

    # print("all group_id_ls ={}".format(list(set(sub_group_ls + super_group_id_ls))))
