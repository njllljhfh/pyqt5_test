# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》 --- 迪米特法则-不符合迪米特法则 --- P-53"


# TODO: 朋友类的定义:出现在成员变量、方法的输入输出参数中的类称为成员朋友类，而出现在方法体内部的类不属于朋友类。
# 女生类
class Girl(object):

    def __init__(self):
        pass


# 体育委员类
class GroupLeader(object):

    @staticmethod
    def count_girls(list_girls):
        """清查女生数量"""
        print(f"女生的数量是：{len(list_girls)}")


# 老师类
class Teacher(object):

    @staticmethod
    def command(group_leader: GroupLeader):
        # 初始化女生
        list_girls = list()
        for i in range(20):
            list_girls.append(Girl())

        # 告诉体育委员开始执行清查任务
        group_leader.count_girls(list_girls)


# 场景类
class Client(object):

    @staticmethod
    def main():
        teacher = Teacher()
        group_leader = GroupLeader()
        # 老师发布命令
        teacher.command(group_leader)


if __name__ == '__main__':
    client = Client()
    client.main()
