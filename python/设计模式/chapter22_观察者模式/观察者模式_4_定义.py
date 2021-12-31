# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 观察者模式-定义 --- P-288"


"""
观察者模式（Observer Pattern）也叫作发布订阅模式（Publish/Subscribe），它是一个在项目中经常使用的模式。
定义：
    Define a one-to-many dependency between objects so that when one object changes state,
    all its dependents are notified and updated automatically.
    定义对象间一种一对多的依赖关系，使得每当一个对象改变状态，所有依赖于他的对象都会得到通知并自动更新。
"""


# 观察者接口
class Observer(object):
    """
    观察者一般是一个接口，每一个实现该接口的实现类都是具体观察者。
    """

    def update(self):
        pass


# 具体观察者
class ConcreteObserver(Observer):
    """
    每个观察者在接受到消息后的处理反应是不同的，各个观察者有自己的处理逻辑。
    """

    def update(self):
        print(f'接收到信息，并进行处理！')


# 被观察者
class Subject(object):
    """
    定义被观察者必须实现的职责，它必须能够动态添加、取消观察者。
    它一般是 `抽象类` 或者是 `实现类`，仅仅完成作为被观察者必须实现的职责：管理观察者并通知观察者。
    """

    def __init__(self):
        # 定义一个观察者数组
        self._observerList: [Observer] = []

    def addObserver(self, observer: Observer):
        """添加观察者"""
        self._observerList.append(observer)

    def deleteObserver(self, observer: Observer):
        """删除观察者"""
        self._observerList.remove(observer)

    def notifyObservers(self):
        """通知所有观察者"""
        for observer in self._observerList:
            observer.update()


# 具体的被观察者
class ConcreteSubject(Subject):
    """
    定义被观察者自己的业务逻辑，同时定义对哪些事件进行通知。
    """

    def doSomething(self):
        self.notifyObservers()


"""============================== 场景类 =============================="""


# 场景类
class Client(object):

    @staticmethod
    def main():
        # 创建一个被观察者
        subject = ConcreteSubject()

        # 定义一个观察者
        obs = ConcreteObserver()

        # 观察者观察被观察者
        subject.addObserver(obs)

        # 被观察者开始活动了
        subject.doSomething()


if __name__ == '__main__':
    client = Client()
    client.main()
