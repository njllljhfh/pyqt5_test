# -*- coding:utf-8 -*-
# __author__ = "Dragon"

"""实践：chapter35_工厂方法模式_策略模式"""
from enum import Enum, unique
from typing import ClassVar


# from constants import TaskOperType, Gg

# - - - - - - - - - - - 测试用枚举类 - - - - - - - - - - -
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


@unique
class TaskOperType(BaseEnum):
    """任务执行类型 <table: DETECT_TASK_INFO> <field: TASK_OPER_TYPE>"""

    take_picture = 0
    small_auto = 1
    small_file = 2
    small_passiveness = 3
    large_auto = 4
    large_file = 5
    large_passiveness = 6

    @classmethod
    def value_name(cls, value):
        """ Map value to Str. """
        value_map = {
            cls.take_picture.value: "拍照模式",
            cls.small_auto.value: "小图辅助",
            cls.small_file.value: "小图文件夹",
            cls.small_passiveness.value: "全自动控制",  # 拍摄小图，分阶段拼图。改名（20201123）
            cls.large_auto.value: "获取大图",  # 改名（20201109）
            cls.large_file.value: "大图文件夹",
            cls.large_passiveness.value: "接收大图",  # 改名（20201109）
        }
        return value_map.get(value)


@unique
class Gg(BaseEnum):
    """产品信息<table: PRODUCT_INFO> <field: GG> 规格"""
    gg_6_mul_10 = 1
    gg_6_mul_12 = 2
    gg_6_mul_20 = 3
    gg_6_mul_24 = 4
    gg_7_mul_80 = 5
    gg_6_mul_66 = 6
    gg_5_mul_77 = 7
    gg_6_mul_80 = 8

    @classmethod
    def value_name(cls, value):
        """ Map value to Str. """
        value_map = {
            cls.gg_6_mul_10.value: "6*10",
            cls.gg_6_mul_12.value: "6*12",
            cls.gg_6_mul_20.value: "6*20",
            cls.gg_6_mul_24.value: "6*24",
            cls.gg_7_mul_80.value: "7*80",
            cls.gg_6_mul_66.value: "6*66",
            cls.gg_5_mul_77.value: "5*77",
            cls.gg_6_mul_80.value: "6*80",
        }
        return value_map.get(value)

    @classmethod
    def value_name_to_enum_num(cls, value_name: str) -> int:
        """
         Map value_name to enum
        :param value_name: 规格字符串（如："6*10"）
        :return: 规格字符串对应的枚举值
        """
        value_map = {
            cls.value_name(cls.gg_6_mul_10.value): cls.gg_6_mul_10.value,
            cls.value_name(cls.gg_6_mul_12.value): cls.gg_6_mul_12.value,
            cls.value_name(cls.gg_6_mul_20.value): cls.gg_6_mul_20.value,
            cls.value_name(cls.gg_6_mul_24.value): cls.gg_6_mul_24.value,
            cls.value_name(cls.gg_7_mul_80.value): cls.gg_7_mul_80.value,
            cls.value_name(cls.gg_6_mul_66.value): cls.gg_6_mul_66.value,
            cls.value_name(cls.gg_5_mul_77.value): cls.gg_5_mul_77.value,
            cls.value_name(cls.gg_6_mul_80.value): cls.gg_6_mul_80.value,
        }
        return value_map.get(value_name)


# - - - - - - - - - - - - - - - - - - - - - - - - - - -
class TpStrategy(object):
    """TP策略接口"""
    _STRATEGY_NAME = "TpStrategy"

    def __init__(self, row: int, column: int):
        """
        :param row: 总行数
        :param column: 总列数
        """
        self.tp_count = 0  # 总TP数
        self.last_tp_name = ""  # 最后一个TP的名称
        self.row = row  # 整图的总行数
        self.column = column  # 整图的总列数
        self.map_tp_to_scale = dict()  # <type:dict> 每个TP阶段对应的总行数、总列数

    def get_current_scale(self, tp_num: int) -> [int, int]:
        """
        获取当前TP阶段的总行数、列数
        :param tp_num: 要获取的TP阶段
        :return: 当前阶段的总行数、总列数
        """
        if tp_num <= 0 or tp_num > self.tp_count:
            raise ValueError(f"TP{tp_num}阶段超出超出支持的TP范围（TP1-TP{self.tp_count}）。")
        return self.map_tp_to_scale[f"TP{tp_num}"]

    @classmethod
    def strategy_name(cls):
        return cls._STRATEGY_NAME


class Tp1RowAll(TpStrategy):
    """策略：总共1个TP"""
    _STRATEGY_NAME = "Tp1RowAll"

    def __init__(self, row, column):
        super().__init__(row, column)
        self.tp_count = 1
        self.last_tp_name = f"TP{self.tp_count}"
        self.row = row
        self.map_tp_to_scale = {
            "TP1": [self.row, self.column],
        }


class Tp3Row5(TpStrategy):
    """策略：总共3个TP，总共5行，每2行1个TP"""
    _STRATEGY_NAME = "Tp3Row5"

    def __init__(self, row, column):
        super().__init__(row, column)
        self.tp_count = 3
        self.last_tp_name = f"TP{self.tp_count}"
        self.row = 5
        self.map_tp_to_scale = {
            "TP1": [2, self.column],
            "TP2": [4, self.column],
            "TP3": [self.row, self.column],
        }


class Tp3Row6(TpStrategy):
    """策略：总共3个TP，总共6行，每2行1个TP"""
    _STRATEGY_NAME = "Tp3Row6"

    def __init__(self, row, column):
        super().__init__(row, column)
        self.tp_count = 3
        self.last_tp_name = f"TP{self.tp_count}"
        self.row = 6
        self.map_tp_to_scale = {
            "TP1": [2, self.column],
            "TP2": [4, self.column],
            "TP3": [self.row, self.column],
        }


