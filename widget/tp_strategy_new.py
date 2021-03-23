# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
# __author__ = "Dragon"

from enum import Enum, unique
from typing import ClassVar
from constants import TaskOperType, Gg

# 数据类型
typeScale = [int, int]  # tp阶段的标尺规格


class ITpStrategy(object):
    """TP策略接口"""

    def __init__(self, row: int, column: int, every_row_num: int = None):
        """
        :param row: 总行数
        :param column: 总列数
        """
        self.tp_count = 0  # 总TP数
        self.last_tp_name = ""  # 最后一个TP的名称
        self.row = row  # 整图的总行数
        self.column = column  # 整图的总列数
        self.map_tp_to_scale: {str: typeScale} = dict()  # 每个TP阶段对应的总行数、总列数
        self._generate_tp_scale(every_row_num)

    def _generate_tp_scale(self, every_row_num):
        """
        生成各个tp对应的行数
        :param every_row_num: 每TP显示几行
        :return:
        """
        pass

    def get_current_scale(self, tp_num: int) -> typeScale:
        """
        获取当前TP阶段的总行数、列数
        :param tp_num: 要获取的TP阶段
        :return: 当前阶段的总行数、总列数
        """
        if tp_num <= 0 or tp_num > self.tp_count:
            raise ValueError(f"TP{tp_num}阶段超出超出支持的TP范围（TP1-TP{self.tp_count}）。")
        return self.map_tp_to_scale[f"TP{tp_num}"]

    @classmethod
    def strategy_name(cls) -> str:
        return cls.__name__

    def tp_info(self):
        import copy
        return copy.deepcopy(self.map_tp_to_scale)


class SingleTpStrategy(ITpStrategy):
    """单TP"""

    def _generate_tp_scale(self, every_row_num):
        self.tp_count = 1
        self.last_tp_name = f"TP{self.tp_count}"
        self.map_tp_to_scale.update({
            "TP1": [self.row, self.column],
        })


class MultiTpStrategy(ITpStrategy):
    """多TP"""

    def _generate_tp_scale(self, every_row_num):
        integer = int(self.row / every_row_num)
        remainder = self.row % every_row_num
        if remainder > 0:
            self.tp_count = integer + 1
        else:
            self.tp_count = integer

        self.last_tp_name = f"TP{self.tp_count}"

        for tp_num in range(1, 1 + self.tp_count):
            if tp_num != self.tp_count:
                self.map_tp_to_scale[f"TP{tp_num}"] = [every_row_num * tp_num, self.column]
            else:
                self.map_tp_to_scale[f"TP{tp_num}"] = [self.row, self.column]


# 定制的TP策略
class Tp4Row7(ITpStrategy):
    """策略：总共4个TP，总共7行，每2行1个TP"""

    def _generate_tp_scale(self, every_row_num):
        self.tp_count = 4
        self.last_tp_name = f"TP{self.tp_count}"
        self.map_tp_to_scale = {
            "TP1": [2, self.column],
            "TP2": [4, self.column],
            "TP3": [6, self.column],
            "TP4": [self.row, self.column],
        }


@unique
class StrategyEnum(Enum):
    """TP策略枚举"""
    SingleTpStrategy = SingleTpStrategy
    MultiTpStrategy = MultiTpStrategy

    @classmethod
    def name_to_strategy(cls, name: str) -> ClassVar[ITpStrategy]:
        """
        映射：名字 ---> 策略类
        :param name: 策略类名称
        :return: 策略类（class TpStrategy 的实现类）
        """
        map_name_to_strategy = {
            SingleTpStrategy.__name__: cls.SingleTpStrategy.value,
            MultiTpStrategy.__name__: cls.MultiTpStrategy.value,
        }
        if name not in map_name_to_strategy:
            raise KeyError(f'不存在名称为"{name}"的TP策略。')
        return map_name_to_strategy.get(name)


class TpStrategyFactory(object):
    """TP策略工厂"""

    @classmethod
    def get_tp_strategy(cls, strategy_name: str, row: int, column: int, every_row_now=2):
        """生成TP策略实例"""
        strategy_class = StrategyEnum.name_to_strategy(strategy_name)
        strategy = strategy_class(row, column, every_row_now)
        return strategy


class TpStrategyContext(object):
    """TP策略封装"""

    def __init__(self, tp_strategy: ITpStrategy):
        """
        :param tp_strategy: 接口 TpStrategy 的实现类的对象
        """
        self.tp_strategy = tp_strategy

    def get_current_scale(self, tp_num: int) -> typeScale:
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

    def get_current_scale(self, tp_num: int) -> typeScale:
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

    @property
    def tp_info(self):
        return self._tp_strategy_context.tp_strategy.tp_info()


def get_tp_strategy_name(task_oper_type: int) -> str:
    """
    根据任务类型和产品规格，获取TP策略
    :param task_oper_type: 任务类型
    :return: TP策略类的名称
    """
    if task_oper_type in [TaskOperType.small_auto.value,
                          TaskOperType.small_file.value,
                          TaskOperType.small_passiveness.value,
                          TaskOperType.automatic_control]:
        tp_strategy_name = MultiTpStrategy.__name__
    elif task_oper_type in [TaskOperType.large_auto.value,
                            TaskOperType.large_file.value,
                            TaskOperType.large_passiveness.value]:
        tp_strategy_name = SingleTpStrategy.__name__
    else:
        raise ValueError(f'任务类型错误"{task_oper_type}"')
    return tp_strategy_name


if __name__ == '__main__':
    # task_oper_type_ = TaskOperType.small_passiveness.value
    task_oper_type_ = TaskOperType.large_passiveness.value

    gg_enum_ = Gg.gg_7_mul_80.value
    # gg_enum_ = Gg.gg_6_mul_66.value

    gg_str_: str = Gg.value_name(gg_enum_)
    row_, column_ = [int(num) for num in gg_str_.split("*")]

    strategy_name_ = get_tp_strategy_name(task_oper_type_)
    tp_strategy_facade = TpStrategyFacade(strategy_name_, row_, column_)
    print(f"TP策略名称：{tp_strategy_facade.strategy_name}")
    print(f"TP策略最后一个TP的名称：{tp_strategy_facade.last_tp_name}")
    current_tp_num = 1
    print(f"TP{current_tp_num}: row_column={tp_strategy_facade.get_current_scale(current_tp_num)}")
    print("- " * 30)
    print(f"to_info = {tp_strategy_facade.tp_info}")
