# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 开闭原则 --- P-61"


# 书籍接口
class IBook(object):

    def get_name(self):
        """书籍有名称"""
        pass

    def get_price(self):
        """书籍有售价"""
        pass

    def get_author(self):
        """书籍有作者"""
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


# 书店销售类
class BookStore(object):

    def __init__(self):
        self.book_list = list()
        self._generate_book_list()

    def _generate_book_list(self):
        """模拟高层模块获取书籍列表的业务"""
        self.book_list.append(NovelBook("天龙八部", 3200, "金庸"))
        self.book_list.append(NovelBook("巴黎圣母院", 5600, "雨果"))
        self.book_list.append(NovelBook("悲惨世界", 3500, "雨果"))
        self.book_list.append(NovelBook("金瓶梅", 4300, "兰陵笑笑生"))

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
