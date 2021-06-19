# -*- coding:utf-8 -*-
# TODO:替换文件
import sys
import logging
from enum import unique
from pprint import pprint

from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QDialog, QApplication, QTreeWidgetItem, QMessageBox

# from api.mvpapi import MvpApi
from ui.annotation_authorization_ui import Ui_AnnotationAuthorization

from widgets.test_data_njl import ANNOTATION_AUTHORIZATION_DATA_LS
from widgets import ResponseCode, BaseEnum

logger = logging.getLogger(__name__)


class AnnotationAuthorizationDialog(QDialog):
    """ Annotation authorization. """

    @unique
    class AuthorizationType(BaseEnum):
        """
        用户对数据集的权限类型
        """
        changeable = 0
        unchangeable = 1

        @classmethod
        def value_name(cls, value):
            """ Map value to Chinese. """
            value_map = {
                cls.changeable.value: "可修改",
                cls.unchangeable.value: "不可修改",
            }
            return value_map.get(value)

    def __init__(self, parent=None, dataset_id=None, row=None, cookies=None):
        super(AnnotationAuthorizationDialog, self).__init__(parent)
        self.ui = Ui_AnnotationAuthorization()
        self.ui.setupUi(self)
        self.dataset_id = dataset_id
        self.row = row
        # self.mvpApi = MvpApi(cookies=cookies)

        self.oldAuthorizedUserLs = list()  # 未修改前，有标注权限的用户列表

        self.setWindowFlags(Qt.WindowCloseButtonHint)  # 只显示关闭按钮 其他的不显示

        # 添加头部信息(QTreeView)
        # model = QStandardItemModel(self.ui.annotationPermissionTreeView)
        # model.setHorizontalHeaderLabels(["标注组"])
        # self.ui.annotationPermissionTreeView.setModel(model)

        # TODO:访问服务器(接口：5、数据集授权用户列表查询  参数：dataset_id)
        try:
            pass
            # response = self.mvpApi.dataset_authorization_list(self.dataset_id)
            # self.annotationAuthorizationDataLs = response["results"]["groups"]
            # TODO:假数据
            # for group in self.annotationAuthorizationDataLs:
            #     if group["group_name"] == "算法部":
            #         group["users"].append(
            #             {
            #                 "user_id": "2019122810000000002",
            #                 "user_name": "用户2",
            #                 "is_authorized": False,  # 当前用户是否已经被授权；true/false
            #                 "is_unchangeable": False,
            #             }
            #         )
            #     if group["group_name"] == "system":
            #         group["users"].append(
            #             {
            #                 "user_id": "2019122810000000111",
            #                 "user_name": "用户x",
            #                 "is_authorized": True,  # 当前用户是否已经被授权；true/false
            #                 "is_unchangeable": True,
            #             }
            #         )
            # - - - - - - - - - -
        except Exception as Error:
            raise Error
        # - - -假数据- - -
        # # 标注人员数据
        self.annotationAuthorizationDataLs = ANNOTATION_AUTHORIZATION_DATA_LS
        # - - -假数据- - -

        # 添加头部信息(QTreeWidget)
        self.ui.annotationAuthorizationTree.setColumnCount(1)
        self.ui.annotationAuthorizationTree.setHeaderLabels(["组/人员"])

        # 刷新树中数据
        self.refreshAnnotationAuthorizationTree()

        # 事件绑定
        self.ui.annotationAuthorizationTree.itemChanged.connect(self.onTreeItemChangedEvent)
        self.ui.confirmBtn.clicked.connect(self.confirmBtnClickedEvent)
        self.ui.cancelBtn.clicked.connect(self.cancelBtnClickedEvent)

    def confirmBtnClickedEvent(self, column=0):
        """确定按钮-点击事件"""

        try:
            logger.info(f"确定修改数据集标注权限?-确定")
            newAuthorizedUserLs = list()
            topLevelItemCount = self.ui.annotationAuthorizationTree.topLevelItemCount()
            for groupPointerInt in range(topLevelItemCount):
                groupItem: QTreeWidgetItem = self.ui.annotationAuthorizationTree.topLevelItem(groupPointerInt)
                if groupItem.checkState(column) == Qt.Checked or groupItem.checkState(
                        column) == Qt.PartiallyChecked:
                    childCount = groupItem.childCount()
                    for childPointerInt in range(childCount):
                        childItem = groupItem.child(childPointerInt)
                        if childItem.checkState(column) == Qt.Checked:
                            newAuthorizedUserLs.append({
                                "user_id": childItem.user_id,  # 用户ID
                                "user_group_id": childItem.user_group_id,  # 用户组ID
                            })

            if self.oldAuthorizedUserLs == newAuthorizedUserLs:
                result = QMessageBox.information(self, "信息", "数据集标注权限未修改，是否关闭授权窗口？", QMessageBox.No, QMessageBox.Yes)
                if result == QMessageBox.Yes:
                    self.close()
                else:
                    pass
            else:
                result = QMessageBox.warning(self, "警告", "确定修改数据集标注授权?", QMessageBox.No, QMessageBox.Yes)
                if result == QMessageBox.Yes:
                    requestData = {
                        "dataset_id": self.dataset_id,
                        "users": newAuthorizedUserLs,
                    }
                    pprint(requestData)
                    # TODO:访问服务器(接口：6、数据集用户授权  参数：dataset_id、requestData)
                    response = self.mvpApi.dataset_authorization(requestData["dataset_id"], requestData["users"])

                    if response["code"] == ResponseCode.success.value:
                        logger.info(f"成功：修改数据集授权")
                        self.accept()
                    else:
                        logger.info(f"失败：修改数据集授权")
                        Error = Exception(f'code:{response["code"]}, msg:{response["msg"]}')
                        raise Error
                        # logger.error(f'code:{response["code"]}, msg:{response["msg"]}')
                        # QMessageBox.warning(self, "警告", str(Error), QMessageBox.Yes, QMessageBox.Yes)
                else:
                    # 恢复修改前的数据
                    self.refreshAnnotationAuthorizationTree()
                    logger.info(f"确定修改数据集标注权限?-取消")
        except Exception as Error:
            logger.error(Error)
            qMessageBox = QMessageBox()
            qMessageBox.warning(self, "警告", str(Error), QMessageBox.Yes, QMessageBox.Yes)

    def cancelBtnClickedEvent(self):
        """取消按钮-点击事件"""
        logger.info(f"取消按钮-点击事件")
        self.close()

    def refreshAnnotationAuthorizationTree(self):
        """刷新标注授权树"""
        column = 0
        self.ui.annotationAuthorizationTree.clear()
        self.oldAuthorizedUserLs.clear()
        for groupData in self.annotationAuthorizationDataLs:
            # 设置根节点
            groupItem = QTreeWidgetItem(self.ui.annotationAuthorizationTree)
            groupItem.group_id = groupData["group_id"]
            groupItem.setText(column, groupData["group_name"])
            groupItem.setCheckState(column, Qt.Unchecked)
            if groupData["users"]:
                # 设置子节点
                userItemLs = list()
                for user in groupData["users"]:
                    # 设置子节点1
                    userItem = QTreeWidgetItem()
                    userItem.user_id = user["user_id"]
                    userItem.user_group_id = groupData["group_id"]
                    userItem.setText(column, user["user_name"])
                    # njl1.setText(1, 'ios')
                    if user["is_authorized"]:
                        userItem.setCheckState(column, Qt.Checked)
                        self.oldAuthorizedUserLs.append({
                            "user_id": userItem.user_id,  # 用户ID
                            "user_group_id": userItem.user_group_id,  # 用户组ID
                        })
                        # TODO：判断该用户的权限是否可以修改
                        # if int(user["is_unchangeable"]) == self.AuthorizationType.unchangeable.value:
                        #     userItem.setDisabled(True)
                    else:
                        userItem.setCheckState(column, Qt.Unchecked)
                    userItemLs.append(userItem)
                    groupItem.addChildren(userItemLs)
                # 更新groupItem的选中状态
                self.onTreeItemChangedEvent(userItemLs[0])
            else:
                pass

        # 节点全部展开
        self.ui.annotationAuthorizationTree.expandAll()
        # 加载根节点的所有属性与子控件
        # self.ui.annotationPermissionTree.addTopLevelItems(group_node_ls)

    """==================================="""
    """=         Custom Events           ="""
    """==================================="""

    def updateParentItemCheckState(self, qTreeWidgetItem: QTreeWidgetItem, column=0):
        """
        Recursively Update check-box state of parent node.
        :param qTreeWidgetItem: QTreeWidget中的item
        :param column: 列号
        :return: None
        """
        print(f"父节点执行了")
        parentItem = qTreeWidgetItem.parent()
        if not parentItem:
            return

        selectedCount = 0  # parentItem下被勾选的子childItem的个数
        childCount = parentItem.childCount()

        disableChildCount = 0
        for pointerInt in range(childCount):
            childItem = parentItem.child(pointerInt)
            if childItem.checkState(column) == Qt.Checked or childItem.checkState(column) == Qt.PartiallyChecked:
                selectedCount += 1
            if childItem.isDisabled():
                disableChildCount += 1

        if selectedCount <= 0:
            # 如果没有子项被选中，父项设置为未选中状态
            parentItem.setCheckState(column, Qt.Unchecked)
        elif 0 < selectedCount < childCount:
            # 如果有部分子项被选中，父项设置为部分选中状态
            parentItem.setCheckState(column, Qt.PartiallyChecked)
        elif selectedCount == childCount:
            # 如果子项全部被选中，父项则设置为选中状态
            parentItem.setCheckState(column, Qt.Checked)
            if disableChildCount == childCount:
                parentItem.setDisabled(True)

        self.updateParentItemCheckState(parentItem)

    def onTreeItemChangedEvent(self, qTreeWidgetItem: QTreeWidgetItem, column=0):
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
                    if childItem.isDisabled() is True:
                        childItem.setCheckState(column, Qt.Checked)
                    else:
                        childItem.setCheckState(column, Qt.Checked)
            else:
                self.updateParentItemCheckState(qTreeWidgetItem)
        elif qTreeWidgetItem.checkState(column) == Qt.Unchecked:
            if childCount > 0:
                # Uncheck check-boxes of all child nodes.
                for pointerInt in range(childCount):
                    childItem = qTreeWidgetItem.child(pointerInt)
                    if childItem.isDisabled() is True:
                        childItem.setCheckState(column, Qt.Checked)
                    else:
                        childItem.setCheckState(column, Qt.Unchecked)
            else:
                self.updateParentItemCheckState(qTreeWidgetItem)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ClassAttrDialog = AnnotationAuthorizationDialog()
    ClassAttrDialog.show()
    sys.exit(app.exec_())
