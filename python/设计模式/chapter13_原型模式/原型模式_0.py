# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 原型模式(Builder Pattern)_1 --- P-152"

# 广告信模板
class AdvTemplate(object):

    def __init__(self):
        # 广告信名称
        self.advSubject = 'XX银行国庆信用卡抽奖活动'
        # 广告信内容
        self.advContext = '国庆抽奖活动通知： 只要刷卡就送你一百万！ ...'

        # 取得广告信的名称

    # 取得广告信的名称
    def getAdvSubject(self):
        return self.advSubject

    # 取得广告信的内容
    def getAdvContext(self):
        return self.advContext


# 邮件类
class Mail(object):

    def __init__(self, advTemplate: AdvTemplate):
        # 收件人
        self.receiver = None
        # 邮件名称
        self.subject = advTemplate.getAdvSubject()
        # 称谓
        self.appellation = None
        # 邮件内容
        self.context = advTemplate.getAdvContext()
        # 邮件的尾部， 一般都是加上"XXX版权所有"等信息
        self.tail = None

    """以下为getter/setter方法"""

    def getReceiver(self):
        return self.receiver

    def setReceiver(self, receiver: str):
        self.receiver = receiver

    def getSubject(self):
        return self.subject

    def setSubject(self, subject):
        self.subject = subject

    def getAppellation(self):
        return self.appellation

    def setAppellation(self, appellation):
        self.appellation = appellation

    def getContext(self):
        return self.context

    def setContext(self, context):
        self.context = context

    def getTail(self):
        return self.tail

    def setTail(self, tail):
        self.tail = tail


# 场景类
class Client(object):
    # 发送账单的数量， 这个值是从数据库中获得
    MAX_COUNT = 6

    @classmethod
    def main(cls):
        # 模拟发送邮件
        i = 0
        # 把模板定义出来， 这个是从数据库中获得
        mail = Mail(AdvTemplate())
        mail.setTail('XX银行版权所有')
        while i < cls.MAX_COUNT:
            # 以下是每封邮件不同的地方
            mail.setAppellation(f'先生（女士）-{i}')
            mail.setReceiver(f'{i}' * 5 + '@' + f'{i}' * 8)
            # 然后发送邮件
            cls.sendMail(mail)
            i += 1

    # 发送邮件
    @classmethod
    def sendMail(cls, mail: Mail):
        print(f'标题：{mail.getSubject()}\t收件人：{mail.getReceiver()}\t...发送成功！')


if __name__ == '__main__':
    client = Client()
    client.main()
