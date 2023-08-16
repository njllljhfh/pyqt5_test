# -*- coding:utf-8 -*-
import json

import cv2
import math
import numpy as np


class KlarfAnalysis(object):
    """
    解析鲁道夫 .klarf文件
    """

    def __init__(self, filePath, leftTop=True):
        with open(filePath) as f:
            lines = f.readlines()
        self._data = lines
        self.leftTop = leftTop  # True:左上角是原点, False:左下角是原点
        self.class_data = {}

    def analysis(self):
        columnheader = []
        summaryliststartline = 0
        samplediemapendline = 0
        samplediemapstartline = 0
        lines = []
        count = 0
        defectdatastartline = 0
        defectdataendline = 0
        testplans = 0
        class_data_start_line = None
        class_data_end_line = None
        for line in self._data:
            if line.find("LotID") != -1:
                # LotID = line[7:-3]
                LotID = line.split('"')[1]
                self.LotID = LotID
            if line.find("SetupID") != -1:
                # SetupID = line[9:-23]
                SetupID = line.split('"')[1]
                self.SetupID = SetupID
            if line.find("DeviceID") != -1:
                # DeviceID = line[10:-3]
                DeviceID = line.split('"')[1]
                self.DeviceID = DeviceID
            if line.find("StepID") != -1:
                # StepID = line[8:-3]
                StepID = line.split('"')[1]
                self.StepID = StepID
            if line.find("WaferID") != -1:
                WaferID = line[9:-2]
                self.WaferID = WaferID
            if line.find("Slot") != -1:
                Slot = line[5:-1]
                self.Slot = Slot
            if line.find("SampleDieMap") != -1:
                DieCount = int(line[13:])
                self.DieCount = DieCount
                samplediemapstartline = count + 1
                samplediemapendline = samplediemapstartline + DieCount
                class_data_end_line = count - 1  # 缺陷类数据结束-行号
            if line.find("InspectionTest") != -1:  # testplans
                testplans = testplans + 1

            if line.find("DefectRecordSpec") != -1:
                columnheader = line[20:-1].split(" ")  # 表头字段
                columnheader.insert(0, "IMAGENAME")
                defectdatastartline = count - 1  # 缺陷数据开始位置-行数

            if line.find("SummarySpec") != -1:
                defectdataendline = count - 1  # 缺陷数据结束位置-行数
                line = line.replace(";", "")

            if line.find("SummaryList") != -1:
                summaryliststartline = count + 1  # 统计数据开始位置-行数

            if line.find("DiePitch") != -1:  # 晶粒长宽比例
                pitch = line[9:-1].split(" ")
                X_DIES = pitch[1]
                Y_DIES = pitch[0]
                self.Xdies = X_DIES
                self.Ydies = Y_DIES
            if line.find('ClassLookup') != -1:
                class_data_start_line = count + 1  # 缺陷类数据开始位置-行号
            lines.append(line.rstrip("\n"))  # 删除每一行最后的回车符，并推进lines列表中
            count = count + 1

        if not self.SetupID.endswith(self.DeviceID):
            self.SetupID = self.SetupID + '-' + self.DeviceID

        defectlist = lines[defectdatastartline:defectdataendline + 1]  # 所有的缺陷数据
        defectlist.pop(1)  # 表头与第一个文件名错位 需要单独处理
        defectlist[-1] = defectlist[-1].replace(';', '')  # 最后一行有;符号需要删除
        summarylist = [i.replace(';', '').split(" ") for i in
                       lines[summaryliststartline:summaryliststartline + testplans]]  # 统计数据每个testplans都是一行
        samplediemap = lines[samplediemapstartline:samplediemapendline]
        samplediemap[-1] = samplediemap[-1].replace(';', '')  # 最后一行有;符号需要删除

        self.__analysis_rowct_colct_die_map(samplediemap)

        if (class_data_start_line is not None) and (class_data_end_line is not None):
            class_data_ls = lines[class_data_start_line:class_data_end_line + 1]
            class_data_ls[-1] = class_data_ls[-1].replace(';', '')  # 最后一行有;符号需要删除
            self.__analysis_class_map(class_data_ls)
        else:
            raise ValueError("无法解析晶圆klarf文件中的缺陷类数据")

    def __analysis_rowct_colct_die_map(self, samplediemap):
        all_die_xy = []
        for xy in samplediemap:
            x, y = xy.split(" ")
            all_die_xy.append([int(x), int(y)])
        # wafer 的 array 数据，初始化全是 0
        all_die_xy_np = np.reshape(all_die_xy, [-1, 2])

        Xs, Ys = all_die_xy_np[:, 0], all_die_xy_np[:, 1]
        self.Rowct = int(Ys.max()) + 1  # Y 是 行（最下边是第0行）
        self.Colct = int(Xs.max()) + 1  # X 是 列（最左边是第0列）
        # xy_array = np.zeros([self.Rowct, self.Colct], dtype=np.int)  # 全0图像
        print(f"self.Rowct={self.Rowct}, self.Colct={self.Colct}")

        scale = self.Colct / self.Rowct
        print(f"scale={scale}")

        die_width = 4
        # die_height = math.ceil(die_width * scale)
        die_height = 4
        print(f"die_width={die_width}, die_height={die_height}")
        grid_line_width: int = 2
        all_height = self.Rowct * die_height + (self.Rowct - 1) * grid_line_width
        all_width = self.Colct * die_width + (self.Colct - 1) * grid_line_width

        # xy_array = np.zeros((self.Rowct, self.Colct, 3), np.uint8)
        xy_array = np.zeros((all_height, all_width, 3), np.uint8)
        xy_array[:, :] = [255, 255, 255]

        # 不反转坐标系
        for die_xy in all_die_xy_np:
            # xy_array[int(Xs.max()) - die_xy[0]][int(Ys.max()) - die_xy[1]] = -666
            # xy_array[die_xy[1]][die_xy[0]] = [255, 0, 0]   # 晶粒在晶圆图上的行列

            if self.leftTop:
                row = die_xy[1]
            else:
                row = int(Ys.max() - die_xy[1])
            column = die_xy[0]
            start_row = row * (grid_line_width + die_height)
            end_row = start_row + die_height
            start_column = column * (grid_line_width + die_width)
            end_column = start_column + die_width

            xy_array[start_row:end_row, start_column:end_column] = [255, 0, 0]

        # 拉伸
        shape = xy_array.shape
        print(f"shape={shape}")
        side_len = max(shape[0], shape[1])
        xy_array = cv2.resize(xy_array, (side_len, side_len))

        # 取值范围：0-100，数值越小，压缩比越高，图片质量损失越严重
        img_encode = cv2.imencode(".jpg", xy_array, [cv2.IMWRITE_JPEG_QUALITY, 100])

        # 取值范围：0-9，数值越小，压缩比越低，图片质量越高
        # img_encode = cv2.imencode(".png", img_np, [cv2.IMWRITE_PNG_COMPRESSION, 0])

        img_bytes = img_encode[1].tobytes()
        with open("./waferMap.jpg", "wb") as f:
            f.write(img_bytes)

        cv2.imshow('img', xy_array)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def __analysis_class_map(self, class_ls: list):
        """
        解析缺陷类数据
        :param class_ls: 缺陷类数据列表
        :return: None
        """
        for class_line in class_ls:
            class_id, class_name = class_line.split(' ', maxsplit=1)
            class_id = int(class_id)
            class_name = class_name.strip('"')
            self.class_data[class_name] = class_id

    def classIDTOHex(self):
        """将classId转为16进制"""
        classData = {}
        for className, classId in self.class_data.items():
            classData[self._dec_to_hex(str(classId))] = className
        return classData

    def _dec_to_hex(self, num_str: str):
        """
        十进制转十六进制 左侧补0
        :param num_str:
        :return:
        """
        if num_str.count('0') == len(num_str):
            num = 0
        else:
            num = int(num_str.lstrip('0'))
        hex_str = hex(num)[2:]
        hex_str = '0' + hex_str if len(hex_str) < 2 else hex_str
        return hex_str


if __name__ == '__main__':
    # 此klarf中的die信息是以【左上角】为原点给的坐标数据
    # filePath = "./1683894545.227089_dbdfj_01_dbdfj_01.klarf"
    filePath = "./Test.klarf"
    # filePath = "./Test_20230816.klarf"
    klarf = KlarfAnalysis(filePath, leftTop=True)
    # klarf = KlarfAnalysis(filePath, leftTop=False)
    klarf.analysis()
    print(" - - - - - - - - - - - -- - ")

    print(klarf.class_data)
    print(" - - - - - - - - - - - -- - ")

    hexIdTOClassName = klarf.classIDTOHex()
    print(hexIdTOClassName)
    print(" - - - - - - - - - - - -- - ")
    # 生成json文件
    jsonData = json.dumps(hexIdTOClassName)
    with open("./hexIdToClassName.json", "w") as f:
        f.write(jsonData)
