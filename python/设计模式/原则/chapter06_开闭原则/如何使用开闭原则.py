# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 开闭原则-如何使用开闭原则 --- P-69"

# TODO: 第一，通过接口或抽象类约束扩展，对扩展进行边界限定，不允许出现在接口或抽象类中不存在的publish方法；
#       第二，参数类型、引用对象尽量使用接口或抽象类型，而不是实现类；
#       第三，抽象层保持稳定，一旦确定即不允许修改。


# 书籍接口
class IBook(object):
    """书籍接口"""

    def get_name(self):
        """书籍有名称"""
        pass

    def get_price(self):
        """书籍有售价"""
        pass

    def get_author(self):
        """书籍有作者"""
        pass


class IComputerBook(IBook):
    """计算机书籍接口"""

    def get_scope(self):
        """计算机书籍有一个范围"""
        pass


# 小说类
class NovelBook(IBook):

    def __init__(self, name, price, author):
        self.name = name
        self.price = price
        self.author = author

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_author(self):
        return self.author


# 有了打折的需求后，扩展出来的小说类
# 打折销售的小说类
class OffNovelBook(NovelBook):

    def get_price(self):
        if self.price > 4000:
            # 原价大于40元打九折
            off_price = self.price * 0.9
        else:
            off_price = self.price * 0.8
        return off_price


# 计算机书籍类
# TODO: 首先，ComputerBook 类必须实现 IBook 的三个方法，是通过 IComputerBook 接口传递进来的约束，也就是我们制定的 IBook 接口
#       对扩展类 ComputerBook 产生了约束力，正是由于该约束力，BookStore 类才不需要进行大量的修改。（P-71）
class ComputerBook(IComputerBook):

    def __init__(self, name, price, author, scope):
        self.name = name
        self.price = price
        self.author = author
        self.scope = scope

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_author(self):
        return self.author

    def get_scope(self):
        return self.scope


# 书店销售类
class BookStore(object):

    def __init__(self):
        self.book_list = list()
        self._generate_book_list()

    def _generate_book_list(self):
        """模拟高层模块获取书籍列表的业务"""
        self.book_list.append(OffNovelBook("天龙八部", 3200, "金庸"))
        self.book_list.append(OffNovelBook("巴黎圣母院", 5600, "雨果"))
        self.book_list.append(OffNovelBook("悲惨世界", 3500, "雨果"))
        self.book_list.append(OffNovelBook("金瓶梅", 4300, "兰陵笑笑生"))
        self.book_list.append(ComputerBook("Think in Java", 4300, "Bruce Eckel", "编程语言"))

    def main(self):
        print("---------书店卖出去的书籍记录如下:---------")
        for book in self.book_list:
            # book: IBook
            print("{}{:<10s}\t{}{:<10s}\t{}{:10s}\t".format(
                "数据名称: ", book.get_name(),
                "书籍作者: ", book.get_author(),
                "书籍价格: ", "{:.2f}元".format(book.get_price() / 100)
            ))


if __name__ == '__main__':
    book_store = BookStore()
    book_store.main()
