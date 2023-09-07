# -*- coding:utf-8 -*-
import copy
import json
import pandas as pd
import numpy as np

"""
adc中的解析逻辑
"""

# sinf 文件解析后的 json 文件中的 'Origin_DieMap' 字段，晶圆原始数据为ok的晶粒的站位字符
OK_PLACEHOLDER = 'ook'

# 数据库中 AI 和 人工复检 结果为OK的 LAB_CLASS_ID
DB_OK_CLASS_ID = -1

# 客户数据中OK的类的id
META_DATA_OK_CLASS_ID = 0


class MetaAnalysis:
    """
    Wafer元数据解析基类
    """
    _file_url = None  # 需要解析文件的minio地址,传空则使用默认数据
    _data = None  # 元数据
    LotID = "lot001"  # lotid
    SetupID = "setup001"  # setupid
    DeviceID = "device001"  # 设备id
    StepID = "step001"  # stepid
    WaferID = "wafer001"  # 晶圆id
    ProductID = "product001"  # 产品id
    Slot = "1"  # Slot
    DieCount = 0  # 总晶粒数
    defectLocation = []  # 缺陷列表
    DieMap = []  # 晶粒对照图
    Origin_DieMap = []  # 晶粒对照图
    Xdies = 1.0  # 晶粒长/宽比例
    Ydies = 1.0  # 晶粒长/宽比例
    Rowct = 0  # 行数
    Colct = 0  # 列数
    class_data = {}  # 源文件中 缺陷类列表, key：客户的缺陷类名称 value:客户的缺陷类id
    SampleSize = []  # 晶圆尺寸

    def __init__(self, file_url=None):
        # self._file_url = file_url
        # if not self._file_url:
        #     return
        #
        # # 生产代码
        #
        # temp_data = data.data.decode()
        # if "\r\n" in temp_data:
        #     self._data = temp_data.split("\r\n")
        # else:
        #     self._data = temp_data.split("\n")
        # # self._data = data.data.decode().split("\r\n")
        # # - - -
        #
        # # 测试代码
        # # with open(file_url) as f:
        # #     self._data = f.read()
        # #     self._data = self._data.split("\n")
        # # - - -
        self._file_url = file_url
        with open(file_url) as f:
            lines = f.readlines()
            self._data = lines

    def _agg_data(self):
        row_data = []
        data = self.DieMap
        for item in data:
            start_space_count = 0
            end_space_count = 0

            for jtem in item[::-1]:
                # if jtem == "_":
                #     end_space_count += 1
                # elif jtem == "001":
                #     break

                if jtem == "_":
                    end_space_count += 1
                else:
                    break

            for ktem in item:
                # if ktem == "_":
                #     start_space_count += 1
                # elif ktem == "001":
                #     break

                if ktem == "_":
                    start_space_count += 1
                else:
                    break

            if start_space_count == end_space_count:
                space_count = start_space_count
            elif start_space_count > end_space_count:
                space_count = end_space_count
            else:
                space_count = start_space_count

            for i in range(space_count):
                del item[0]
                item.pop()

            row_data.append(item)

        self.DieMap = row_data

    @property
    def file_url(self):
        return self._file_url

    def props(self):
        """
        对象属性转为dict,私有属性不转
        :return:
        """
        pr = {}
        for name in dir(self):
            value = getattr(self, name)
            if not name.startswith('__') and not callable(value) and not name.startswith('_'):
                pr[name] = value
        return pr


