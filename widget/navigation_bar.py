# -*- coding:utf-8 -*-
# __author__ = "Dragon"

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFrame, QGridLayout, QTreeWidget, QApplication, QTreeWidgetItem


class NavigationTreeItem(QTreeWidgetItem):

    def __init__(self, identification, *args, parent=None):
        super().__init__(parent, *args)
        self._identification = identification

    @property
    def identification(self):
        return self._identification


class NavigationBar(QFrame):
    # This signal is emitted when the navigation item is clicked.
    # arg1: the identification of item clicked.
    signal_navigation_item_clicked = pyqtSignal(object)

    def __init__(self, navigation_data: dict, parent=None):
        super().__init__(parent=parent)

        layout = QGridLayout(self)
        layout.setObjectName("layout")

        """=== UI ==="""
        self.navigation_tree = QTreeWidget(self)
        self.navigation_tree.setObjectName("navigation_tree")
        # self.navigation_tree.headerItem().setText(0, "1")
        layout.addWidget(self.navigation_tree, 0, 0, 1, 1)

        """=== Variables. ==="""
        self._default_header_name = "Navigation bar"
        self._navigation_data: dict = navigation_data
        self._first_tree_item = None

        """=== Initialize. ==="""
        self.set_header_name(self._default_header_name)
        self._generate_tree(self._navigation_data)
        if self._first_tree_item:
            self.navigation_tree.setCurrentItem(self._first_tree_item)

        qss = """
        QTreeWidget::item{
            margin: 2px;
        }
        """
        self.setStyleSheet(qss)

        """=== Connect signals. ==="""
        self._connect_signal()

    def _connect_signal(self):
        """Connect signals."""
        self.navigation_tree.itemClicked.connect(self._handle_tree_item_clicked)

    def _handle_tree_item_clicked(self, tree_item: NavigationTreeItem, column=None):
        """Handle the tree item clicked event."""
        print(f"tree_item.identification={tree_item.identification}, column={column}")
        self.signal_navigation_item_clicked.emit(tree_item.identification)

    def _generate_tree(self, item_data: dict, previous_navigation: NavigationTreeItem = None):
        """Recursively generate tree item."""
        # column = 0
        for k, v in item_data.items():
            identification = v["identification"]
            sub_navigation = v["sub_navigation"]

            if not previous_navigation:
                navigation_item = NavigationTreeItem(identification, parent=self.navigation_tree)
                if not self._first_tree_item:
                    self._first_tree_item = navigation_item
            else:
                navigation_item = NavigationTreeItem(identification, parent=previous_navigation)
            navigation_item.setText(0, k)

            if sub_navigation:
                if previous_navigation:
                    previous_navigation.addChild(navigation_item)
                self._generate_tree(sub_navigation, previous_navigation=navigation_item)

    def set_header_name(self, header_name: str):
        """Set header name."""
        self.navigation_tree.setHeaderLabels([header_name])

    def unfold_all_navigations(self):
        self.navigation_tree.expandAll()

    def fold_all_navigations(self):
        self.navigation_tree.collapseAll()


if __name__ == "__main__":
    import sys
    from enum import Enum, unique
    from pprint import pprint


    class BaseEnum(Enum):

        @classmethod
        def value_exists(cls, value):
            """
            Determine whether the value is in class.
            :param value: The value of enumerate class.  <type: int>
            :return: True or False.  <type: bool>
            """
            if value in [member.value for member in cls.__members__.values()]:
                return True
            else:
                return False

        @classmethod
        def value_list(cls):
            """
            Get value list.
            :return: Value list.  <type: list>
            """

            return [member.value for member in cls.__members__.values()]

        @classmethod
        def custom_name(cls, enum_value):
            """ Map enum value to custom name. """
            pass


    @unique
    class NavigationEnum(BaseEnum):
        mysql_db = 0
        mysql_db_1 = 1
        mysql_db_2 = 2

        config = 3
        config_1 = 4

        @classmethod
        def custom_name(cls, enum_value):
            value_map = {
                cls.mysql_db.value: "mysql数据库",
                cls.mysql_db_1.value: "mysql数据库_1",
                cls.mysql_db_2.value: "mysql数据库_2",
                cls.config.value: "配置文件",
                cls.config_1.value: "配置文件_1",
            }
            return value_map.get(enum_value)


    # - - -
    app = QApplication(sys.argv)
    items_data = {
        NavigationEnum.custom_name(NavigationEnum.mysql_db.value): {
            "identification": NavigationEnum.mysql_db,
            "sub_navigation": {
                NavigationEnum.custom_name(NavigationEnum.mysql_db_1.value): {
                    "identification": NavigationEnum.mysql_db_1,
                    "sub_navigation": None,
                },
                NavigationEnum.custom_name(NavigationEnum.mysql_db_2.value): {
                    "identification": NavigationEnum.mysql_db_2,
                    "sub_navigation": None,
                },
            }
        },
        NavigationEnum.custom_name(NavigationEnum.config.value): {
            "identification": NavigationEnum.config,
            "sub_navigation": {
                NavigationEnum.custom_name(NavigationEnum.config_1.value): {
                    "identification": NavigationEnum.config_1,
                    "sub_navigation": None,
                },
            }
        },
    }
    pprint(items_data)

    my_widget = NavigationBar(items_data)
    my_widget.unfold_all_navigations()

    my_widget.show()
    sys.exit(app.exec_())