class Tp4Row7(TpStrategy):
    """策略：总共4个TP，总共7行，每2行1个TP"""
    _STRATEGY_NAME = "Tp4Row7"

    def __init__(self, row, column):
        super().__init__(row, column)
        self.tp_count = 4
        self.last_tp_name = f"TP{self.tp_count}"
        self.row = 7
        self.map_tp_to_scale = {
            "TP1": [2, self.column],
            "TP2": [4, self.column],
            "TP3": [6, self.column],
            "TP4": [self.row, self.column],
        }


@unique
class StrategyEnum(Enum):
    """TP策略枚举"""
    Tp1RowAll = Tp1RowAll
    Tp3Row5 = Tp3Row5
    Tp3Row6 = Tp3Row6
    Tp4Row7 = Tp4Row7

    @classmethod
    def name_to_strategy(cls, name: str) -> ClassVar[TpStrategy]:
        """
        映射：名字 ---> 策略类
        :param name: 策略类名称
        :return: 策略类（class TpStrategy 的实现类）
        """
        map_name_to_strategy = {
            Tp1RowAll.__name__: cls.Tp1RowAll.value,
            Tp3Row5.__name__: cls.Tp3Row5.value,
            Tp3Row6.__name__: cls.Tp3Row6.value,
            Tp4Row7.__name__: cls.Tp4Row7.value,
        }
        if name not in map_name_to_strategy:
            raise KeyError(f'不存在名称为"{name}"的TP策略。')
        return map_name_to_strategy.get(name)


class TpStrategyFactory(object):
    """TP策略工厂"""

    @classmethod
    def get_tp_strategy(cls, strategy_name: str, row: int, column: int):
        """生成TP策略实例"""
        strategy_class = StrategyEnum.name_to_strategy(strategy_name)
        strategy = strategy_class(row, column)
        return strategy


class TpStrategyContext(object):
    """TP策略封装"""

    def __init__(self, tp_strategy: TpStrategy):
        """
        :param tp_strategy: 接口 TpStrategy 的实现类的对象
        """
        self.tp_strategy = tp_strategy

    def get_current_scale(self, tp_num: int) -> [int, int]:
        return self.tp_strategy.get_current_scale(tp_num)


class TpStrategyFacade(object):
    """TP策略-门面"""

    def __init__(self, tp_strategy_name, row, column):
        try:
            # TP策略对象
            tp_strategy = TpStrategyFactory.get_tp_strategy(tp_strategy_name, row, column)
            # TP策略上下文
            self._tp_strategy_context = TpStrategyContext(tp_strategy)
        except Exception as e:
            raise e

    def get_current_scale(self, tp_num: int) -> [int, int]:
        return self._tp_strategy_context.tp_strategy.get_current_scale(tp_num)

    @property
    def tp_count(self):
        return self._tp_strategy_context.tp_strategy.tp_count

    @property
    def row(self):
        return self._tp_strategy_context.tp_strategy.row

    @property
    def column(self):
        return self._tp_strategy_context.tp_strategy.column

    @property
    def strategy_name(self):
        return self._tp_strategy_context.tp_strategy.strategy_name()

    @property
    def last_tp_name(self):
        return self._tp_strategy_context.tp_strategy.last_tp_name


def get_tp_strategy_name(task_oper_type: int, gg: int) -> str:
    """
    根据任务类型和产品规格，获取TP策略
    :param task_oper_type: 任务类型
    :param gg: 产品规格
    :return: TP策略类的名称
    """
    if task_oper_type in [TaskOperType.small_auto.value,
                          TaskOperType.small_file.value,
                          TaskOperType.small_passiveness.value]:
        if gg in [Gg.gg_6_mul_10.value, Gg.gg_6_mul_12.value, Gg.gg_6_mul_20.value,
                  Gg.gg_6_mul_24.value, Gg.gg_6_mul_66.value, Gg.gg_6_mul_80.value]:
            tp_strategy_name = Tp3Row6.__name__
        elif gg in [Gg.gg_7_mul_80.value]:
            tp_strategy_name = Tp4Row7.__name__
        elif gg in [Gg.gg_5_mul_77.value]:
            tp_strategy_name = Tp3Row5.__name__
        else:
            raise ValueError(f'产品规格错误"{gg}"')
    elif task_oper_type in [TaskOperType.large_auto.value,
                            TaskOperType.large_file.value,
                            TaskOperType.large_passiveness.value]:
        tp_strategy_name = Tp1RowAll.__name__
    else:
        raise ValueError(f'任务类型错误"{task_oper_type}"')
    return tp_strategy_name


if __name__ == '__main__':
    # task_oper_type_ = TaskOperType.small_passiveness.value
    task_oper_type_ = TaskOperType.large_passiveness.value

    gg_enum_ = Gg.gg_7_mul_80.value
    # task_oper_type_ = Gg.gg_5_mul_77.value

    gg_str_: str = Gg.value_name(gg_enum_)
    row_, column_ = [int(num) for num in gg_str_.split("*")]

    strategy_name_ = get_tp_strategy_name(task_oper_type_, gg_enum_)
    tp_strategy_facade = TpStrategyFacade(strategy_name_, row_, column_)
    print(f"TP策略名称：{tp_strategy_facade.strategy_name}")
    print(f"TP策略最后一个TP的名称：{tp_strategy_facade.last_tp_name}")
    current_tp_num = 1
    print(f"TP{current_tp_num}: row_column={tp_strategy_facade.get_current_scale(current_tp_num)}")
