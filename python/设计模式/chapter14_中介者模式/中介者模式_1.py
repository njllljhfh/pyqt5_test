# -*- coding:utf-8 -*-
import random


# 抽象中介者
class AbstractMediator(object):

    def __init__(self):
        self._purchase = Purchase(self)
        self._sale = Sale(self)
        self._stock = Stock(self)

    # 中介者最重要的方法叫做事件方法， 处理多个对象之间的关系
    def execute(self, string, *args):
        pass

    def getPurchase(self):
        return self._purchase

    def getSale(self):
        return self._sale

    def getStock(self):
        return self._stock


# 具体中介者
class Mediator(AbstractMediator):
    """
        中介者Mediator定义了多个private方法， 其目的是处理各个对象之间的依赖关系， 就是
        说把原有一个对象要依赖多个对象的情况移到中介者的私有方法中实现。 在实际项目中，
        一般的做法是中介者按照职责进行划分， 每个中介者处理一个或多个类似的关联请求。
    """

    # 中介者最重要的方法
    def execute(self, string, *args):
        if string == "purchase.buy":  # 采购电脑
            self._buyComputer(args[0])
        elif string == "sale.sell":  # 销售电脑
            self._sellComputer(args[0])
        elif string == "sale.offSell":  # 折价销售
            self._offSell()
        elif string == "stock.clear":  # 清仓处理
            self._clearStock()

    # 采购电脑
    def _buyComputer(self, number: int):
        # 电脑的销售情况
        saleStatus = self._sale.getSaleStatus()
        if saleStatus > 80:
            # 销售情况良好
            print(f"采购IBM电脑：{number} 台")
            self._stock.increase(number)
        else:
            # 销售情况不好
            buyNumber = int(number / 2)  # 折半采购
            print(f"采购IBM电脑：{buyNumber} 台")
            self._stock.increase(buyNumber)

    # 销售电脑
    def _sellComputer(self, number: int):
        if self._stock.getStockNumber() < number:  # 库存数量不够销售
            self._purchase.buyIBMComputer(number)

        self._stock.decrease(number)

    # 折价处理
    def _offSell(self):
        # 库房有多少卖多少
        print(f"折价销售IBM电脑 {self._stock.getStockNumber()} 台")

    # 清仓处理
    def _clearStock(self):
        # 要求清仓销售
        self._sale.offSale()

        # 要求采购人员不要采购
        self._purchase.refuseBuyIBM()


# 抽象同事类
class AbstractColleague(object):

    def __init__(self, mediator: AbstractMediator):
        self._mediator = mediator


# 修改后的采购管理
class Purchase(AbstractColleague):

    def __init__(self, mediator: AbstractMediator):
        super(Purchase, self).__init__(mediator)

    # 采购IBM电脑
    def buyIBMComputer(self, number: int):
        self._mediator.execute("purchase.buy", number)

    # 不再采购IBM电脑
    @classmethod
    def refuseBuyIBM(cls):
        print("不再采购IBM电脑")


# 修改后的库存管理
class Stock(AbstractColleague):

    def __init__(self, mediator: AbstractMediator):
        super(Stock, self).__init__(mediator)
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
        self._mediator.execute("stock.clear")


# 修改后的销售管理
class Sale(AbstractColleague):

    def __init__(self, mediator: AbstractMediator):
        super(Sale, self).__init__(mediator)

    # 销售IBM电脑
    def sellIBMComputer(self, number: int):
        self._mediator.execute("sale.sell", number)
        print(f"销售IBM电脑 {number} 台")

    # 反馈销售情况，0～100之间变化，0:代表根本就没人买, 100:代表非常畅销，出一个卖一个
    @classmethod
    def getSaleStatus(cls):
        # saleStatus = random.randint(0, 100)
        saleStatus = 95
        print(f"IBM电脑的销售情况为：{saleStatus}")
        return saleStatus

    # 折价处理
    def offSale(self):
        self._mediator.execute("sale.offSell")


# 修改后的场景类
class Client(object):
    # @staticmethod
    # def main():
    #     mediator = Mediator()
    #     # 采购人员采购电脑
    #     # fixme: mediator 中的 mediator._purchase 与 purchase 并不是同一个对象。这样没问题么？
    #     print("------采购人员采购电脑--------")
    #     purchase = Purchase(mediator)
    #     purchase.buyIBMComputer(100)
    #
    #     # 销售人员销售电脑
    #     print("\n------销售人员销售电脑--------")
    #     sale = Sale(mediator)
    #     sale.sellIBMComputer(1)
    #
    #     # 库房管理人员管理库存
    #     print("\n------库房管理人员清库处理--------")
    #     stock = Stock(mediator)
    #     stock.clearStock()
    #
    #     print('- ' * 30)
    #     print(stock.getStockNumber())

    @staticmethod
    def main():
        mediator = Mediator()
        # 采购人员采购电脑
        print("------采购人员采购电脑--------")
        purchase = mediator.getPurchase()
        purchase.buyIBMComputer(100)

        # 销售人员销售电脑
        print("\n------销售人员销售电脑--------")
        sale = mediator.getSale()
        sale.sellIBMComputer(1)

        # 库房管理人员管理库存
        print("\n------库房管理人员清库处理--------")
        stock = mediator.getStock()
        stock.clearStock()

        print('- ' * 30)
        print(stock.getStockNumber())


if __name__ == '__main__':
    client = Client()
    client.main()
