import time
from pprint import pprint
from typing import List, Dict


class Group(object):
    """用户组"""

    def __init__(self, group_id, super_group_id):
        self.GROUP_ID = group_id
        self.SUPER_GROUP_ID = super_group_id


class UserGroupData(object):

    def __init__(self, user_group_obj_ls: List[Group], group_obj_ls_all: List[Group]):
        """
        :param user_group_obj_ls: 用户所属的组对象列表
        :param group_obj_ls_all: 全部用户组对象列表
        """
        self.user_group_obj_ls = user_group_obj_ls
        self._group_data: Dict[int, dict] = {}

        self._group_layer_data: Dict[str, dict] = {
            "sub_group_layer_data": dict(),
            "super_group_layer_data": dict(),
        }

        self.update_group_data(self.user_group_obj_ls, group_obj_ls_all)

    def update_group_data(self, user_group_obj_ls: List[Group], group_obj_ls_all: List[Group]):
        """更新数据"""
        self.user_group_obj_ls = user_group_obj_ls
        self._organize_group_data(group_obj_ls_all)
        self._organize_group_layer_data()

    @property
    def group_data(self):
        return self._group_data

    @property
    def group_layer_data(self):
        return self._group_layer_data

    def _recur_group(self, group_obj_ls: List[Group], sub_group_id_data: List[dict], is_sub_group: bool = True):
        """
        递归查询子级组，或父级组
        :param group_obj_ls: 全部组对象的列表
        :param sub_group_id_data: [{父级组id: 空字典}]
        :param is_sub_group: True:组织下级组， False:组织上级组
        :return:
        """
        start_count = len(group_obj_ls)

        map_ = dict()
        for item in sub_group_id_data:
            # item:dict
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
                    if group.SUPER_GROUP_ID is not None:
                        map_[group.GROUP_ID][group.SUPER_GROUP_ID] = dict()
                    group_obj_ls.remove(group)

        end_count = len(group_obj_ls)
        if end_count == start_count:
            return
        else:
            _sub_group_id_data = list()
            for item in list(map_.values()):
                # item:dict
                for key in item.keys():
                    _sub_group_id_data.append({key: item[key]})
            self._recur_group(group_obj_ls, _sub_group_id_data, is_sub_group=is_sub_group)

    def _organize_group_data(self, all_group_obj_ls: List[Group]):
        """
        组织用户全部的组数据
        :param all_group_obj_ls:
        :return:
        """
        self._group_data.clear()
        for group_obj in self.user_group_obj_ls:
            group_id = group_obj.GROUP_ID
            super_group_id = group_obj.SUPER_GROUP_ID
            self._group_data[group_id] = {
                "super_group": dict(),  # 字典的深度方向是组层级上升的方向（即字典越深，字典的键表示的组级别越高）
                "sub_group": dict()  # 字典的深度方向是组层级下降的方向（即字典越深，字典的键表示的组级别越低）
            }
            # 组织一个用户组上下级组数据
            # 上级组
            if super_group_id is not None:
                super_group_id_dict = {super_group_id: dict()}  # key:用户的第一层父级组id
                sub_group_data = [{key: super_group_id_dict[key]} for key in super_group_id_dict]
                self._recur_group(all_group_obj_ls[:], sub_group_data, is_sub_group=False)
                self._group_data[group_id]["super_group"].update(super_group_id_dict)
            # 下级组
            super_group_id_dict = {group_id: dict()}  # key:用户所在组id
            sub_group_data = [{key: super_group_id_dict[key]} for key in super_group_id_dict]
            self._recur_group(all_group_obj_ls[:], sub_group_data, is_sub_group=True)
            self._group_data[group_id]["sub_group"].update(super_group_id_dict[group_id])

    def _organize_group_layer_data(self):
        """组织用户组层级信息"""
        sub_group_layer_data = dict()
        super_group_layer_data = dict()
        for group_id in self._group_data:
            # group_id: 用户所在组的id
            print(f"(用户所在组id = {group_id}) * * * * * * * * * * * * * *")
            print(f"组织子级组层级数据 - - - - -")
            group_id_ls = list()
            sub_group_data = self._group_data[group_id]["sub_group"]
            pprint(sub_group_data, width=4)
            self._recur_group_layer(sub_group_data, group_id_ls)
            sub_group_layer_data[group_id] = group_id_ls
            self._group_layer_data["sub_group_layer_data"] = sub_group_layer_data

            print(f"组织父级组层级数据 - - - - -")
            group_id_ls = list()
            super_group_data = self._group_data[group_id]["super_group"]
            pprint(super_group_data, width=4)
            self._recur_group_layer(super_group_data, group_id_ls)
            super_group_layer_data[group_id] = group_id_ls
            self._group_layer_data["super_group_layer_data"] = super_group_layer_data

    def _recur_group_layer(self, group_data: dict, group_id_ls: list):
        """
        递归组织一个用户组下个各层子级组id，或各层父级组id
        :param group_data: 一个用户组的子级组的数据，或父级组数据
        :param group_id_ls: 空 list，用于保存各个层的组id
        :return:
        """
        group_id_ls_current_layer = list(group_data.keys())
        if group_id_ls_current_layer:
            group_id_ls.append(group_id_ls_current_layer)
        else:
            # group_data 的keys是空的，则values也是空的
            return

        group_next_layer_origin_data: List[dict] = list(group_data.values())
        group_next_layer_data = dict()
        for groups_next_layer in group_next_layer_origin_data:
            for key in groups_next_layer.keys():
                group_next_layer_data[key] = groups_next_layer[key]

        if group_next_layer_data:
            self._recur_group_layer(group_next_layer_data, group_id_ls)
        else:
            # group_data 的keys不是空的，但是values中的字典全是空的
            return


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
    group_9 = Group(9, 4)  # is a sub group of the group with group_id = 1
    group_10 = Group(10, 4)  # is a sub group of the group with group_id = 1
    group_11 = Group(11, 9)  # is a sub group of the group with group_id = 1
    group_12 = Group(12, 11)  # is a sub group of the group with group_id = 1
    obj_ls = [
        group_0,
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
    # 用户属于的组
    user_group_obj_ls_ = [group_1, group_2, group_8]
    user_group_data = UserGroupData(user_group_obj_ls_, obj_ls)
    print("* " * 50)
    print(f"用户组结构:")
    pprint(user_group_data.group_data, width=1)
    print("* " * 50)
    print(f"用户组-父级id，子级id分层结构:")
    pprint(user_group_data.group_layer_data)

    print(f"= " * 70)
    obj_ls = [group_0, group_1, group_2, group_3, group_4, group_5, ]
    user_group_obj_ls_ = [group_1, group_2]
    user_group_data.update_group_data(user_group_obj_ls_, obj_ls)
    print(f"用户组结构:")
    pprint(user_group_data.group_data, width=1)
    print("* " * 50)
    print(f"用户组-父级id，子级id分层结构:")
    pprint(user_group_data.group_layer_data)

    t2 = time.time()
    print("耗时：{}".format(t2 - t1))
