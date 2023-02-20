# -*- coding:utf-8 -*-


""" ============================== 接口、抽象类、基类 =============================="""


# 抽象产品类
class AbstractProduct(object):

    def beProduced(self):
        """
        甭管是什么产品它总要能被生产出来
        :return:
        """
        raise NotImplementedError()

    def beSold(self):
        """
        生产出来的东西， 一定要销售出去， 否则亏本
        :return:
        """
        raise NotImplementedError()


# 抽象公司
class AbstractCorp(object):
    def __init__(self, product: AbstractProduct):
        self.product = product

    def makeMoney(self):
        """
        公司是干什么的？赚钱的
        :return:
        """
        # 每个公司都是一样， 先生产
        self.product.beProduced()
        # 然后销售
        self.product.beSold()


""" ============================== 具体类 =============================="""


# 房子
class House(AbstractProduct):

    def beProduced(self):
        print(f'生产出的房子是这样的...')

    def beSold(self):
        print(f'生产出的房子卖出去了...')


#  iPod产品
class IPod(AbstractProduct):

    def beProduced(self):
        print(f'生产出的iPod是这样的...')

    def beSold(self):
        print(f'生产出的iPod卖出去了...')


# 服装
class Clothes(AbstractProduct):

    def beProduced(self):
        print(f'生产出的衣服是这样的...')

    def beSold(self):
        print(f'生产出的衣服卖出去了...')


# 房地产公司
class HouseCorp(AbstractCorp):

    def __init__(self, product: House):  # 这里的 product 是具体类 House
        super().__init__(product)

    def makeMoney(self):
        super().makeMoney()
        print(f'房地产公司赚大钱了...')


# 山寨公司
class ShanZhaiCorp(AbstractCorp):

    def __init__(self, product: AbstractProduct):  # 这里的 product 是抽象类 AbstractProduct
        super().__init__(product)

    def makeMoney(self):
        super().makeMoney()
        print(f'我赚钱呀...')


# 场景类
class Client(object):
    @staticmethod
    def main():
        house = House()
        print(f'-------房地产公司是这样运行的-------')
        houseCorp = HouseCorp(house)
        houseCorp.makeMoney()
        print()

        print(f'-------山寨公司是按这样运行的-------')
        # 山寨公司生产的产品很多， 不过我只要指定产品就成了
        # shanZhaiCorp = ShanZhaiCorp(IPod())  # 卖 ipod
        shanZhaiCorp = ShanZhaiCorp(Clothes())  # 卖 服装
        shanZhaiCorp.makeMoney()


if __name__ == '__main__':
    client = Client()
    client.main()
