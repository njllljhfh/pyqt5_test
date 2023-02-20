# -*- coding:utf-8 -*-
import random


# 采购管理
class Purchase(object):
    # 采购IBM电脑
    def buyIBMcomputer(self, number: int):
        # 访问库存
        stock = Stock()

        # 访问销售
        sale = Sale()

        # 电脑的销售情况
        saleStatus = sale.getSaleStatus()
        if saleStatus > 80:
            # 销售情况良好
            print(f"采购IBM电脑：{number}台")
            stock.increase(number)
        else:
            # 销售情况不好
            buyNumber = int(number / 2)  # 折半采购
            print(f"采购IBM电脑：{buyNumber}台")
            stock.increase(buyNumber)

    # 不再采购IBM电脑
    def refuseBuyIBM(self):
        print("不再采购IBM电脑")


#  库存管理
class Stock(object):

    def __init__(self):
        # 刚开始有100台电脑
        self._computer_number = 100

    # 库存增加
    def increase(self, number: int):
        self._computer_number += number
        print(f"库存数量为：{self._computer_number}")

    # 库存降低
    def decrease(self, number: int):
        self._computer_number -= number
        print(f"库存数量为：{self._computer_number}")

    # 获得库存数量
    def getStockNumber(self):
        return self._computer_number

    # 存货压力大了， 就要通知采购人员不要采购， 销售人员要尽快销售
    def clearStock(self):
        purchase = Purchase()
        sale = Sale()
        print(f"清理存货数量为：{self._computer_number}")

        # 要求折价销售
        sale.offSale()

        # 要求采购人员不要采购
        purchase.refuseBuyIBM()


# 销售管理
class Sale(object):
    # 销售IBM电脑
    def sellIBMComputer(self, number: int):
        # 访问库存
        stock = Stock()
        # 访问采购
        purchase = Purchase()
        if stock.getStockNumber() < number:  # 库存数量不够销售
            purchase.buyIBMcomputer(number)

        print(f"销售IBM电脑{number}台")
        stock.decrease(number)

    # 反馈销售情况，0～100之间变化，0 代表根本就没人买，100 代表非常畅销，出一个卖一个
    @classmethod
    def getSaleStatus(cls):
        # saleStatus = random.randint(0, 100)
        saleStatus = 95
        print(f"IBM电脑的销售情况为：{saleStatus}")
        return saleStatus

    # 折价处理
    def offSale(self):
        # 库房有多少卖多少
        stock = Stock()
        print(f"折价销售IBM电脑{stock.getStockNumber()} 台")


# 场景类
class Client(object):
    @staticmethod
    def main():
        # 采购人员采购电脑
        print("------采购人员采购电脑--------")
        purchase = Purchase()
        purchase.buyIBMcomputer(100)

        # 销售人员销售电脑
        print("\n------销售人员销售电脑--------")
        sale = Sale()
        sale.sellIBMComputer(1)

        # 库房管理人员管理库存
        print("\n------库房管理人员清库处理--------")
        stock = Stock()
        stock.clearStock()


if __name__ == '__main__':
    client = Client
    client.main()
