import time
from pprint import pprint


class Group(object):
    def __init__(self, group_id, super_group_id):
        self.GROUP_ID = group_id
        self.SUPER_GROUP_ID = super_group_id


# I = 0


def recursion_retrieve(group_obj_ls: list, sub_group_id_data: [dict, ...], is_sub_group=True):
    """
    递归查询子级组或父级组
    :param group_obj_ls: 全部组对象的列表
    :param sub_group_id_data: [{父级组id: 空字典}]
    :param is_sub_group: True:组织下级组， False:组织上级组
    :return:
    """
    start_count = len(group_obj_ls)

    map_ = dict()
    for item in sub_group_id_data:
        for key in item.keys():
            map_[key] = item[key]

    input_super_group_id_ls = [list(x.keys())[0] for x in sub_group_id_data]

    if is_sub_group:
        # 组织下级组
        for group in group_obj_ls[:]:
            if group.SUPER_GROUP_ID in input_super_group_id_ls:
                map_[group.SUPER_GROUP_ID][group.GROUP_ID] = dict()
                group_obj_ls.remove(group)
    else:
        # 组织上级组
        for group in group_obj_ls[:]:
            if group.GROUP_ID in input_super_group_id_ls:
                map_[group.GROUP_ID][group.SUPER_GROUP_ID] = dict()
                group_obj_ls.remove(group)

    end_count = len(group_obj_ls)
    # print(f"start_count = {start_count}")
    # print(f"end_count = {end_count}")
    if end_count == start_count:
        return
    else:
        _sub_group_id_data = list()
        for item in list(map_.values()):
            # item:dict
            for key in item.keys():
                _sub_group_id_data.append({key: item[key]})
        recursion_retrieve(group_obj_ls, _sub_group_id_data, is_sub_group=is_sub_group)


if __name__ == '__main__':
    group_0 = Group(0, None)
    group_1 = Group(1, 0)
    group_2 = Group(2, 1)  # is a sub group of the group with group_id = 1
    group_3 = Group(3, 2)  # is a sub group of the group with group_id = 1
    group_4 = Group(4, 1)  # is a sub group of the group with group_id = 1
    group_5 = Group(5, 3)  # is a sub group of the group with group_id = 1
    group_6 = Group(6, 1)  # is a sub group of the group with group_id = 1
    group_7 = Group(7, 0)
    group_8 = Group(8, None)
    group_9 = Group(9, 10)  # is a sub group of the group with group_id = 1
    group_10 = Group(10, 4)  # is a sub group of the group with group_id = 1
    group_11 = Group(11, 9)  # is a sub group of the group with group_id = 1
    group_12 = Group(12, 11)  # is a sub group of the group with group_id = 1
    obj_ls = [
        group_1,
        group_2,
        group_3,
        group_4,
        group_5,
        group_6,
        group_7,
        group_8,
        group_9,
        group_10,
        group_11,
        group_12,
    ]

    t1 = time.time()

    # 假设用户属于两个组
    group_a = group_1
    group_b = group_2
    group_data = {
        group_a.GROUP_ID: {
            "super_group": dict(),  # 字典的深度方向是组层级上升的方向（即字典越深，字典的键表示的组级别越高）
            "sub_group": dict()  # 字典的深度方向是组层级下降的方向（即字典越深，字典的键表示的组级别越低）
        },
        group_b.GROUP_ID: {
            "super_group": dict(),
            "sub_group": dict()
        }
    }

    # 组织第一个组
    # 上级组
    if group_a.SUPER_GROUP_ID:
        super_group_id_dict = {group_a.SUPER_GROUP_ID: dict()}  # key:用户的第一层父级组id
        sub_group_data = [{key: super_group_id_dict[key]} for key in super_group_id_dict]
        recursion_retrieve(obj_ls[:], sub_group_data, is_sub_group=False)
        group_data[group_a.GROUP_ID]["super_group"].update(super_group_id_dict)
    # 下级组
    super_group_id_dict = {group_a.GROUP_ID: dict()}  # key:用户所在组id
    sub_group_data = [{key: super_group_id_dict[key]} for key in super_group_id_dict]
    recursion_retrieve(obj_ls[:], sub_group_data, is_sub_group=True)
    group_data[group_a.GROUP_ID]["sub_group"].update(super_group_id_dict[group_a.GROUP_ID])
    # - - -

    # 组织第二个组
    # 上级组
    if group_b.SUPER_GROUP_ID:
        super_group_id_dict = {group_b.SUPER_GROUP_ID: dict()}  # key:用户的第一层父级组id
        sub_group_data = [{key: super_group_id_dict[key]} for key in super_group_id_dict]
        recursion_retrieve(obj_ls[:], sub_group_data, is_sub_group=False)
        group_data[group_b.GROUP_ID]["super_group"].update(super_group_id_dict)
    # 下级组
    super_group_id_dict = {group_b.GROUP_ID: dict()}  # key:用户所在的组id
    sub_group_data = [{key: super_group_id_dict[key]} for key in super_group_id_dict]
    recursion_retrieve(obj_ls[:], sub_group_data, is_sub_group=True)
    group_data[group_b.GROUP_ID]["sub_group"].update(super_group_id_dict[group_b.GROUP_ID])
    pprint(group_data)

    t2 = time.time()
    print("\n", "- " * 30)
    print("耗时：{}".format(t2 - t1))
