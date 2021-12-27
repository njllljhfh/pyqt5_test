# -*- coding:utf-8 -*-
import copy


class FunctionMenu(object):
    NO_SUPER_GROUP_ID = 0

    def __init__(self, func_info):
        self.func_info = func_info
        self._func_menu_flat = self._generate_func_menu_flat()

    def _generate_func_menu_flat(self) -> dict:
        """
        组织功能菜单
        将所有菜单放在同一级，字典的key表示菜单id，字典的value中的sub_func_ls表示菜单下的子功能或子菜单
        O(n)
        """
        super_id_set = {func["super_id"] for func in self.func_info.values()}
        # print(f"super_id_set = {super_id_set}")

        func_menu_flat = {}
        for func_id, func in self.func_info.items():
            func_ = {"sub_func_ls": []}
            func_.update(func)
            # func_ = func
            super_id = func["super_id"]
            if (func_id in super_id_set) and (func_id not in func_menu_flat):
                func_menu_flat[func_id] = {
                    "sub_func_ls": []
                }
                func_menu_flat[func_id].update(func_)

            if super_id in func_menu_flat:
                func_menu_flat[super_id]["sub_func_ls"].append(func_)
            else:
                func_menu_flat[super_id] = {
                    "sub_func_ls": [func_]
                }
                super_func = self.func_info.get(super_id)
                if super_func:
                    func_menu_flat[super_id].update(super_func)

        return func_menu_flat

    def _recur_func_menu(self, func_menu, menu_func_id) -> dict:
        """
        递归组织层级的菜单数据
        O(n)
        :param func_menu:
        :param menu_func_id:
        :return:
        """
        length = len(func_menu)
        if length == 1:
            return func_menu

        sub_func_ls = func_menu[menu_func_id]["sub_func_ls"]
        for i, sub_func in enumerate(sub_func_ls):
            sub_func_id = sub_func["func_id"]
            if sub_func_id in func_menu:
                replace_func = func_menu[sub_func_id]
                sub_func_ls[i] = replace_func
                self._recur_func_menu(func_menu, sub_func_id)
                func_menu.pop(sub_func_id)

                length = len(func_menu)
                if length == 1:
                    return func_menu

    @property
    def func_menu_flat(self):
        return self._func_menu_flat

    def generate(self):
        """生成功能菜单"""
        res = self._recur_func_menu(copy.deepcopy(self._func_menu_flat), self.NO_SUPER_GROUP_ID)
        return res[self.NO_SUPER_GROUP_ID]["sub_func_ls"]


if __name__ == '__main__':
    from pprint import pprint

    FUNC_INFO = {
        4: {"func_name": "f4", "func_id": 4, "super_id": 1},
        1: {"func_name": "f1", "func_id": 1, "super_id": 2},
        5: {"func_name": "f5", "func_id": 5, "super_id": 2},
        2: {"func_name": "f2", "func_id": 2, "super_id": 0},
        6: {"func_name": "f6", "func_id": 6, "super_id": 3},
        3: {"func_name": "f3", "func_id": 3, "super_id": 4},
    }

    # FUNC_INFO = {
    #     4: {"func_name": "f4", "func_id": 4, "super_id": 0},
    #     1: {"func_name": "f1", "func_id": 1, "super_id": 0},
    #     5: {"func_name": "f5", "func_id": 5, "super_id": 0},
    #     2: {"func_name": "f2", "func_id": 2, "super_id": 0},
    #     6: {"func_name": "f6", "func_id": 6, "super_id": 0},
    #     3: {"func_name": "f3", "func_id": 3, "super_id": 0},
    # }

    function_menu = FunctionMenu(FUNC_INFO)
    func_menu_flat = function_menu._generate_func_menu_flat()
    # pprint(func_menu_flat, width=4)
    print("- " * 30)

    print(f"fun_menu = {function_menu.generate()}")
