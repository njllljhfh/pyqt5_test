# -*- coding:utf-8 -*-
import copy
from enum import Enum, unique
from typing import ClassVar

# Data structure.
typeScale = [int, int]  # The scale of every tp step.


class BaseTpStrategy(object):
    """Tp interface."""

    def __init__(self, row: int, column: int, num_of_rows_per_tp: int = None):
        """
        :param row: Total row.
        :param column: Total column.
        :param num_of_rows_per_tp: The number of rows per tp step.
        """
        self.tp_count = 0  # Total tp number.
        self.last_tp_name = ""  # The name of last tp.
        self.row = row
        self.column = column
        self.map_tp_to_scale: {str: typeScale} = dict()  # The mapping of tp name and tp scale.
        self._generate_tp_scale(num_of_rows_per_tp)

    def _generate_tp_scale(self, num_of_rows_per_tp) -> None:
        """
        Generate tp scale for every tp step.
        :param num_of_rows_per_tp: The number of rows per tp step.
        :return: None.
        """
        pass

    def get_current_scale(self, tp_num: int) -> typeScale:
        """
        Get the tp scale of tp_num given.
        :param tp_num: Tp number.
        :return: The tp scale of tp_num given.
        """
        if tp_num <= 0 or tp_num > self.tp_count:
            raise ValueError(f"TP{tp_num} out of the tp range `TP1-TP{self.tp_count}`.")
        return self.map_tp_to_scale[f"TP{tp_num}"]

    def tp_info(self) -> dict:
        return copy.deepcopy(self.map_tp_to_scale)

    @classmethod
    def strategy_name(cls) -> str:
        return cls.__name__


class SingleTpStrategy(BaseTpStrategy):

    def _generate_tp_scale(self, num_of_rows_per_tp):
        self.tp_count = 1
        self.last_tp_name = f"TP{self.tp_count}"
        self.map_tp_to_scale.update(
            {
                "TP1": [self.row, self.column],
            }
        )


class MultiTpStrategy(BaseTpStrategy):

    def _generate_tp_scale(self, num_of_rows_per_tp):
        integer = int(self.row / num_of_rows_per_tp)
        remainder = self.row % num_of_rows_per_tp
        if remainder > 0:
            self.tp_count = integer + 1
        else:
            self.tp_count = integer

        self.last_tp_name = f"TP{self.tp_count}"

        for tp_num in range(1, 1 + self.tp_count):
            if tp_num != self.tp_count:
                self.map_tp_to_scale[f"TP{tp_num}"] = [num_of_rows_per_tp * tp_num, self.column]
            else:
                self.map_tp_to_scale[f"TP{tp_num}"] = [self.row, self.column]


# Customization tp.
# class Custom4TpStrategy(BaseTpStrategy):
#
#     def _generate_tp_scale(self, num_of_rows_per_tp):
#         self.tp_count = 4
#         self.last_tp_name = f"TP{self.tp_count}"
#         self.map_tp_to_scale.update(
#             {
#                 "TP1": [1, self.column],
#                 "TP2": [3, self.column],
#                 "TP3": [7, self.column],
#                 "TP4": [self.row, self.column],
#             }
#         )


@unique
class StrategyEnum(Enum):
    """Tp strategy class enumeration."""
    singleTpStrategy = SingleTpStrategy
    multiTpStrategy = MultiTpStrategy

    # custom4TpStrategy = Custom4TpStrategy

    @classmethod
    def get_strategy_by_name(cls, name: str) -> ClassVar[BaseTpStrategy]:
        """
        Get subclass of class ITpStrategy by subclass name.
        :param name: Name of tp strategy class.
        :return: Subclass of class ITpStrategy.
        """
        map_name_to_strategy = {
            SingleTpStrategy.__name__: cls.singleTpStrategy.value,
            MultiTpStrategy.__name__: cls.multiTpStrategy.value,
            # Custom4TpStrategy.__name__: cls.custom4TpStrategy.value,
        }
        if name not in map_name_to_strategy:
            raise KeyError(f"Does not exist tp strategy with name `{name}`.")
        return map_name_to_strategy.get(name)