class KlarfAnalysis(MetaAnalysis):
    """
    解析鲁道夫 .klarf文件
    """

    def __init__(self, file_url=None):
        super(KlarfAnalysis, self).__init__(file_url)
        if not self._file_url:
            return
        self.__analysis()
        self._agg_data()

    def __analysis(self):
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

            if line.find("SampleSize") != -1:
                self.SampleSize = line[:-1].split(' ')[1:]

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

        if summarylist[0][0] == "":
            temp_summary_start = 1
        else:
            temp_summary_start = 0
        self.__analysis_detects(columnheader, summarylist, temp_summary_start, defectlist)
        self.__analysis_rowct_colct_die_map(samplediemap)

        if (class_data_start_line is not None) and (class_data_end_line is not None):
            class_data_ls = lines[class_data_start_line:class_data_end_line + 1]
            class_data_ls[-1] = class_data_ls[-1].replace(';', '')  # 最后一行有;符号需要删除
            self.__analysis_class_map(class_data_ls)
        else:
            raise ValueError("无法解析晶圆klarf文件中的缺陷类数据")

    def __analysis_detects(self, columnheader, summarylist, temp_summary_start, defectlist):
        """
        解析缺陷列表
        :param columnheader: 表头
        :param summarylist: 统计
        :param temp_summary_start:
        :param defectlist: 缺陷列表
        :return:
        """
        defectheader = columnheader  # 缺陷数据表头
        noofdefectcolumn = len(defectheader)
        noofdefects = 0  # ng图片数
        for k in summarylist:  # 每个testplans的数的和
            noofdefects = noofdefects + int(k[temp_summary_start + 1])  # summarylist第二列数据
        index_defect = -1
        defectlocation_np = []
        """
        将缺陷列表数据转化为dataframe
        """
        values = []
        for index, row in enumerate(defectlist):
            if len(defectlist[index].split(" ")) > 3:
                if defectlist[index].split(" ")[0] == "":
                    temp_defect_start = 1
                else:
                    temp_defect_start = 0
                index_defect = index_defect + 1
                values.extend(row.split(" ")[temp_defect_start:(
                        noofdefectcolumn + temp_defect_start - 1)])
                defectlocation_np.append(values)
                values = []
            else:
                if len(defectlist[index].split(" ")) == 2:  # 图片文件名TiffFileName
                    TiffFileName = defectlist[index].split(" ")[-1].replace(";", "")
                    values.append(TiffFileName)
                else:  # DefectList
                    pass

        self.defectLocation = pd.DataFrame(defectlocation_np, columns=columnheader)

    def __analysis_rowct_colct_die_map(self, samplediemap):
        all_die_xy = []
        for xy in samplediemap:
            x, y = xy.split(" ")
            all_die_xy.append([int(x), int(y)])
        # wafer 的 array 数据，初始化全是 0
        all_die_xy_np = np.reshape(all_die_xy, [-1, 2])

        Xs, Ys = all_die_xy_np[:, 0], all_die_xy_np[:, 1]
        # self.Rowct = int(Xs.max()) + 1
        # self.Colct = int(Ys.max()) + 1
        # xy_array = np.zeros([Xs.max() + 1, Ys.max() + 1], dtype=np.int)
        self.Rowct = int(Ys.max()) + 1  # Y 是 行（最下边是第0行）
        self.Colct = int(Xs.max()) + 1  # X 是 列（最左边是第0列）
        xy_array = np.zeros([self.Rowct, self.Colct], dtype=np.int)  # 全0图像

        # (0，0) 为图像的左下角，所以Y方向的坐标要做上下翻转
        for die_xy in all_die_xy_np:
            # xy_array[int(Xs.max()) - die_xy[0]][int(Ys.max()) - die_xy[1]] = -666
            xy_array[int(Ys.max()) - die_xy[1]][die_xy[0]] = -666  # 晶粒在晶圆图上的行列

        for index, detect_xy in self.defectLocation.iterrows():
            # xy_array[int(Xs.max()) - int(detect_xy["XINDEX"])][int(Ys.max()) - int(detect_xy["YINDEX"])] = int(
            #     detect_xy["CLASSNUMBER"])
            # 有缺陷的晶粒在晶圆图上的行列
            xy_array[int(Ys.max()) - int(detect_xy["YINDEX"])][int(detect_xy["XINDEX"])] = int(detect_xy["CLASSNUMBER"])

        die_map_list = xy_array.tolist()
        for i in die_map_list:  # 将数据中的0变为_,数据中的10变为001，数据中的其他如90变为三位的090
            for j in range(len(i)):
                if i[j] == 0:
                    i[j] = "_"
                # elif i[j] == 10:
                elif i[j] == -666:
                    # i[j] = "001"
                    i[j] = OK_PLACEHOLDER
                else:
                    d = str(i[j])
                    i[j] = "0" * (3 - len(d)) + d
        self.DieMap = die_map_list
        self.Origin_DieMap = copy.deepcopy(die_map_list)
        self.defectLocation = json.loads(
            self.defectLocation[["IMAGENAME", "XINDEX", "YINDEX", "CLASSNUMBER"]]
                .rename(
                columns={
                    "IMAGENAME": "ImageName",
                    "YINDEX": "Row",
                    "XINDEX": "Col",
                    "CLASSNUMBER": "LabClassId",

                }
            ).to_json(orient='records'))

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


if __name__ == '__main__':
    filePath = "./Test_20230816.klarf"
    klarf = KlarfAnalysis(filePath)
    print(f"klarf = {klarf.props()}")
