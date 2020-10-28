# -*- coding:utf-8 -*-
import sys
from enum import Enum, unique
from PyQt5.QtCore import QTimer, Qt, QPoint, QEvent
from PyQt5.QtGui import QPaintEvent, QMoveEvent
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QPushButton, QLabel


@unique
class TipDirection(Enum):
    """信息提示框放置的方向"""
    left = 0
    top = 1
    right = 2
    bottom = 3

    @classmethod
    def value_name(cls, value):
        """ Map value to Str. """
        value_map = {
            cls.left.value: "左",
            cls.top.value: "上",
            cls.right.value: "右",
            cls.bottom.value: "下",
        }
        return value_map.get(value)

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


class CopyBtn(QPushButton):
    """复制按钮中的内容"""

    def __init__(self, *args, parent=None, tip_text=None, empty_tip_text=None, empty_flag="",
                 tip_display_time=1.5, tip_offset=10, tip_direction: int = 2):
        """
        :param args:
        :param parent: 父级实例
        :param tip_text: 提示信息
        :param tip_display_time: 提示信息显示时间（s）
        :param tip_offset: 提示信息偏移量
        :param empty_flag: 无数据时的字符
        :param tip_direction: 信息提示框放置的方向（默认放在按钮右侧，其他位置见枚举类 TipDirection）
        """
        super().__init__(parent, *args)

        self._empty_flag = empty_flag
        self.data = self._empty_flag  # 保存的数据(如：产品条码)
        self.tip_text = tip_text if tip_text is not None else "已复制，请去粘贴使用"
        self.empty_tip_text = empty_tip_text if empty_tip_text is not None else "无数据可复制，请稍后"
        self.tip_offset = tip_offset
        self.tip_direction = 2  # 右侧
        self.set_tip_direction(tip_direction)

        # 时间间隔(秒)
        self.tip_display_time = tip_display_time

        # 提示信息框
        self.tip_widget = TipQWidget()  # 不要设置父类
        self.tip_widget.setObjectName("tip_widget")
        self.tip_widget.hide()
        qss = """
        TipQWidget QLabel{
            color: rgb(255, 255, 255);
            background-color: rgb(100, 100, 100);
            border-radius: 6px;
        }
        """
        self.tip_widget.setStyleSheet(qss)

        # 事件绑定
        self.clicked.connect(self.clicked_event)

        # 定时器
        self.tip_timer = QTimer()
        self.tip_timer.setInterval(self.tip_display_time * 1000)  # 时间间隔换算为:秒
        self.tip_timer.setTimerType(Qt.PreciseTimer)
        self.tip_timer.timeout.connect(self.tip_timer_time_out_event)

    def set_tip_fixed_size(self, width, height):
        """设置信息提示框宽高"""
        self.tip_widget.setFixedSize(width, height)

    def set_tip_display_time(self, tip_display_time):
        """设置信息提示框显示时间"""
        self.tip_display_time = float(tip_display_time)
        self.tip_timer.setInterval(self.tip_display_time * 1000)  # 时间间隔换算为:秒

    def set_tip_direction(self, tip_direction: int):
        """设置信息提示框放置的方向"""
        if TipDirection.value_exists(tip_direction):
            self.tip_direction = tip_direction
        else:
            raise ValueError(f"信息提示框放置的方向(tip_direction)设置错误，支持的值为{TipDirection.value_list()}")

    def set_tip_offset(self, tip_offset):
        """设置信息提示框偏移量(即：与按钮之间的间距)"""
        self.tip_offset = float(tip_offset)

    def clicked_event(self):
        """点击事件"""
        try:
            # 系统剪切板
            clipboard = QApplication.clipboard()  # 获取系统剪贴板指针
            clipboard.setText(str(self.data))  # 设置剪贴板文本信息
            # clipboard_text = clipboard.text()  # 获取剪贴板上文本信息

            if self.data != self._empty_flag:
                massage = self.tip_text
            else:
                massage = self.empty_tip_text

            # 计算提示框位置
            tip_pos = self.calculate_tip_pos()
            self.tip_widget.show_tip(massage, tip_pos.x(), tip_pos.y())

            self.tip_timer.start()
        except Exception as e:
            print(f"error = {e}")
            raise

    def calculate_tip_pos(self) -> QPoint:
        """计算信息提示框位置"""
        global_pos = self.mapToGlobal(QPoint(0, 0))  # map到屏幕的全局坐标
        if self.tip_direction == TipDirection.left.value:
            tip_pos = QPoint(global_pos.x() - self.tip_offset - self.tip_widget.width(),
                             global_pos.y() + (self.height() - self.tip_widget.height()) / 2)
        elif self.tip_direction == TipDirection.top.value:
            tip_pos = QPoint(global_pos.x() + (self.width() - self.tip_widget.width()) / 2,
                             global_pos.y() - self.tip_widget.height() - self.tip_offset)
        elif self.tip_direction == TipDirection.right.value:
            tip_pos = QPoint(global_pos.x() + self.tip_offset + self.width(),
                             global_pos.y() + (self.height() - self.tip_widget.height()) / 2)
        else:
            tip_pos = QPoint(global_pos.x() + (self.width() - self.tip_widget.width()) / 2,
                             global_pos.y() + self.height() + self.tip_offset)
        return tip_pos

    def tip_timer_time_out_event(self):
        if self.tip_widget.isVisible():
            self.tip_widget.hide()
            self.tip_timer.stop()

    def update_data(self, data: str = ""):
        """
        更新数据
        :param data: 按钮保存的数据
        :return: None
        """
        self.data = data

    def clear_data(self):
        """清空保存的数据"""
        self.data = self._empty_flag
        self.tip_timer_time_out_event()

    def paintEvent(self, event: QPaintEvent):
        print(f"{self.objectName()} --- paintEvent")
        # 移动信息提示框
        self.move_tip_widget()
        super().paintEvent(event)

    def move_tip_widget(self):
        """移动信息提示框"""
        try:
            tip_pos = self.calculate_tip_pos()
            # print(f"{self.objectName()} --- move_tip_widget")
            self.tip_widget.move(tip_pos.x(), tip_pos.y())
        except Exception as e:
            print(f"e = {e}")
            raise


