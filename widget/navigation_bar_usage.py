# -*- coding:utf-8 -*-
# __author__ = "Dragon"
import sys
from enum import Enum, unique

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFrame, QGridLayout, QApplication, QStackedWidget, QVBoxLayout, QLabel, QTableWidget, \
    QHeaderView

from widget.navigation_bar import NavigationBar

"""
The usage of NavigationBar.
"""


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


class SettingPage(QFrame):

    def __init__(self, label_text, parent=None):
        super().__init__(parent=parent)
        layout = QVBoxLayout(self)

        self.label = QLabel(self)
        self.label.setText(label_text)
        layout.addWidget(self.label)

        self.table = QTableWidget(self)
        header_field = [f"{label_text}_a", f"{label_text}_b", f"{label_text}_c"]
        self.table.setColumnCount(len(header_field))
        self.table.setHorizontalHeaderLabels(header_field)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)


class PageContainer(QStackedWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)


class MySetting(QFrame):

    def __init__(self, navigation_data: dict, parent=None):
        super().__init__(parent=parent)

        layout = QGridLayout(self)

        self.navigation_bar = NavigationBar(navigation_data, parent=self)
        self.navigation_bar.setFixedWidth(200)
        layout.addWidget(self.navigation_bar, 0, 0, 1, 1)

        self.page_container = PageContainer(parent=self)
        layout.addWidget(self.page_container, 0, 1, 1, 1)

        self.mysql_db = SettingPage("mysql_db")
        self.mysql_db_1 = SettingPage("mysql_db_1")
        self.mysql_db_2 = SettingPage("mysql_db_2")
        self.config = SettingPage("config")
        self.config_1 = SettingPage("config_1")
        self.page_container.addWidget(self.mysql_db)
        self.page_container.addWidget(self.mysql_db_1)
        self.page_container.addWidget(self.mysql_db_2)
        self.page_container.addWidget(self.config)
        self.page_container.addWidget(self.config_1)
        # - - -

        self._init_ui()
        # - - -

        self._connect_signal()

    def _init_ui(self):
        self.navigation_bar.unfold_all_navigations()
        # self.navigation_bar.fold_all_navigations()

        self.handler_switch_to_specified_widget(NavigationEnum.mysql_db)

    def _connect_signal(self):
        self.navigation_bar.signal_navigation_item_clicked.connect(self.handler_switch_to_specified_widget)

    @pyqtSlot(object)
    def handler_switch_to_specified_widget(self, identification):
        if identification == NavigationEnum.mysql_db:
            self.page_container.setCurrentWidget(self.mysql_db)

        elif identification == NavigationEnum.mysql_db_1:
            self.page_container.setCurrentWidget(self.mysql_db_1)

        elif identification == NavigationEnum.mysql_db_2:
            self.page_container.setCurrentWidget(self.mysql_db_2)

        elif identification == NavigationEnum.config:
            self.page_container.setCurrentWidget(self.config)

        elif identification == NavigationEnum.config_1:
            self.page_container.setCurrentWidget(self.config_1)


if __name__ == "__main__":
    from pprint import pprint
    from collections import OrderedDict

    app = QApplication(sys.argv)
    items_data = OrderedDict({
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
    })
    pprint(items_data)

    my_widget = MySetting(items_data)
    my_widget.setMinimumSize(600, 400)
    my_widget.setWindowTitle("Settings")

    my_widget.show()
    sys.exit(app.exec_())
