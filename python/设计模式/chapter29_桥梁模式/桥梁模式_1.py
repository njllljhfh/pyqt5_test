# -*- coding:utf-8 -*-


""" ============================== 接口、抽象类、基类 =============================="""


# 抽象公司
class AbstractCorp(object):

    def produce(self):
        """
        如果是公司就应该有生产，不管是软件公司还是制造业公司，每家公司生产的东西都不一样，所以由实现类来完成
        :return:
        """
        raise NotImplementedError()

    def sell(self):
        """
        有产品了， 那肯定要销售啊， 不销售公司怎么生存
        :return:
        """
        raise NotImplementedError()

    def makeMoney(self):  # 这是 模板方法
        """
        公司是干什么的？赚钱的
        :return:
        """
        # 每个公司都是一样， 先生产
        self.produce()
        # 然后销售
        self.sell()


""" ============================== 具体类 =============================="""


class HouseCorp(AbstractCorp):

    def produce(self):
        print(f'房地产公司盖房子...')

    def sell(self):
        print(f'房地产公司出售房子...')

    def makeMoney(self):
        super().makeMoney()
        print(f'房地产公司赚大钱了...')


class ClothesCorp(AbstractCorp):

    def produce(self):
        print(f'服装公司生产衣服...')

    def sell(self):
        print(f'服装公司出售衣服...')

    def makeMoney(self):
        super().makeMoney()
        print(f'服装公司赚小钱...')


class IPodCorp(AbstractCorp):

    def produce(self):
        print(f'我生产iPod...')

    def sell(self):
        print(f'iPod畅销...')

    def makeMoney(self):
        super().makeMoney()
        print(f'我赚钱呀...')


# 场景类
class Client(object):
    @staticmethod
    def main():
        print(f'-------房地产公司是这样运行的-------')
        houseCorp = HouseCorp()
        houseCorp.makeMoney()
        print()

        print(f'-------服装公司是这样运行的-------')
        clothesCorp = ClothesCorp()
        clothesCorp.makeMoney()
        print()

        print(f'-------山寨公司是按这样运行的-------')
        iPodCorp = IPodCorp()
        iPodCorp.makeMoney()


if __name__ == '__main__':
    client = Client()
    client.main()
