# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》-- P-500 -- 工厂方法模式+策略模式"
from enum import Enum, unique


# IC卡类
class Card(object):
    """IC卡类"""

    def __init__(self):
        self.cardNo = ""  # 卡号
        self.steadyMoney = 0  # 固定类型金额
        self.freeMoney = 0  # 自由类型金额

    def getCardNo(self):
        return self.cardNo

    def setCardNo(self, cardNo):
        self.cardNo = cardNo

    def getSteadyMoney(self):
        return self.steadyMoney

    def setSteadyMoney(self, steadyMoney):
        self.steadyMoney = steadyMoney

    def getFreeMoney(self):
        return self.freeMoney

    def setFreeMoney(self, freeMoney):
        self.freeMoney = freeMoney


# 交易类
class Trade(object):
    """交易类"""

    def __init__(self):
        self.tradeNo = ""  # 交易号
        self.amount = 0  # 交易金额

    def getTradeNo(self):
        return self.tradeNo

    def setTradeNo(self, tradeNo):
        self.tradeNo = tradeNo

    def getAmount(self):
        return self.amount

    def setAmount(self, amount):
        self.amount = amount


"""============================================================================================================"""


# 扣款策略接口
class IDeduction(object):
    """扣款策略接口"""

    def exec(self, card: Card, trade: Trade) -> bool:
        """扣款"""
        pass


# 扣款策略一:固定金额和自由金额各扣除50%
class SteadyDeduction(IDeduction):

    def exec(self, card: Card, trade: Trade) -> bool:
        """固定金额和自由金额各扣除50%"""
        halfMoney = int(trade.getAmount() / 2 + 0.5)  # 四舍五入
        card.setSteadyMoney(card.getSteadyMoney() - halfMoney)
        card.setFreeMoney(card.getFreeMoney() - halfMoney)
        return True


# 扣款策略二:直接从自由金额中扣除
class FreeDeduction(IDeduction):

    def exec(self, card: Card, trade: Trade) -> bool:
        """直接从自由金额中扣除"""
        card.setFreeMoney(card.getFreeMoney() - trade.getAmount())
        return True


# 扣款策略封装
class DeductionContext(object):
    """扣款策略封装"""

    def __init__(self, deduction: IDeduction):
        self.deduction = deduction

    def exec(self, card: Card, trade: Trade) -> bool:
        return self.deduction.exec(card, trade)


# 策略管理
@unique
class StrategyManager(Enum):
    """策略管理"""
    SteadyDeduction = SteadyDeduction
    FreeDeduction = FreeDeduction

    @classmethod
    def name_to_strategy(cls, name: str):
        """
        映射：枚举名字 --> 策略类
        :param name: 策略枚举类的名字
        :return: 策略类(class IDeduction 的实现)
        """
        map_name_to_strategy = {
            cls.SteadyDeduction.name: cls.SteadyDeduction.value,
            cls.FreeDeduction.name: cls.FreeDeduction.value,
        }
        return map_name_to_strategy.get(name)


# 策略工厂
class StrategyFactory(object):
    """
    策略工厂
    修正《策略模式》必须对外暴露具体策略类的问题，由《工厂方法模式》直接产生一个具体策略对象，而其他模块不需要依赖具体策略。
    """

    @classmethod
    def get_deduction(cls, strategy_name: str):
        """
        获取策略
        :param strategy_name: 策略枚举类的名字
        :return:
        """
        # 获取策略类
        strategy = StrategyManager.name_to_strategy(strategy_name)
        return strategy()


"""============================================================================================================"""


# 扣款模块封装（门面模式）
class DeductionFacade(object):
    """扣款模块封装（门面模式）"""

    @classmethod
    def deduct(cls, card: Card, trade: Trade) -> Card:
        """消费，对外公布的扣款信息"""
        # 获取消费策略类的名字
        strategy_name = cls.getDeductionType(trade)
        # 初始化一个策略
        deduction = StrategyFactory.get_deduction(strategy_name)
        # 产生一个策略上下文
        context = DeductionContext(deduction)
        # 进行扣款处理
        context.exec(card, trade)
        return card

    @classmethod
    def getDeductionType(cls, trade: Trade) -> str:
        """
        获得对应的商户消费策略
        :param trade:
        :return: subclass of IDeduction.
        """

        """
        这段代码在实际项目中是存在的，但是与此处的写法不同。
        在实际项目中，数据库中保存了策略代码与交易编码的对应关系，直接通过数据库的SQL语句就可以返回对应的策略。
        在实际项目中，读者请把该方法放到其他的Helper类中。
        """
        # 模拟操作（扣款策略的选择规则）
        if "s" in trade.getTradeNo():
            return SteadyDeduction.__name__
        else:
            return FreeDeduction.__name__


"""============================================================================================================"""


# 场景类
class Client(object):
    """场景类"""

    @classmethod
    def main(cls):
        """模拟交易"""
        # 初始化一个IC卡
        card = cls.initIC()
        # 显示一下卡内信息
        print(f"========初始卡信息:========")
        cls.showCard(card)
        # 是否停止运行状态
        flag = True
        while flag:
            # 模拟消费
            trade = cls.createTrade()
            DeductionFacade.deduct(card, trade)
            # 交易成功，打印出成功处理消息
            print(f"========交易凭证========")
            print(f"{trade.getTradeNo()} 交易成功！")
            print(f"本次发生的交易金额：{trade.getAmount() / 100} 元")
            # 展示一下卡内信息
            cls.showCard(card)
            if input("是否需要退出？（y/n）").lower() == "y":
                flag = False

    @staticmethod
    def initIC():
        """初始化一个IC卡"""
        card = Card()
        card.setCardNo("1100010001000")
        card.setFreeMoney(1000 * 100)  # 1000元
        card.setSteadyMoney(800 * 100)  # 800元
        return card

    @staticmethod
    def createTrade():
        """产生一条交易"""
        trade = Trade()
        trade.setTradeNo(input(f"请输入交易号码: "))
        trade.setAmount(int(input(f"请输入交易金额: ")))
        return trade

    @staticmethod
    def showCard(card: Card):
        """打印出当前卡内交易余额"""
        print(f"IC卡编号：{card.getCardNo()}")
        print(f"固定类型余额：{card.getSteadyMoney() / 100.0} 元")
        print(f"自由类型余额：{card.getFreeMoney() / 100.0} 元")


if __name__ == '__main__':
    client = Client()
    client.main()
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
