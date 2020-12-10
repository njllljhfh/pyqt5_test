# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 适配器模式_2_定义 --- P-238"

"""
适配器模式（Adapter Pattern）的定义如下：
    Convert the interface of a class into anther interface clients expect.
    Adapter lets classes work together that couldn't otherwise because of incompatible interfaces.
    （将一个类的接口变换成客户端所期待的另一个种接口，从而使原本因接口不匹配而无法再一起工作的两个类能够在一起工作。）


适配器模式又叫做 变压器模式，也叫做 包装模式（Wrapper），但是包装模式可不止一个，还包括第17章讲解的装饰器模式。


适配器模式的三个角色：
    1.Target（目标角色）
        该角色定义把其他类转换为何种接口，也就是我们的期望接口，例子中的 IUserInfo 接口就是目标角色。
    2.Adaptee（源角色）
        你想要把谁转换成目标角色，这个"谁"就是源角色，他是已经存在的、运行良好的类或对象，
        经过适配器角色的包装，它会称为一个崭新、靓丽的角色。
    3.Adapter（适配器角色）
        适配器模式的核心角色，其他两个角色都是已经存在的角色，而适配器角色是需要新建立的，
        他的角色职责非常简单：把源角色转换为目标角色，怎么转换？通过继承或是类关联的方式。


适配器模式的使用场景
    适配器应用的场景只要记住一点就足够了：你有冬季修改一个已经投产中的接口时，适配器模式可能是最合适你的模式。
    比如系统扩展了，需要使用一个已有或新建立的类，但是这个类有不符合系统的接口，怎么办？使用适配器模式，这也是我们例子中提到的。


适配器模式的注意注意事项
    1.适配器模式最好在详细设计阶段不要考虑它，它不是为了解决还处在开发阶段的问题，而是解决正在服役的项目的问题，
      没有一个系统分析师会在做详细设计的时候考虑使用适配器模式，这个模式使用的主要场景是扩展应用，就像我们的例子一样，系统扩展了，
      不符合原有设计的时候才考虑通过适配器模式减少代码修改带来的风险。
    2.再次提醒点，项目一定要遵守 依赖倒置原则 和 里氏替换原则，否则即使在适合使用适配器的场合下，也会带来非常大的改造。


Java不支持多继承。

在实际项目中，【对象适配器】使用到的场景比较多。

技术是为业务服务的。
"""


# TODO:目标角色是一个接口或者是抽象类，一般不会是实现类。
# 目标角色
class Target(object):

    def request(self):
        """目标角色有自己的方法"""
        pass


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# 目标角色的实现类
class ConcreteTarget(Target):

    def request(self):
        print(f"If you need any help ,please call me!")


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# TODO(tip): 源角色也是已经服役状态（当然，非要建立一个新角色，然后套用适配器模式，那也是没有任何问题），他是一个正常的类。
# 源角色
class Adaptee(object):

    def do_something(self):
        """原有的业务逻辑"""
        print(f"I'm kind of busy, leave me alone, please!")


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# TODO:【类适配器】
# 适配器角色
class Adapter(Target, Adaptee):

    def request(self):
        super().do_something()


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# 场景类
class Client(object):

    @staticmethod
    def main():
        print("- - - - - - - - - 原有的业务逻辑 - - - - - - - - - ")
        target = ConcreteTarget()
        target.request()

        print("- - - - - - - - - 现在增加了适配器橘色后的业务逻辑 - - - - - - - - - ")
        target_2 = Adapter()
        target_2.request()


if __name__ == '__main__':
    client = Client()
    client.main()
