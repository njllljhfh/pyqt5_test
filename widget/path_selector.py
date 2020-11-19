# -*- coding:utf-8 -*-
import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QFileDialog, QPushButton, QApplication, QWidget, QLineEdit, QHBoxLayout, QLabel, QGridLayout


class PathSelectionLineEdit(QLineEdit):
    """文件夹路径选择QLineEdit"""

    def __init__(self, *args, parent=None):
        super().__init__(parent, *args)
        self.setFocusPolicy(Qt.NoFocus)
        self.file_dialog = PathSelectionWidget(parent=parent)

    def mousePressEvent(self, QMouseEvent):
        try:
            old_path = self.text()
            path = self.file_dialog.getExistingDirectory()
            if path:
                self.setText(path)
            else:
                self.setText(old_path)
        except Exception as e:
            print(f"Error:{e}")


class PathSelectionWidget(QFileDialog):
    """文件夹路径选择"""

    def __init__(self, *args, parent=None):
        super().__init__(parent, *args)


class CopyWidget(QWidget):
    def __init__(self, *args, parent=None):
        super().__init__(parent, *args)
        # 文件夹路径选择
        layout = QGridLayout(self)

        self.layout_source_path = QHBoxLayout()
        self.layout_source_path.setSpacing(6)
        self.layout_source_path.setObjectName("layout_source_path")
        # Label
        self.label_source_path = QLabel(parent)
        self.label_source_path.setObjectName("path_selection_label")
        self.label_source_path.setText("源文件目录：")
        self.label_source_path.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_source_path.setMinimumSize(QSize(90, 20))
        self.label_source_path.setMaximumSize(QSize(90, 20))
        # PathSelectionLineEdit
        self.line_edit_source_path = PathSelectionLineEdit(parent)
        self.line_edit_source_path.setObjectName("line_edit_source_path")
        self.line_edit_source_path.setMaximumSize(QSize(16777215, 20))
        self.line_edit_source_path.setPlaceholderText("请选源文件目录")
        self.layout_source_path.addWidget(self.label_source_path)
        self.layout_source_path.addWidget(self.line_edit_source_path)
        layout.addLayout(self.layout_source_path, 0, 0, 1, 1)

        # - - - -
        self.layout_target_path = QHBoxLayout()
        self.layout_target_path.setSpacing(6)
        self.layout_target_path.setObjectName("layout_target_path")
        # Label
        self.label_target_path = QLabel(parent)
        self.label_target_path.setObjectName("label_target_path")
        self.label_target_path.setText("目标文件目录：")
        self.label_target_path.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_target_path.setMinimumSize(QSize(90, 20))
        self.label_target_path.setMaximumSize(QSize(90, 20))
        # PathSelectionLineEdit
        self.line_edit_target_path = PathSelectionLineEdit(parent)
        self.line_edit_target_path.setObjectName("line_edit_target_path")
        self.line_edit_target_path.setMaximumSize(QSize(16777215, 20))
        self.line_edit_target_path.setPlaceholderText("请选择目标文件目录")
        self.layout_target_path.addWidget(self.label_target_path)
        self.layout_target_path.addWidget(self.line_edit_target_path)
        layout.addLayout(self.layout_target_path, 1, 0, 1, 1)

        # 拷贝按钮
        self.copy_btn = QPushButton(self)
        self.copy_btn.setText("拷贝")
        layout.addWidget(self.copy_btn, 2, 0, 1, 1)
        self.copy_btn.clicked.connect(self.event_copy_btn_clicked)

        self.resize(800, 80)

    def event_copy_btn_clicked(self):
        source_path = self.line_edit_source_path.text()
        target_path = self.line_edit_target_path.text()
        print(f"source_path: {source_path}")
        print(f"target_path: {target_path}")
        # TODO: copy code.
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    my_widget = CopyWidget()
    my_widget.show()

    sys.exit(app.exec_())
