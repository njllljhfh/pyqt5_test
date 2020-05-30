# -*- coding:utf-8 -*-
import xlsxwriter

# Create an new Excel file and add a worksheet.
from xlsxwriter.worksheet import Worksheet


class ExcelManager(object):
    """创建excel文件"""

    def __init__(self, file_name="统计表.xlsx"):
        self.workbook = None  # Excel file
        self._create_file(file_name)
        # 水平，竖直居中
        self.header_format = self.workbook.add_format(
            {
                'align': 'center',
                'valign': 'vcenter',
                'border': 1,
                'bold': True,
            }
        )

    def __enter__(self):
        """Return self object to use with "with" statement."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close workbook when exiting "with" statement."""
        self.close()

    def close(self):
        """关闭workbook"""
        self.workbook.close()

    def _create_file(self, file_name: str):
        """
        创建excel文件
        :param file_name: 文件名称（如：“统计表.xlsx”）
        :return:
        """
        # Create an new Excel file and add a worksheet.
        self.workbook = xlsxwriter.Workbook(file_name)

    def create_sheet(self, name: str):
        """
        新建并返回一个sheet
        :param name: sheet名称
        :return: Worksheet
        """
        return self.workbook.add_worksheet(name)

    def generate_statistics_sheet(self, sheet: Worksheet, table_header: list):
        """
        生成统计表
        :param sheet: 表对象
        :param table_header: 表头
        :return:
        """
        column_width = 30
        # 写表头
        for column, header in enumerate(table_header):
            sheet.set_column(0, column, column_width)
            sheet.write(0, column, header, self.header_format)


if __name__ == '__main__':
    file_name_a = "统计表.xlsx"

    with ExcelManager(file_name_a) as excel_manager:
        sheet_name_1 = "sheet_1"
        sheet_1 = excel_manager.create_sheet(sheet_name_1)
        table_header_1 = ["序号", "模块", "子模块", "功能", "子功能", "功能描述"]
        excel_manager.generate_statistics_sheet(sheet_1, table_header_1)

        sheet_name_2 = "sheet_2"
        sheet_2 = excel_manager.create_sheet(sheet_name_2)
        table_header_2 = ["序号2", "模块2", "子模块2", "功能2", "子功能2", "功能描述2"]
        excel_manager.generate_statistics_sheet(sheet_2, table_header_2)