class TpStrategyFactory(object):
    """Tp strategy factory."""

    @classmethod
    def get_tp_strategy(cls, strategy_name: str, row: int, column: int, num_of_rows_per_tp=2):
        """Get tp strategy object."""
        strategy_class = StrategyEnum.get_strategy_by_name(strategy_name)
        strategy = strategy_class(row, column, num_of_rows_per_tp=num_of_rows_per_tp)
        return strategy


class TpStrategyContext(object):
    """Context of tp strategy."""

    def __init__(self, tp_strategy: BaseTpStrategy):
        self.tp_strategy = tp_strategy

    def get_current_scale(self, tp_num: int) -> typeScale:
        return self.tp_strategy.get_current_scale(tp_num)

    @property
    def tp_count(self):
        return self.tp_strategy.tp_count

    @property
    def row(self):
        return self.tp_strategy.row

    @property
    def column(self):
        return self.tp_strategy.column

    @property
    def last_tp_name(self):
        return self.tp_strategy.last_tp_name

    @property
    def tp_info(self):
        return self.tp_strategy.tp_info()

    @property
    def strategy_name(self):
        return self.tp_strategy.strategy_name()


class TpStrategyFacade(object):
    """Facade of tp strategy."""

    def __init__(self, tp_strategy_name, row, column, num_of_rows_per_tp=2):
        try:
            tp_strategy = TpStrategyFactory.get_tp_strategy(tp_strategy_name, row, column,
                                                            num_of_rows_per_tp=num_of_rows_per_tp)
            self._tp_strategy_context = TpStrategyContext(tp_strategy)
        except Exception as e:
            raise e

    def get_current_scale(self, tp_num):
        return self._tp_strategy_context.get_current_scale(tp_num)

    @property
    def tp_count(self):
        return self._tp_strategy_context.tp_count

    @property
    def row(self):
        return self._tp_strategy_context.row

    @property
    def column(self):
        return self._tp_strategy_context.column

    @property
    def last_tp_name(self):
        return self._tp_strategy_context.last_tp_name

    @property
    def tp_info(self):
        return self._tp_strategy_context.tp_info

    @property
    def strategy_name(self):
        return self._tp_strategy_context.strategy_name


# class NewTpStrategyFacade(object):
#     def __init__(self, tp_strategy_name, row, column, num_of_rows_per_tp=2):
#         try:
#             tp_strategy = TpStrategyFactory.get_tp_strategy(tp_strategy_name, row, column,
#                                                             num_of_rows_per_tp=num_of_rows_per_tp)
#             self._tp_strategy_context = TpStrategyContext(tp_strategy)
#         except Exception as e:
#             raise e
#
#     @property
#     def tp_info(self):
#         return self._tp_strategy_context.tp_info


def get_tp_strategy_name(img_type: str) -> str:
    """
    Get class name of tp strategy by detect_site.
    :param img_type: Table:`DETECT_SITE_LIST`, field:`IMG_TYPE`.
    :return: The subclass name of class ITpStrategy.
    """
    if img_type == '整图':
        tp_strategy_name = SingleTpStrategy.__name__
    # elif img_type == '自定义4TP':
    #     tp_strategy_name = Custom4TpStrategy.__name__
    else:
        tp_strategy_name = MultiTpStrategy.__name__

    return tp_strategy_name


if __name__ == '__main__':
    # ========= 获取策略的参数 ==========
    # img_type = '整图'
    # img_type = '分段图'
    img_type = '自定义4TP'

    row, column = [6, 80]
    # row, column = [7, 66]
    # row, column = [1, 12]
    # row, column = [9, 80]  # 自定义

    # ========= 业务1调用 ==========
    strategy_name = get_tp_strategy_name(img_type)
    tp_strategy_facade = TpStrategyFacade(strategy_name, row, column, num_of_rows_per_tp=3)
    print(f"TP策略名称：{tp_strategy_facade.strategy_name}")
    print(f"TP策略最后一个TP的名称：{tp_strategy_facade.last_tp_name}")
    current_tp_num = 1
    print(f"TP{current_tp_num}: row_column={tp_strategy_facade.get_current_scale(current_tp_num)}")
    print(f"tp_info = {tp_strategy_facade.tp_info}")
    print("- " * 30)

    # ========= 业务2调用 ==========
    # nww_tp_strategy_facade = NewTpStrategyFacade(strategy_name, row, column, num_of_rows_per_tp=3)
    # print(nww_tp_strategy_facade.tp_info)
    # ==============================

    import requests

    requests.get()
