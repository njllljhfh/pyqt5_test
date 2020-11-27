# -*- coding:utf-8 -*-
from typing import NewType, ClassVar

UserId = NewType('UserId', int)
some_id = UserId(524313)


def get_user_name(user_id: UserId) -> str:
    return "xxx"


# typechecks
user_a = get_user_name(UserId(42351))

# does not typecheck; an int is not a UserId
user_b = get_user_name(-1)
print(f"user_b = {user_b}")

output = UserId(100) + UserId(200)
print(f"output = {output}")
print(f"type(output) = {type(output)}")

print(f"* " * 30)
from typing import TypeVar, Generic
from logging import Logger
import logging

T = TypeVar('T')
S = TypeVar('S', int, float)


class LoggedVar(Generic[T]):
    def __init__(self, value: T, name: str, logger: Logger) -> None:
        self.name = name
        self.logger = logger
        self.value = value

    def set(self, new: T) -> None:
        self.log('Set ' + repr(self.value))
        self.value = new

    def get(self) -> T:
        self.log('Get ' + repr(self.value))
        return self.value

    def log(self, message: str) -> None:
        self.logger.info('%s: %s', self.name, message)
        print(message)


logger = logging.getLogger(__name__)
lv = LoggedVar(111, "b", logger)
a = lv.get()
print(f"type(a) = {type(a)}")
# - - -
print(f"* " * 30)
# # from collections.abc import Iterable
# from typing import Iterable
#
#
# def zero_all_vars(vars: Iterable[LoggedVar[int]]) -> None:
#     for var in vars:
#         var.set(0)
#
#
# vars_x = [lv, ]
# zero_all_vars(vars_x)
#
# # - - -
# print(f"* " * 30)
#
#
# class LoggedVar2(Generic[T, S]):
#     def __init__(self, value: T, name: str, logger: Logger) -> None:
#         self.name = name
#         self.logger = logger
#         self.value = value
#
#     def set(self, new: T) -> None:
#         self.log('Set ' + repr(self.value))
#         self.value = new
#
#     def get(self) -> T:
#         self.log('Get ' + repr(self.value))
#         return self.value
#
#     def log(self, message: str) -> None:
#         self.logger.info('%s: %s', self.name, message)
#         print(message)
#
#     def get_name(self):
#         print(self.name)
#         return self.name
#
#
# lv2 = LoggedVar2(1, 0.12, logger)
#
# a = lv2.get()
# print(f"type(a) = {type(a)}")
# a = lv2.get_name()
# print(f"type(a) = {type(a)}")
print("* " * 30)
from typing import Iterable


def xxx(vars: Iterable[str]):
    print(vars)


xxx(['1', '2'])

print("* " * 30)


class Human(object):

    def __init__(self, name):
        self.name = name

    def get_name(self):
        pass


class YellowHuman(Human):

    def get_name(self):
        return self.name


def get_human(var: ClassVar[Human], name):
    return var(name)


x = get_human(YellowHuman, "dragon")

print(x.get_name())
