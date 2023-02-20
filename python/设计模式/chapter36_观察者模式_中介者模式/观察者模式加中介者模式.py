# -*- coding:utf-8 -*-
# todo: 本章，未完待续
from __future__ import annotations

import copy
from enum import Enum, unique
from typing import List


class Cloneable(object):

    def clone(self) -> object:
        return copy.deepcopy(self)


class Product(Cloneable):

    def __init__(self, manager: ProductManager, name: str):
        self.name = ''
        self.canChanged = False
        if manager.isCreateProduct():  # 这种一个对象只能由固定的对象初始化的方法就叫做: 单来源调用（SingleCall）
            # 允许建立产品
            self.canChanged = True
            self.name = name

    def getName(self):
        return self.name

    def setName(self, name: str):
        if self.canChanged:
            self.name = name

    def clone(self) -> Product:
        p = self.clone()
        return p


class ProductManager(object):

    def __init__(self):
        # 是否可以创建一个产品
        self.isPermittedCreate = False

    # 建立一个产品
    def createProduct(self, name: str) -> Product:
        self.isPermittedCreate = True
        p = Product(self, name)
        return p

    # 废弃一个产品
    @classmethod
    def abandonProduct(cls, p: Product):
        p = None

    # 修改一个产品
    @classmethod
    def editProduct(cls, p: Product, name: str):
        p.setName(name)

    # 获得是否可以创建一个产品
    def isCreateProduct(self):
        return self.isPermittedCreate

    # 克隆一个产品
    @classmethod
    def clone(cls, p: Product):
        return

# 事件类型定义
@unique
class ProductEventType(Enum):
    NEW_PRODUCT = 1
    DEL_PRODUCT = 2
    EDIT_PRODUCT = 3
    CLONE_PRODUCT = 4


# 观察者接口
class IObserver(object):
    def update(self, observable: AbstractObservable, obj: object):
        """
        :param observable: 被观察者
        :param obj: 要传递的数据对象 DTO(Data Transfer Object)。由被观察者生成，由观察者消费。
        :return:
        """
        pass


# 被观察者抽象类
class AbstractObservable(object):
    def __init__(self):
        # 所有的观察者
        self._observerList: List[IObserver] = []

    def addObserver(self, observer: IObserver):
        """添加观察者"""
        self._observerList.append(observer)

    def deleteObserver(self, observer: IObserver):
        """删除观察者"""
        self._observerList.remove(observer)

    def notifyObservers(self, obj: object):
        """通知所有观察者"""
        for observer in self._observerList:
            observer.update(self, obj)


# 产品事件
class ProductEvent(AbstractObservable):

    # 事件源头以及事件类型
    def __init__(self, p: Product, type_: ProductEventType):
        super(ProductEvent, self).__init__()
        self.source = p
        self.type = type_
        # 事件触发
        self._notifyEventDispatch()

    # 获得事件的始作俑者
    def getSource(self):
        return self.source

    # 获得事件的类型
    def getEventType(self):
        return self.type

    # 通知事件处理中心
    def _notifyEventDispatch(self):
        # self.addObserver(EventDispatch.getEventDispatch())
        self.addObserver(EventDispatch())
        # self.setChanged()
        self.notifyObservers(self.source)


# 事件的观察者
class EventDispatch(IObserver):
    """单例：线程不安全"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
