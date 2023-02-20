# -*- coding:utf-8 -*-

"""
原型模式的定义:
    Specify the kinds of objects to create using a prototypical instance,
    and create new objects by copying this prototype.
    （用原型实例指定创建对象的种类，并且通过拷贝这些原型创建新的对象。）


最佳实践：
    原型模式先产生出一个包含大量共有信息的类，然后可以拷贝出副本，修正细节信息，建立了一个完整的个性对象。
    不知道大家有没有看过施瓦辛格演的《第六日》这部电影，电影的主线也就是一个人被复制，然后正本和副本对掐。
    我们今天讲的原型模式也就是由一个正本可以创建多个副本的概念。
    可以这样理解：一个对象的产生可以不由零起步，直接从一个已经具备一定雏形的对象克隆，然后再修改为生产需要的对象。
    也就是说，产生一个人，可以不从1岁长到2岁，再到3岁……也可以直接找一个人，从其身上获得DNA，然后克隆一个，直接修改一下就是30岁了！
    我们讲的原型模式也就是这样的功能。
"""

import copy


# 可拷贝
class Cloneable(object):
    def clone(self):
        raise NotImplementedError()


# 实现一个接口，然后重写clone方法，就完成了原型模式！
class PrototypeClass(Cloneable):
    # 覆写父类方法
    def clone(self):
        return copy.deepcopy(self)
