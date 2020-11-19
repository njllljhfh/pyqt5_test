# -*- coding:utf-8 -*-
import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QButtonGroup, QPushButton, QHBoxLayout, QApplication


class SwitchBtnGroup(QWidget):
    """切换按钮组"""
    signal_btn_a_clicked = pyqtSignal(bool)
    signal_btn_b_clicked = pyqtSignal(bool)

    def __init__(self, *args, parent=None, text_btn_a: str = "EL", text_btn_b: str = "VI"):
        super().__init__(parent, *args)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.button_group = QButtonGroup(self)
        self.button_group.setObjectName("button_group")

        self.btn_a = SwitchBtn(parent=self)
        self.btn_a.setObjectName("btn_a")
        self.btn_a.setText(text_btn_a or "EL")
        self.button_group.addButton(self.btn_a)
        layout.addWidget(self.btn_a)

        self.btn_b = SwitchBtn(parent=self)
        self.btn_b.setObjectName("btn_b")
        self.btn_b.setText(text_btn_b or "VI")
        self.button_group.addButton(self.btn_b)
        layout.addWidget(self.btn_b)

        self.btn_a.clicked.connect(self.signal_btn_a_clicked)
        self.btn_b.clicked.connect(self.signal_btn_b_clicked)


class SwitchBtn(QPushButton):
    """单个切换按钮"""

    def __init__(self, *args, parent=None):
        super().__init__(parent, *args)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)


if __name__ == '__main__':
    # 测试代码
    class MyTestWidget(QWidget):

        def __init__(self, *args, parent=None):
            super().__init__(parent, *args)

            layout = QHBoxLayout(self)
            # layout.setContentsMargins(0, 0, 0, 0)
            # layout.setSpacing(0)

            self.switch_btn_group = SwitchBtnGroup(parent=self)
            layout.addWidget(self.switch_btn_group)

            self.setStyleSheet("""
            SwitchBtnGroup SwitchBtn{
              background-color: rgb(27, 27, 27);
              color: rgb(255, 255, 255);
              border: 1px solid rgb(121, 121, 121);
              width: 65px;
              height: 30px;
            }

            SwitchBtnGroup SwitchBtn:checked {
              background-color: rgb(25, 151, 253);
            }
            """)

            self.switch_btn_group.signal_btn_a_clicked.connect(self.btn_el_clicked_event)
            self.switch_btn_group.signal_btn_b_clicked.connect(self.btn_vi_clicked_event)

        def btn_el_clicked_event(self, checked):
            print(f"btn_el_clicked_event---checked = {checked}")
            pass

        def btn_vi_clicked_event(self, checked):
            print(f"btn_vi_clicked_event---checked = {checked}")
            pass


    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    app = QApplication(sys.argv)

    # - - -
    my_widget = MyTestWidget()
    # - - -

    my_widget.show()
    sys.exit(app.exec_())