class TipQWidget(QWidget):

    def __init__(self, *args, parent=None):
        super().__init__(parent, *args)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)  # 无边框、置顶、任务栏不显示
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置为透明

        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.msg_label = QLabel(self)
        self.msg_label.setObjectName("msg_label")
        self.msg_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.addWidget(self.msg_label)

    def show_tip(self, massage: str, x, y):
        """
        显示提示信息
        :param massage: 提示信息
        :param x: 相对于父类的横坐标
        :param y: 相对于父类的纵坐标
        :return:
        """
        self.msg_label.setText(str(massage))
        self.setGeometry(x, y, self.width(), self.height())
        self.show()


if __name__ == '__main__':
    QSS = """
    MyWidget {
    background-color: rgb(54, 54, 54);
    }
    
    CopyBtn {
      color: rgb(0, 0, 0);
      border: none;
      border-radius: 6px;
      padding: 10px;
      min-width: 80px;
      background-color: rgb(102, 187, 106);
    }
    """


    class MyWidget(QWidget):

        def __init__(self, *args):
            super().__init__(*args)

            layout = QHBoxLayout(self)
            layout.setSpacing(10)
            self.product_code_copy_btn = CopyBtn(tip_direction=2, tip_display_time=15, parent=self)
            # self.product_code_copy_btn.set_tip_direction(0)
            # self.product_code_copy_btn.set_tip_offset(3)
            # self.product_code_copy_btn.set_tip_display_time(3)
            self.product_code_copy_btn.setObjectName("copy_product_code_btn")
            self.product_code_copy_btn.setText("复制条码")
            # self.product_code_copy_btn.setFixedSize(120, 500)
            layout.addWidget(self.product_code_copy_btn)

            self.product_code_copy_btn.set_tip_fixed_size(170, 40)

            # 测试用的站位按钮1
            self.btn1 = QPushButton("测试用的站位按钮1")
            layout.addWidget(self.btn1)

            # 更新产品条码
            self.product_code_copy_btn.update_data(data="11930200010000123456801")

            self.setStyleSheet(QSS)

        def closeEvent(self, event):
            try:
                self.product_code_copy_btn.clear_data()
                print("closeEvent")
            except Exception as error:
                print(f'error = {error}')
                raise

        def moveEvent(self, event: QMoveEvent):
            # 窗口移动时，强制刷新
            # print(f"{self.objectName()} --- moveEvent")
            self.product_code_copy_btn.update()


    app = QApplication(sys.argv)
    win = MyWidget()
    win.setObjectName("MyWidget")
    win.show()
    sys.exit(app.exec_())
