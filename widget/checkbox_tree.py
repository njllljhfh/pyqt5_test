import sys

from PyQt5.QtWidgets import QApplication, QTreeWidgetItem, QTreeWidget
from PyQt5.QtCore import Qt

"""
带复选框的树

每个节点的数据格式：
{
    "node_name": "xxx",  # 节点在界面上显示的名称
    "data":{...},        # 节点的用户数据
    "sub_data": [...],   # 节点的子节点列表
}
如果没有子节点，则 "sub_data" 字段的值为 None
"""


class CheckboxTree(QTreeWidget):
    def __init__(self, parent=None):
        super(CheckboxTree, self).__init__(parent=parent)
        self.setColumnCount(1)
        self.itemChanged.connect(self.on_tree_item_changed_event)

    def set_header_name(self, header_name: str):
        self.setHeaderLabels([header_name])

    def recur_generate_items(self, data_ls, parent_item=None):
        """刷新标注授权树"""
        column = 0

        item_ls = []
        for data in data_ls:
            custom_data = data["data"]
            node_name = data["node_name"]

            if parent_item:
                item = QTreeWidgetItem(parent_item)
            else:
                item = QTreeWidgetItem(self)

            item.setData(0, Qt.UserRole, custom_data)
            item.setText(column, node_name)
            item.setCheckState(column, Qt.Unchecked)
            item_ls.append(item)

            sub_data = data["sub_data"]
            if sub_data:
                self.recur_generate_items(sub_data, parent_item=item)

        if parent_item:
            parent_item.addChildren(item_ls)

        self.expandAll()

        # - - -
        # column = 0
        # self.clear()
        # # self.oldAuthorizedUserLs.clear()
        # for groupData in self.annotationAuthorizationDataLs:
        #     # 设置根节点
        #     groupItem = QTreeWidgetItem(self.ui.annotationAuthorizationTree)
        #     groupItem.group_id = groupData["group_id"]
        #     groupItem.setText(column, groupData["group_name"])
        #     groupItem.setCheckState(column, Qt.Unchecked)
        #     if groupData["users"]:
        #         # 设置子节点
        #         userItemLs = list()
        #         for user in groupData["users"]:
        #             # 设置子节点1
        #             userItem = QTreeWidgetItem(None)
        #             userItem.user_id = user["user_id"]
        #             userItem.user_group_id = groupData["group_id"]
        #             userItem.setText(column, user["user_name"])
        #             # njl1.setText(1, 'ios')
        #             if user["is_authorized"]:
        #                 userItem.setCheckState(column, Qt.Checked)
        #                 self.oldAuthorizedUserLs.append({
        #                     "user_id": userItem.user_id,  # 用户ID
        #                     "user_group_id": userItem.user_group_id,  # 用户组ID
        #                 })
        #                 # TODO：判断该用户的权限是否可以修改
        #                 # if int(user["is_unchangeable"]) == self.AuthorizationType.unchangeable.value:
        #                 #     userItem.setDisabled(True)
        #             else:
        #                 userItem.setCheckState(column, Qt.Unchecked)
        #             userItemLs.append(userItem)
        #             groupItem.addChildren(userItemLs)
        #         # 更新groupItem的选中状态
        #         self.onTreeItemChangedEvent(userItemLs[0])
        #     else:
        #         pass
        #
        # # 节点全部展开
        # self.expandAll()
        # # 加载根节点的所有属性与子控件
        # # self.ui.annotationPermissionTree.addTopLevelItems(group_node_ls)

    def update_parent_item_check_state(self, qTreeWidgetItem: QTreeWidgetItem, column=0):
        """
        Recursively Update check-box state of parent node.
        :param qTreeWidgetItem: QTreeWidget中的item
        :param column: 列号
        :return: None
        """
        # print(f"父节点执行了")
        parentItem = qTreeWidgetItem.parent()
        print(f"父节点执行了:parentItem={parentItem}")
        if not parentItem:
            return

        selectedCount = 0  # parentItem下被勾选的子childItem的个数
        partiallyCount = 0
        childCount = parentItem.childCount()

        # disableChildCount = 0
        for pointerInt in range(childCount):
            childItem = parentItem.child(pointerInt)
            if childItem.checkState(column) == Qt.Checked:
                selectedCount += 1
            elif childItem.checkState(column) == Qt.PartiallyChecked:
                partiallyCount += 1
            # if childItem.isDisabled():
            #     disableChildCount += 1
        pass

        if selectedCount == 0 and partiallyCount == 0:
            # 如果没有子项被选中，父项设置为未选中状态
            parentItem.setCheckState(column, Qt.Unchecked)
        elif selectedCount == childCount:
            # 如果子项全部被选中，父项则设置为选中状态
            parentItem.setCheckState(column, Qt.Checked)
            # if disableChildCount == childCount:
            #     parentItem.setDisabled(True)
        else:
            # 如果有部分子项被选中，父项设置为部分选中状态
            parentItem.setCheckState(column, Qt.PartiallyChecked)

        self.update_parent_item_check_state(parentItem)

    def on_tree_item_changed_event(self, qTreeWidgetItem: QTreeWidgetItem, column=0):
        """
        annotationAuthorizationTree的QTreeWidgetItem-发生变化事件(如勾选状态发生变化)
        :param qTreeWidgetItem: QTreeWidget中的item
        :param column: 列号
        :return: None
        """
        childCount = qTreeWidgetItem.childCount()
        if qTreeWidgetItem.checkState(column) == Qt.Checked:
            if childCount > 0:
                # Check check-boxes of all child nodes.
                for pointerInt in range(childCount):
                    childItem = qTreeWidgetItem.child(pointerInt)
                    # if childItem.isDisabled() is True:
                    #     childItem.setCheckState(column, Qt.Checked)
                    # else:
                    #     childItem.setCheckState(column, Qt.Checked)
                    childItem.setCheckState(column, Qt.Checked)
            else:
                self.update_parent_item_check_state(qTreeWidgetItem)
        elif qTreeWidgetItem.checkState(column) == Qt.Unchecked:
            if childCount > 0:
                # Uncheck check-boxes of all child nodes.
                for pointerInt in range(childCount):
                    childItem = qTreeWidgetItem.child(pointerInt)
                    # if childItem.isDisabled() is True:
                    #     childItem.setCheckState(column, Qt.Checked)
                    # else:
                    #     childItem.setCheckState(column, Qt.Unchecked)
                    childItem.setCheckState(column, Qt.Unchecked)
            else:
                self.update_parent_item_check_state(qTreeWidgetItem)

    def get_selected_node_data(self):
        # TODO: 获取勾选节点的用户数据
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # data = [
    #     {
    #         "aoi_d_id": 84,
    #         "machine_code": "未知",
    #         "machine_name": "",
    #         "work_dir": "踩踩踩1",
    #         "product_type_history_list": [
    #             {
    #                 "product_type_id": 84,
    #                 "product_type_name": "product01",
    #                 "setup_list": [
    #                     {
    #                         "setup_name": "setup01",
    #                         "lot_list": [
    #                             {
    #                                 "lot_name": "A05054.19",
    #                                 "wafer_detect_status_list": [
    #                                     {
    #                                         "wafer_id": 241,
    #                                         "wafer_code": "09",
    #                                         "status": 0
    #                                     }
    #                                 ]
    #                             }
    #                         ]
    #                     }
    #                 ]
    #             }
    #         ]
    #     },
    #     {
    #         "aoi_d_id": 85,
    #         "machine_code": "未知",
    #         "machine_name": "SA1201A-NA-Full Scan-Stretched",
    #         "work_dir": "踩踩踩2",
    #         "product_type_history_list": [
    #             {
    #                 "product_type_id": 85,
    #                 "product_type_name": "product01",
    #                 "setup_list": [
    #                     {
    #                         "setup_name": "setup01",
    #                         "lot_list": [
    #                             {
    #                                 "lot_name": "A05080",
    #                                 "wafer_detect_status_list": [
    #                                     {
    #                                         "wafer_id": 242,
    #                                         "wafer_code": "04",
    #                                         "status": 0
    #                                     },
    #                                     {
    #                                         "wafer_id": 243,
    #                                         "wafer_code": "06",
    #                                         "status": 0
    #                                     },
    #                                     {
    #                                         "wafer_id": 244,
    #                                         "wafer_code": "08",
    #                                         "status": 0
    #                                     },
    #                                     {
    #                                         "wafer_id": 245,
    #                                         "wafer_code": "10",
    #                                         "status": 0
    #                                     }
    #                                 ]
    #                             }
    #                         ]
    #                     }
    #                 ]
    #             }
    #         ]
    #     }
    # ]

    test_data = [
        {
            "node_name": "踩踩踩1",
            "data": {
                "aoi_d_id": 84,
                "machine_code": "未知",
                "machine_name": "",
                "work_dir": "踩踩踩1",
            },
            "sub_data": [
                {
                    "node_name": "product01",
                    "data": {
                        "product_type_id": 84,
                        "product_type_name": "product01",
                    },
                    "sub_data": [
                        {
                            "node_name": "setup01",
                            "data": {
                                "setup_name": "setup01",
                            },
                            "sub_data": [
                                {
                                    "node_name": "A05054.19",
                                    "data": {
                                        "lot_name": "A05054.19",
                                    },
                                    "sub_data": [
                                        {
                                            "node_name": "09",
                                            "data": {
                                                "wafer_id": 241,
                                                "wafer_code": "09",
                                                "status": 0
                                            },
                                            "sub_data": None,
                                        },
                                        {
                                            "node_name": "10",
                                            "data": {
                                                "wafer_id": 242,
                                                "wafer_code": "10",
                                                "status": 0
                                            },
                                            "sub_data": None,
                                        }
                                    ]
                                }
                            ],
                        },
                        {
                            "node_name": "setup01",
                            "data": {
                                "setup_name": "setup01",
                            },
                            "sub_data": [
                                {
                                    "node_name": "A05054.19",
                                    "data": {
                                        "lot_name": "A05054.19",
                                    },
                                    "sub_data": [
                                        {
                                            "node_name": "09",
                                            "data": {
                                                "wafer_id": 241,
                                                "wafer_code": "09",
                                                "status": 0
                                            },
                                            "sub_data": None,
                                        },
                                        {
                                            "node_name": "10",
                                            "data": {
                                                "wafer_id": 242,
                                                "wafer_code": "10",
                                                "status": 0
                                            },
                                            "sub_data": None,
                                        }
                                    ]
                                }
                            ],
                        },
                    ]
                },
                {
                    "node_name": "product02",
                    "data": {
                        "product_type_id": 84,
                        "product_type_name": "product02",
                    },
                    "sub_data": [
                        {
                            "node_name": "setup02",
                            "data": {
                                "setup_name": "setup02",
                            },
                            "sub_data": [
                                {
                                    "node_name": "A05054.29",
                                    "data": {
                                        "lot_name": "A05054.29",
                                    },
                                    "sub_data": [
                                        {
                                            "node_name": "29",
                                            "data": {
                                                "wafer_id": 251,
                                                "wafer_code": "29",
                                                "status": 0
                                            },
                                            "sub_data": None,
                                        },
                                        {
                                            "node_name": "20",
                                            "data": {
                                                "wafer_id": 252,
                                                "wafer_code": "20",
                                                "status": 0
                                            },
                                            "sub_data": None,
                                        }
                                    ]
                                }
                            ],
                        }
                    ]
                }
            ],
        },
        {
            "node_name": "踩踩踩2",
            "data": {
                "aoi_d_id": 84,
                "machine_code": "未知",
                "machine_name": "",
                "work_dir": "踩踩踩1",
            },
            "sub_data": [
                {
                    "node_name": "product01",
                    "data": {
                        "product_type_id": 84,
                        "product_type_name": "product01",
                    },
                    "sub_data": [
                        {
                            "node_name": "setup01",
                            "data": {
                                "setup_name": "setup01",
                            },
                            "sub_data": [
                                {
                                    "node_name": "A05054.19",
                                    "data": {
                                        "lot_name": "A05054.19",
                                    },
                                    "sub_data": [
                                        {
                                            "node_name": "09",
                                            "data": {
                                                "wafer_id": 241,
                                                "wafer_code": "09",
                                                "status": 0
                                            },
                                            "sub_data": None,
                                        },
                                        {
                                            "node_name": "10",
                                            "data": {
                                                "wafer_id": 242,
                                                "wafer_code": "10",
                                                "status": 0
                                            },
                                            "sub_data": None,
                                        }
                                    ]
                                }
                            ],
                        },
                        {
                            "node_name": "setup01",
                            "data": {
                                "setup_name": "setup01",
                            },
                            "sub_data": [
                                {
                                    "node_name": "A05054.19",
                                    "data": {
                                        "lot_name": "A05054.19",
                                    },
                                    "sub_data": [
                                        {
                                            "node_name": "09",
                                            "data": {
                                                "wafer_id": 241,
                                                "wafer_code": "09",
                                                "status": 0
                                            },
                                            "sub_data": None,
                                        },
                                        {
                                            "node_name": "10",
                                            "data": {
                                                "wafer_id": 242,
                                                "wafer_code": "10",
                                                "status": 0
                                            },
                                            "sub_data": None,
                                        }
                                    ]
                                }
                            ],
                        },
                    ]
                },
                {
                    "node_name": "product02",
                    "data": {
                        "product_type_id": 84,
                        "product_type_name": "product02",
                    },
                    "sub_data": [
                        {
                            "node_name": "setup02",
                            "data": {
                                "setup_name": "setup02",
                            },
                            "sub_data": [
                                {
                                    "node_name": "A05054.29",
                                    "data": {
                                        "lot_name": "A05054.29",
                                    },
                                    "sub_data": [
                                        {
                                            "node_name": "29",
                                            "data": {
                                                "wafer_id": 251,
                                                "wafer_code": "29",
                                                "status": 0
                                            },
                                            "sub_data": None,
                                        },
                                        {
                                            "node_name": "20",
                                            "data": {
                                                "wafer_id": 252,
                                                "wafer_code": "20",
                                                "status": 0
                                            },
                                            "sub_data": None,
                                        }
                                    ]
                                }
                            ],
                        }
                    ]
                }
            ],
        },
    ]

    my_widget = CheckboxTree()
    my_widget.clear()
    my_widget.set_header_name("多选树组件")
    my_widget.recur_generate_items(test_data)
    my_widget.resize(260, 800)
    my_widget.show()
    sys.exit(app.exec_())
