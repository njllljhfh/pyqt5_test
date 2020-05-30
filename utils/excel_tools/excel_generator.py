# -*- coding:utf-8 -*-
import xlsxwriter

# Create an new Excel file and add a worksheet.
from xlsxwriter.worksheet import Worksheet


def xxx():
    workbook = xlsxwriter.Workbook('demo.xlsx')
    worksheet = workbook.add_worksheet("表1")
    # worksheet2 = workbook.add_worksheet("表2")

    # Widen the first column to make the text clearer.
    # worksheet.set_column('A:A', 20)
    worksheet.set_column(0, 0, 20)

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})

    # Write some simple text.
    # worksheet.write('A1', 'Hello')
    worksheet.write(0, 0, 'Hello')

    # Text with formatting.
    worksheet.write(1, 0, 'World', bold)

    # Write some numbers, with row/column notation.
    worksheet.write(2, 0, 123)
    worksheet.write(3, 0, 123.456)

    # Insert an image.
    worksheet.insert_image('B5', 'img_拓海_1.png')

    workbook.close()


# xxx()


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

    def _create_file(self, file_name: str):
        """创建excel文件"""
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
        :param table_header: 表头
        :param sheet: 表对象
        :return:
        """

        column_width = 30
        # 写表头
        with self.workbook:
            for column, header in enumerate(table_header):
                sheet.set_column(0, column, column_width)
                sheet.write(0, column, header, self.header_format)


if __name__ == '__main__':
    file_name = "统计表.xlsx"
    excel_manager = ExcelManager(file_name)

    sheet_name = "sheet_1"
    sheet_1 = excel_manager.create_sheet(sheet_name)

    table_header = ["序号", "模块", "子模块", "功能", "子功能", "功能描述"]
    excel_manager.generate_statistics_sheet(sheet_1, table_header)
