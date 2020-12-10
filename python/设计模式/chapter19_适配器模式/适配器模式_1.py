# -*- coding:utf-8 -*-
# __source__ = "《设计模式之禅》--- 适配器模式()_1 --- P-232"

"""
一个对象如果不存储实体状态以及对象之间的关系，该对象就较多贫血对象，对应的领域模型就是贫血领域模型，
有实体状态和对象关系的模型就是充血领域模型。
"""


# 员工信息接口
class IUserInfo(object):

    def get_user_name(self):
        """获取用户名"""
        pass

    def get_home_address(self):
        """获得家庭地址"""
        pass

    def get_mobile_number(self):
        """手机号码，这个太重要，手机泛滥呀"""
        pass

    def get_office_tel_number(self):
        """办公电话，一般是座机"""
        pass

    def get_job_position(self):
        """这个人的职位是什么"""
        pass

    def get_home_tel_number(self):
        """获得家庭电话，这有点不好，我不喜欢打家庭电话讨论工作"""
        pass


# 实现类
class UserInfo(IUserInfo):

    def get_home_address(self):
        print(f"这里是员工的家庭地址...")

    def get_home_tel_number(self):
        print(f"员工的家庭电话是...")

    def get_job_position(self):
        print(f"这个人的职位是BOSS...")

    def get_mobile_number(self):
        print(f"这个人的手机号码是0000...")

    def get_office_tel_number(self):
        print(f"办公室电话是...")

    def get_user_name(self):
        print(f"姓名叫做...")


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# 劳动服务公司的人员信息接口
class IOuterUser(object):

    def get_user_base_info(self):
        """基本信息，比如名称、性别、手机号码等"""
        pass

    def get_user_office_info(self):
        """工作区域信息"""
        pass

    def get_user_home_info(self):
        """用户的家庭信息"""
        pass


# 劳动服务公司的人员信息的实现类
class OuterUser(IOuterUser):

    def get_user_base_info(self):
        base_info = dict()
        base_info["user_name"] = "这个员工叫混世魔王...."
        base_info["mobile_number"] = "这个员工的额电话是...."
        return base_info

    def get_user_home_info(self):
        home_info = dict()
        home_info["home_tel_number"] = "员工的家庭电话是...."
        home_info["home_address"] = "员工的家庭地址是...."
        return home_info

    def get_user_office_info(self):
        office_info = dict()
        office_info["job_position"] = "这个人的职位是BOSS...."
        office_info["office_tel_number"] = "员工的办公电话是...."
        return office_info


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """

"""
咱们的系统要和他们的系统进行交互，怎么办？我们不可能为了这一小小的功能而对我们已经运行良好的系统进行大手术，那怎么办？
我们可以转化，先拿到对方的数据对象，然后转化为我们自己的数据对象，中间加一层转换处理。

OuterUserInfo 可以看做是"两面派"，实现了 IUserInfo 接口，还继承了 OuterUser，
通过这样的设计，把 OuterUser 伪装成我们系统中一个IUserInfo对象，
这样，我们的系统基本不用修改，所有的人员查询、调用跟本地一样。

注意：我们之所以能够增加一个 OuterUserInfo 中转类，是因为我们在系统设计时严格遵守了 依赖倒置原则 和 里氏替换原则，
     否则即使增加了中转类也无法解决问题。
"""


# TODO:【类适配器】
# 中转角色
class OuterUserInfo(IUserInfo, OuterUser):

    def __init__(self):
        # 员工的基本信息
        self.base_info = super().get_user_base_info()
        # 员工的家庭信息
        self.home_info = super().get_user_home_info()
        # 工作信息
        self.office_info = super().get_user_office_info()

    def get_home_address(self):
        home_address = self.home_info["home_address"]
        print(f"{home_address}")
        return home_address

    def get_home_tel_number(self):
        home_tel_number = self.home_info["home_tel_number"]
        print(f"{home_tel_number}")
        return home_tel_number

    def get_job_position(self):
        job_position = self.office_info["job_position"]
        print(f"{job_position}")
        return job_position

    def get_mobile_number(self):
        mobile_number = self.base_info["mobile_number"]
        print(f"{mobile_number}")
        return mobile_number

    def get_office_tel_number(self):
        office_tel_number = self.office_info["office_tel_number"]
        print(f"{office_tel_number}")
        return office_tel_number

    def get_user_name(self):
        user_name = self.base_info["user_name"]
        print(f"{user_name}")
        return user_name


"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - """


# 场景类
# 公司大老板想看看我们自己公司年轻女孩子的电话号码
class Client(object):
    # @staticmethod
    # def main():
    #     """没有与外系统连接的时候，是这样写的"""
    #     young_girl = UserInfo()
    #     # 从数据库中查到3个
    #     for i in range(3):
    #         young_girl.get_mobile_number()

    # TODO(tip): 使用了适配器模式只修改了一句话，其他的业务逻辑都不用修改就解决了系统对接的问题，
    #            而且在我们实际系统中只是增加了一个业务类的继承，就实现了可以查本公司员工信息，也可以查人力资源公司的员工信息，
    #            尽量少的修改，通过扩展的方式解决了该问题。这就是适配器模式。
    @staticmethod
    def main():
        """查看劳动公司人员信息场景"""
        young_girl = OuterUserInfo()
        # 从数据库中查到3个
        for i in range(3):
            young_girl.get_mobile_number()


if __name__ == '__main__':
    client = Client()
    client.main()
